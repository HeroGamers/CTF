/* unified api for cgroups v1 and v2, because systemd decided we need to support v2 */
/* just #include this file, no need for linker issues */
/* we expect die(), urandom() to be around */

#if !defined(die) || !defined(die_noerrno)
#error "You should #include \"cgroups.c\""
#endif

#ifndef CGROUP2_SUPER_MAGIC
#define CGROUP2_SUPER_MAGIC 0x63677270 /* man 2 statfs */
#endif

typedef enum {
    CGROUPS_NOT_SUPPORTED = -2,
    CGROUPS_UNKNOWN = -1,
    CGROUPS_DISABLED = 0, /* allows -cg 0 to disable cgroups */
    CGROUPS_V1 = 1,
    CGROUPS_V2 = 2
} cgroups_version;

typedef struct
{
    cgroups_version version;
    union {
        struct {
            char root_path[40];
            char child_path[33];
        } v1;
        struct {
            char mount_path[40];
            bool ready; /* fs is there */
            bool did_mount; /* we mounted it ourselves */
            char cg_path[79];
        } v2;
    };
} cgroup_state_t;


/* helper functions */

static bool try_write_file(const char *file, const void *buf, size_t count)
{
    int fd = open(file, O_WRONLY | O_CLOEXEC);
    if (-1 == fd) {
        return false;
    }

    ssize_t n;
    for (size_t i = 0; i < count; i += n) {
        if (0 >= (n = write(fd, buf, count - i))) {
            close(fd);
            return false;
        }
    }

    return 0 == close(fd);
}

static void write_file(const char *file, const void *buf, size_t count)
{
    int fd = open(file, O_WRONLY | O_CLOEXEC);
    if (-1 == fd) {
        die("open");
    }

    ssize_t n;
    for (size_t i = 0; i < count; i += n)
        if (0 >= (n = write(fd, buf, count - i)))
            die("write");

    if (0 != close(fd)) {
        die("close");
    }
}

static bool try_write_value(const char *path, unsigned long value)
{
    char contents[64];
    int res;

    res = snprintf(contents, sizeof(contents), "%lu", value);
    if (res < 0 || (size_t) res >= sizeof(contents))
        die_noerrno("snprintf");
    return try_write_file(path, contents, strlen(contents));
}

static void write_value(const char *path, unsigned long value)
{
    char contents[64];
    int res;

    res = snprintf(contents, sizeof(contents), "%lu", value);
    if (res < 0 || (size_t) res >= sizeof(contents))
        die_noerrno("snprintf");
    write_file(path, contents, strlen(contents));
}


/* cgroups v2 implementation */

#define CGROUP_V2_CONTROLLERS "+pids +memory" /* NB: if you change this, adjust cgroup_v2_check_controllers */

static bool cgroup_v2_check_controllers(const char *path)
{
    char buf[256];
    char *iterator, *next;
    bool has_pid_controller = false;
    bool has_memory_controller = false;
    FILE *controllers = fopen(path, "re");

    if (NULL == controllers) {
        die("fopen");
    }
    if (NULL == fgets(buf, sizeof(buf), controllers)) { /* one line! */
        if (feof(controllers)) { /* no controllers at all! */
            if (0 != fclose(controllers)) {
                die("fclose");
            }
            return false;
        } else {
            die("fgets");
        }
    }
    if (0 != fclose(controllers)) {
        die("fclose");
    }

    /* remove newline */
    iterator = buf;
    next = strchr(iterator, '\n');
    if (NULL != next) {
        *next = '\0';
    }

    /* split into tokens */
    do {
        next = strchr(iterator, ' ');
        if (NULL != next) {
            *next = '\0';
        }
        if (0 == strcmp(iterator, "pids")) {
            has_pid_controller = true;
        } else if (0 == strcmp(iterator, "memory")) {
            has_memory_controller = true;
        }
        iterator = next + 1;
    } while (next);

    return (has_pid_controller && has_memory_controller);
}

typedef enum { PATH_PARENT, PATH_CHILD } cgroup_v2_level;

/* returns a pointer to a global buffer. do not multithread, do not free(). */
static const char *cgroup_v2_build_path(cgroup_state_t *state, cgroup_v2_level type, const char *leaf)
{
    static char path[4096];
    int res;

    res = snprintf(path, sizeof(path),
                   "%s/%s",
                   type == PATH_PARENT ? state->v2.mount_path : state->v2.cg_path,
                   leaf);
    if (res < 0 || (size_t) res >= sizeof(path))
        die_noerrno("snprintf");

    return path;
}

#define DEFAULT_CGROUP_MOUNT "/sys/fs/cgroup"
static void cgroup_v2_mount(cgroup_state_t *state)
{
    unsigned char rand[16];
    if (state->v2.ready)
        return;

    if (0 == access(DEFAULT_CGROUP_MOUNT, F_OK)) {
        /* /sys/fs/cgroup exists, check it is actually cgroup2 */
        struct statfs fs;
        if (0 == statfs(DEFAULT_CGROUP_MOUNT, &fs) && fs.f_type == CGROUP2_SUPER_MAGIC) {
            strncpy(state->v2.mount_path, DEFAULT_CGROUP_MOUNT, sizeof(state->v2.mount_path) - 1);
            state->v2.ready = true;

            if (0 != access(DEFAULT_CGROUP_MOUNT, W_OK)) {
                /* try to remount read-write */
                if (0 != mount(NULL, DEFAULT_CGROUP_MOUNT, NULL, MS_REMOUNT | MS_BIND, NULL)) {
                    state->v2.ready = false; /* failed, we need to mount elsewhere */
                }
            }
        }
    }
    if (!state->v2.ready)
    {
        /* no mounted cgroup2 directory (e.g. /sys/fs/cgroup), need to mount */
        strncpy(state->v2.mount_path, "/ynetd-", sizeof(state->v2.mount_path) - 1);
        _Static_assert(sizeof(state->v2.mount_path) - 1 >= sizeof("/ynetd-") - 1 + 2 * sizeof(rand),
                       "Not enough space for mount path");

        urandom(rand, sizeof(rand));
        for (size_t i = 0; i < sizeof(rand); ++i)
            snprintf(&state->v2.mount_path[i * 2 + 7], 3, "%02hhx", rand[i]);

        if (0 != mkdir(state->v2.mount_path, 0700)) {
            die("mkdir");
        }

        if (0 != mount("ynetd.cgroup2_root", state->v2.mount_path, "cgroup2", 0, NULL)) {
            die("mount");
        }

        state->v2.did_mount = true;
        state->v2.ready = true;
    }
}

static void cgroup_v2_umount(cgroup_state_t *state)
{
    if (state->v2.ready && state->v2.did_mount) {
        if (0 != umount(state->v2.mount_path)) {
            die("umount");
        }
        if (0 != rmdir(state->v2.mount_path)) {
            die("rmdir");
        }
        state->v2.did_mount = false;
        state->v2.ready = false;
    }
}

#define YNETD_ROOT_CGROUP "ynetd-root"
static void cgroup_v2_init(cgroup_state_t *state)
{
    cgroup_v2_mount(state);

    /* check whether the controllers we need are enabled */
    if (cgroup_v2_check_controllers(cgroup_v2_build_path(state, PATH_PARENT, "cgroup.subtree_control")))
        return;

    /* try to enable them normally */
    if (try_write_file(cgroup_v2_build_path(state, PATH_PARENT, "cgroup.subtree_control"), CGROUP_V2_CONTROLLERS, sizeof(CGROUP_V2_CONTROLLERS) - 1))
        return;

    /* this is weird. probably already tied up somewhere. */
    /* if it doesn't exist yet, create a root cgroup to move existing processes to */
    /* this seems to be necessary in docker */
    if (0 != mkdir(cgroup_v2_build_path(state, PATH_PARENT, YNETD_ROOT_CGROUP), 0700)) {
        if (errno != EEXIST)
            die("mkdir");
    }

    /* move all existing processes, including self */
    FILE *existing;
    int fd, len, moved;
    char buf[256];

    do {
        /* keep moving if new processes are added somehow */
        moved = 0;

        /* this setup is a little weird, but we need _one_ write() call _per PID_ */
        existing = fopen(cgroup_v2_build_path(state, PATH_PARENT, "cgroup.procs"), "re");
        if (NULL == existing) {
            die("fopen");
        }
        fd = open(cgroup_v2_build_path(state, PATH_PARENT, YNETD_ROOT_CGROUP "/cgroup.procs"), O_WRONLY | O_CLOEXEC);
        if (-1 == fd) {
            die("open");
        }

        while (NULL != fgets(buf, sizeof(buf), existing)) {
            ++moved;
            len = strlen(buf);
            if (len != write(fd, buf, len)) {
                die("write");
            }
        }

        if (0 != close(fd)) {
            die("close");
        }
        if (0 != fclose(existing)) {
            die("fclose");
        }
    } while (moved > 0);

    /* enable controllers in the parent now */
    write_file(cgroup_v2_build_path(state, PATH_PARENT, "cgroup.subtree_control"), CGROUP_V2_CONTROLLERS, sizeof(CGROUP_V2_CONTROLLERS) - 1);
}

static void cgroup_v2_child_init(cgroup_state_t *state)
{
    unsigned char rand[16];
    int res;
    size_t len;

    /* create cgroup */
    _Static_assert(sizeof(state->v2.cg_path) - 1 >= sizeof(state->v2.mount_path) - 1 +
                                                    sizeof("/ynetd-") - 1 + 2 * sizeof(rand),
                   "Not enough space for cgroup path");

    res = snprintf(state->v2.cg_path, sizeof(state->v2.cg_path), "%s/ynetd-", state->v2.mount_path);
    if (res < 0 || (size_t) res >= sizeof(state->v2.cg_path)) {
        die_noerrno("snprintf");
    }

    len = strlen(state->v2.cg_path);
    if (len >= sizeof(state->v2.cg_path) - sizeof(rand) * 2) {
        die_noerrno("strlen");
    }

    urandom(rand, sizeof(rand));
    for (size_t i = 0; i < sizeof(rand); ++i) {
        snprintf(&state->v2.cg_path[i * 2 + len], 3, "%02hhx", rand[i]);
    }

    if (0 != mkdir(state->v2.cg_path, 0700)) {
        die("mkdir");
    }

    /* this group is indivisible wrt. OOM */
    /* this is only supported in Linux 4.19+, while cgroups v2 is older, so we just try to set that up */
    try_write_value(cgroup_v2_build_path(state, PATH_CHILD, "memory.oom.group"), 1);
}

static void cgroup_v2_child_apply_limits(cgroup_state_t *state, const struct config *cfg)
{
    /* enable appropriate controllers in the parent, then set the limits in the child */
    if (cfg->pids.set) {
        write_value(cgroup_v2_build_path(state, PATH_CHILD, "pids.max"), cfg->pids.val);
    }
    if (cfg->memory_limit.set) {
        write_value(cgroup_v2_build_path(state, PATH_CHILD, "memory.max"), cfg->memory_limit.val);
    }
    /* add current process to cgroup */
    write_value(cgroup_v2_build_path(state, PATH_CHILD, "cgroup.procs"), 0);
}

static void cgroup_v2_child_cleanup(cgroup_state_t *state)
{
    /* delete possible cgroups, we ignore errors */
    rmdir(state->v2.cg_path);
}


/* cgroups v1 implementation */

static void cgroup_v1_init(cgroup_state_t *state)
{
    strncpy(state->v1.root_path, "/ynetd-", sizeof(state->v1.root_path) - 1);
    _Static_assert(sizeof(state->v1.root_path) >= sizeof("/ynetd-"), "Not enough space for prefix");

    unsigned char rand[16];
    urandom(rand, sizeof(rand));
    for (size_t i = 0; i < sizeof(rand); ++i)
        snprintf(&state->v1.root_path[i * 2 + 7], 3, "%02hhx", rand[i]);

    _Static_assert(sizeof(state->v1.root_path) - 1 >= 7 + 2 * sizeof(rand),
                   "Not enough space for cgroup root path");

    if (0 != mkdir(state->v1.root_path, 0700)) {
        die("mkdir");
    }

    if (0 != mount("ynetd.cgroup_root", state->v1.root_path, "tmpfs", 0, "mode=700")) {
        die("mount");
    }

    char buf[256] = {0};

    snprintf(buf, sizeof(buf), "%s/memory", state->v1.root_path);
    if (0 != mkdir(buf, 0700)) {
        die("mkdir");
    }
    if (0 != mount("ynetd.memory", buf, "cgroup", 0, "memory")) {
        die("mount");
    }

    snprintf(buf, sizeof(buf) ,"%s/pids", state->v1.root_path);
    if (0 != mkdir(buf, 0700)) {
        die("mkdir");
    }
    if (0 != mount("ynetd.pids", buf, "cgroup", 0, "pids")) {
        die("mount");
    }
}

static void cgroup_v1_child_init(cgroup_state_t *state)
{
    unsigned char rand[16];
    urandom(rand, sizeof(rand));
    for (size_t i = 0; i < sizeof(rand); ++i)
        snprintf(&state->v1.child_path[i * 2], 3, "%02hhx", rand[i]);

    _Static_assert(sizeof(state->v1.child_path) - 1 >= 2 * sizeof(rand),
                   "Not enough space for cgroup child path");
}

/* returns a pointer to a global buffer. do not multithread, do not free(). */
static const char *cgroup_v1_build_path(cgroup_state_t *state, const char *dir, const char *file)
{
    static char buf[4096];
    int res;

    if (!state->v1.root_path[0] || !state->v1.child_path[0])
        die_noerrno("cgroups not initialized");

    if (file) {
        res = snprintf(buf, sizeof(buf), "%s/%s/%s/%s", state->v1.root_path, dir, state->v1.child_path, file);
        if (res < 0 || (size_t) res >= sizeof(buf))
            die_noerrno("snprintf");
    } else {
        res = snprintf(buf, sizeof(buf), "%s/%s/%s", state->v1.root_path, dir, state->v1.child_path);
        if (res < 0 || (size_t) res >= sizeof(buf))
            die_noerrno("snprintf");
    }

    return buf;
}

static void cgroup_v1_child_apply_limits(cgroup_state_t *state, const struct config *cfg)
{
    /* set cgroup limits */
    if (cfg->pids.set) {
        if (0 != mkdir(cgroup_v1_build_path(state, "pids", NULL), 0700)) die("mkdir");
        write_value(cgroup_v1_build_path(state, "pids", "pids.max"), cfg->pids.val);
        write_value(cgroup_v1_build_path(state, "pids", "cgroup.procs"), 0);
    }

    if (cfg->memory_limit.set) {
        if (0 != mkdir(cgroup_v1_build_path(state, "memory", NULL), 0700)) die("mkdir");
        write_value(cgroup_v1_build_path(state, "memory", "memory.limit_in_bytes"), cfg->memory_limit.val);
        write_value(cgroup_v1_build_path(state, "memory", "cgroup.procs"), 0);
    }
}

static void cgroup_v1_child_cleanup(cgroup_state_t *state)
{
    /* delete possible cgroups, we ignore errors */
    rmdir(cgroup_v1_build_path(state, "pids", NULL));
    rmdir(cgroup_v1_build_path(state, "memory", NULL));
}


/* unified api */

#define CGROUPS_USAGE_WARNING " (try -cg [12] to select a specific version or -cg 0 to disable cgroups; some resource limits are only effective with cgroups enabled)"
#define cgroup_dispatch(version, v1_expr, v2_expr) \
    do { \
        switch (version) { \
            case CGROUPS_NOT_SUPPORTED: die_noerrno("cgroups not supported" CGROUPS_USAGE_WARNING); break; \
            case CGROUPS_DISABLED:      break; \
            case CGROUPS_V1:            { v1_expr; break; } \
            case CGROUPS_V2:            { v2_expr; break; } \
            default:                    die_noerrno("unknown cgroups version" CGROUPS_USAGE_WARNING); break; \
        } \
    } while (0)

static cgroups_version cgroup_detect_version(cgroup_state_t *state)
{
    /* try to find which version of cgroups this machine supports */
    FILE *file;
    char buf[256];
    char *iterator;
    cgroups_version version = CGROUPS_NOT_SUPPORTED;

    file = fopen("/proc/filesystems", "re");
    if (NULL == file) {
        die("fopen");
    }

    while (NULL != fgets(buf, sizeof(buf), file)) {
        /* process one line: first, skip "nodev" if present, then skip spaces */
        iterator = buf;
        if (0 == strncmp(iterator, "nodev", 5)) {
            iterator += 5;
        }
        iterator += strspn(iterator, " \t");

        /* now iterator refers only to the fs type, pick the highest version */
        if (0 == strcmp(iterator, "cgroup\n") && version < CGROUPS_V1) {
            version = CGROUPS_V1;
        } else if (0 == strcmp(iterator, "cgroup2\n") && version < CGROUPS_V2) {
            /* only use v2 if the controllers are there! */
            /* in some unified systems, we "support" v2, but controllers are tied up in v1 */
            cgroup_v2_mount(state);

            if (cgroup_v2_check_controllers(cgroup_v2_build_path(state, PATH_PARENT, "cgroup.controllers"))) {
                /* can use v2, don't unmount - we would just remount in init() */
                version = CGROUPS_V2;
            } else {
                /* not using v2, unmount */
                cgroup_v2_umount(state);
            }
        }
    }

    if (0 != fclose(file)) {
        die("fclose");
    }

    return version;
}

static void cgroup_init(cgroup_state_t *state)
{
    if (state->version == CGROUPS_UNKNOWN)
        state->version = cgroup_detect_version(state);

    cgroup_dispatch(state->version, cgroup_v1_init(state), cgroup_v2_init(state));
}

static void cgroup_child_init(cgroup_state_t *state)
{
    /* in v2, we already have everything set up at this point */
    cgroup_dispatch(state->version, cgroup_v1_child_init(state), cgroup_v2_child_init(state));
}

static void cgroup_child_apply_limits(cgroup_state_t *state, const struct config *cfg)
{
    cgroup_dispatch(state->version, cgroup_v1_child_apply_limits(state, cfg), cgroup_v2_child_apply_limits(state, cfg));
}

static void cgroup_child_cleanup(cgroup_state_t *state)
{
    /* in v2, termination of the child process automatically removes it from the cgroup */
    cgroup_dispatch(state->version, cgroup_v1_child_cleanup(state), cgroup_v2_child_cleanup(state));
}

/* FIXME: clean up cgroups when ynetd terminates (signal handling?) */

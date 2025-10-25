/*
 * This is ctf-ynetd version 2024.12.31 (based on ynetd 2024.02.17).
 */

#define _GNU_SOURCE
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

#include <unistd.h>
#include <pwd.h>
#include <grp.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <sys/resource.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sched.h>
#include <sys/mount.h>
#include <sys/prctl.h>
#include <sys/vfs.h>
#include <errno.h>

__attribute__((noreturn)) static void version()
{
    printf("This is ctf-ynetd version 2024.12.31.\n"
           "ctf-ynetd was written by members of hxp.\n"
           "Please report bugs to contact@hxp.io.\n");
    exit(0);
}

__attribute__((noreturn)) static void help(int st)
{
    bool tty = isatty(fileno(stdout));

    printf("\n");
    printf("    %sctf-ynetd: ynetd, hardened for CTFs by hxp.%s\n",
            tty ? "\x1b[32m" : "", tty ? "\x1b[0m" : "");
    printf("    -------------------------------------------\n\n");
    printf("    %sinvocation:%s # ynetd [$opts] $cmd\n\n",
            tty ? "\x1b[33m" : "", tty ? "\x1b[0m" : "");

    printf("    %sflags:%s\n",
            tty ? "\x1b[33m" : "", tty ? "\x1b[0m" : "");
    printf("-h              "
            "this help text\n");
    printf("-a $addr        "
            "IP address to bind to (default :: and 0.0.0.0)\n");
    printf("-p $port        "
            "TCP port to bind to (default 1024)\n");
    printf("-u $user        "
            "username (default ctf)\n");
    printf("-d $dir         "
            "working directory (default user's home if -u else current)\n");
    printf("-sh [yn]        "
            "invoke /bin/sh to execute $cmd? (default y)\n");
    printf("-si [yn]        "
            "use socket as stdin? (default y)\n");
    printf("-so [yn]        "
            "use socket as stdout? (default y)\n");
    printf("-se [yn]        "
            "use socket as stderr? (default n)\n");
    printf("-nd [yn]        "
            "set TCP_NODELAY? (default y)\n");
    printf("-np [yn]        "
            "allow gaining privileges e.g. with setuid? (default n)\n");
    printf("-lt $lim        "
            "limit cpu time in seconds (default 3)\n");
    printf("-lm $lim        "
            "limit amount of memory in bytes per process (default %d)\n", 32*1024*1024);
    //printf("-lp $lim        "
    //        "limit number of processes (default unchanged)\n");
    //printf("-rn $val        "
    //        "set process priority (default unchanged)\n");
    printf("-cg $ver        "
            "force ynetd to use this cgroups version (default autodetect, 0 to disable)\n");
    printf("-t $val         "
            "timeout for connection in seconds (default 300)\n");
    printf("-lpid $val      "
            "limit number of processes (default 16)\n");
    printf("-lmem $val      "
            "limit amount of total memory in bytes per connection (default unchanged)\n");
    printf("-pow $bits      "
            "proof-of-work difficulty (default disabled)\n");
    printf("$cmd            "
            "command\n");
    printf("                NOTE: $cmd is executed relative to $dir!\n");
    printf("                      if in doubt, use absolute paths only.\n");
    printf("\n");
    exit(st);
}

#define die(S) do { perror(S); exit(-1); } while (0)
#define die_noerrno(S) do { fprintf(stderr, "%s\n", (S)); exit(-1); } while (0)

struct config {
    struct {
        bool set;
        uid_t uid;
        gid_t gid;
    } ids;

    int family;
    union {
        struct in6_addr ipv6;
        struct in_addr ipv4;
    } addr;
    in_port_t port;

    char *cmd;
    char *dir;
    bool shell;
    bool in, out, err;
    bool tcp_nodelay;
    bool allow_new_privs;
    struct {
        bool set;
        rlim_t lim;
    } cpu, mem, proc;
    struct {
        bool set;
        int val;
    } nice, cgroups;
    struct {
        bool set;
        unsigned int val;
    } timeout;
    struct {
        bool set;
        unsigned long val;
    } pids, memory_limit;
    size_t powbits;
};

static void parse_args(size_t argc, char **argv, struct config *cfg)
{
    struct passwd spw, *pw;
    char pwbuf[0x100];

    /* note: to avoid copying all the strings from argv[] to cfg,
     * we only write pointers to the arguments into cfg. since only
     * main() calls this function, these references are guaranteed
     * to stay valid for the lifetime of the program. */

#define ARG_YESNO(S, L, V) \
    else if (!strcmp(argv[i], (S)) || !strcmp(argv[i], (L))) { \
        if (++i >= argc) \
            help(1); \
        if ((*argv[i] != 'y' && *argv[i] != 'n') || argv[i][1]) \
            help(1); \
        (V) = *argv[i++] == 'y'; \
    }

#define ARG_NUM(S, L, V, P) \
    else if (!strcmp(argv[i], (S)) || !strcmp(argv[i], (L))) { \
        if (++i >= argc) \
            help(1); \
        (V) = strtol(argv[i++], NULL, 10); \
        if (P) \
            * (bool *) (P) = true; \
    }

    for (size_t i = 1; i < argc; ) {
        if (!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")) {
            help(0);
        }
        else if (!strcmp(argv[i], "-v") || !strcmp(argv[i], "--version")) {
            version();
        }
        ARG_YESNO("-sh", "--shell", cfg->shell)
        ARG_YESNO("-si", "--stdin", cfg->in)
        ARG_YESNO("-so", "--stdout", cfg->out)
        ARG_YESNO("-se", "--stderr", cfg->err)
        ARG_YESNO("-nd", "--nodelay", cfg->tcp_nodelay)
        ARG_YESNO("-np", "--allow-new-privs", cfg->allow_new_privs)
        else if (!strcmp(argv[i], "-a") || !strcmp(argv[i], "--addr")) {
            if (++i >= argc)
                help(1);
            if (1 == inet_pton(AF_INET6, argv[i], &cfg->addr.ipv6))
                cfg->family = AF_INET6;
            else if (1 == inet_pton(AF_INET, argv[i], &cfg->addr.ipv4))
                cfg->family = AF_INET;
            else
                die("inet_pton");
            ++i;
        }
        ARG_NUM("-p", "--port", cfg->port, NULL)
        else if (!strcmp(argv[i], "-u") || !strcmp(argv[i], "--user")) {
            if (++i >= argc)
                help(1);
#define SET_IDS(N) \
            do { \
                if (getpwnam_r((N), &spw, pwbuf, sizeof(pwbuf), &pw) || !pw) \
                    die("getpwnam_r"); \
                cfg->ids.uid = pw->pw_uid; \
                cfg->ids.gid = pw->pw_gid; \
                cfg->ids.set = true; \
                if (!cfg->dir) { \
                    /* note: pw->pw_dir is local, so we need to copy it. */ \
                    /* note: ideally we should free() this, but it will \
                     * exist until the parent dies anyway. */ \
                    cfg->dir = strdup(pw->pw_dir); \
                } \
                if (cfg->ids.uid == 0 || cfg->ids.gid == 0) { \
                    puts("Sorry! ctf-ynetd doesn't allow root users."); \
                    exit(1); \
                } \
            } while (false)
            SET_IDS(argv[i++]);
        }
        else if (!strcmp(argv[i], "-d") || !strcmp(argv[i], "--dir")) {
            if (++i >= argc)
                help(1);
            cfg->dir = argv[i++];
        }
        ARG_NUM("-lt", "--limit-time", cfg->cpu.lim, &cfg->cpu.set)
        ARG_NUM("-lm", "--limit-memory", cfg->mem.lim, &cfg->mem.set)
        //ARG_NUM("-lp", "--limit-processes", cfg->proc.lim, &cfg->proc.set)
        //ARG_NUM("-rn", "--renice", cfg->nice.val, &cfg->nice.set)
        ARG_NUM("-cg", "--cgroups", cfg->cgroups.val, &cfg->cgroups.set)
        ARG_NUM("-t", "--timeout", cfg->timeout.val, &cfg->timeout.set)
        ARG_NUM("-lpid", "--limit-pids", cfg->pids.val, &cfg->pids.set)
        ARG_NUM("-lmem", "--limit-total-memory", cfg->memory_limit.val, &cfg->memory_limit.set)
        ARG_NUM("-pow", "--proof-of-work", cfg->powbits, NULL)
        else if (!cfg->cmd) {
            cfg->cmd = argv[i++];
        }
        else {
            help(1);
        }
    }

#undef ARG_YESNO
#undef ARG_NUM

    if (!cfg->cmd)
        help(1);

    /* default to the ctf user */
    if (!cfg->ids.set)
        SET_IDS("ctf");
#undef SET_IDS
}

static int bind_listen(struct config const cfg)
{
    int const one = 1;
    int lsock;
    union {
       struct sockaddr_in6 ipv6;
       struct sockaddr_in ipv4;
    } addr = {0};
    socklen_t addr_len;

    if (0 > (lsock = socket(cfg.family, SOCK_STREAM, 0)))
        die("socket");

    if (setsockopt(lsock, SOL_SOCKET, SO_REUSEADDR, &one, sizeof(one)))
        die("setsockopt");

    switch (cfg.family) {
    case AF_INET6:
        addr.ipv6.sin6_family = cfg.family;
        addr.ipv6.sin6_addr = cfg.addr.ipv6;
        addr.ipv6.sin6_port = htons(cfg.port);
        addr_len = sizeof(addr.ipv6);
        break;
    case AF_INET:
        addr.ipv4.sin_family = cfg.family;
        addr.ipv4.sin_addr = cfg.addr.ipv4;
        addr.ipv4.sin_port = htons(cfg.port);
        addr_len = sizeof(addr.ipv4);
        break;
    default:
        fprintf(stderr, "bad address family?!\n");
        exit(-1);
    }

    if (bind(lsock, (struct sockaddr *) &addr, addr_len))
        die("bind");

    if (listen(lsock, 16))
        die("listen");

    return lsock;
}

__attribute__((noreturn)) static void timeout_handler()
{
    exit(0);
}

static void handle_sigchld(__attribute__((unused)) int sig) {
    pid_t pid;
    /* reap all terminated child processes */
    while ((pid = waitpid((pid_t)(-1), NULL, WNOHANG)) > 0) {
        ;
    }
}

static ssize_t from_hex(unsigned char *r, char const *s)
{
#define DECODE_HEX_CHAR_OR_RETURN_ERROR(T, C) \
    do { \
        if ((C) >= 'a' && (C) <= 'f') (T) = (unsigned) ((C) - 'a' + 10); \
        else if ((C) >= 'A' && (C) <= 'F') (T) = (unsigned) ((C) - 'A' + 10); \
        else if ((C) >= '0' && (C) <= '9') (T) = (unsigned) ((C) - '0'); \
        else return (ssize_t) -1; \
    } while (0)

    size_t l = strlen(s);
    unsigned char nibble;

    /* make sure strlen is even (although macro will return 0 on \0) */
    if (l & 1) return (ssize_t) -1;

    /* convert byte by byte */
    for (size_t i = 0; i < l; ) {
        r[i / 2] = 0;
        DECODE_HEX_CHAR_OR_RETURN_ERROR(nibble, s[i]);
        r[i++ / 2] |= nibble << 4;
        DECODE_HEX_CHAR_OR_RETURN_ERROR(nibble, s[i]);
        r[i++ / 2] |= nibble;
    }

    return (ssize_t) (l / 2);
#undef DECODE_HEX_CHAR_OR_RETURN_ERROR
}

static void urandom(unsigned char *buf, size_t len)
{
    if (0 != getentropy(buf, len)){
        die("getentropy");
    }
}

#include "sha256.c"

static bool proof_of_work(int sock, size_t bits)
{
    size_t const prefix_len = 0x8, suffix_len = 0x8;
    unsigned char prefix[prefix_len], suffix[suffix_len], hash[32];
    char buf[2 * (prefix_len > suffix_len ? prefix_len : suffix_len) + 1];
    mbedtls_sha256_context ctx;

    if (bits > sizeof(hash) * 8) {
        fprintf(stderr, "proof of work: too many bits\n");
        exit(-1);
    }

    urandom(prefix, sizeof(prefix));

    for (size_t i = 0; i < sizeof(prefix); ++i)
        snprintf(buf + 2*i, 3, "%02hhx", prefix[i]);
    dprintf(sock, "please give S such that sha256(unhex(\"%s\" + S)) ends with %zu zero bits (see pow-solver.cpp).\n", buf, bits);

    for (size_t i = 0; i < 2 * suffix_len + 1; ++i) {
        if (1 != read(sock, buf + i, 1))
            die("read");
        if (buf[i] == '\r')
            buf[i--] = 0;   // skip
        else if (buf[i] == '\n') {
            buf[i] = 0;
            break;          // done
        }
        if (i == 2 * suffix_len && buf[i])
            goto bad;       // too long
    }

    ssize_t decoded = from_hex(suffix, buf);
    if (decoded < 0 || (size_t) decoded > sizeof(suffix))
        goto bad;

    mbedtls_sha256_init(&ctx);
    mbedtls_sha256_starts(&ctx, 0);
    mbedtls_sha256_update(&ctx, prefix, sizeof(prefix));
    mbedtls_sha256_update(&ctx, suffix, (size_t) decoded);
    mbedtls_sha256_finish(&ctx, hash);
    mbedtls_sha256_free(&ctx);

    for (size_t i = 0; i < bits / 8; ++i)
        if (hash[sizeof(hash) - 1 - i])
            goto bad;
    for (size_t k = bits / 8, i = 0; i < bits % 8; ++i)
        if (hash[sizeof(hash) - 1 - k] & 1 << i)
            goto bad;

    return true;

bad:
    dprintf(sock, "nope\n");
    return false;
}

/* unified api for cgroups v1 and v2 */
#include "cgroups.c"
static cgroup_state_t cgroup_state = { .version = CGROUPS_UNKNOWN };

static void handle_connection(struct config const cfg, int sock)
{
    struct rlimit rlim;
    pid_t pid;
    int const one = 1;

    cgroup_child_init(&cgroup_state);

    if (cfg.tcp_nodelay) {
        if (setsockopt(sock, IPPROTO_TCP, TCP_NODELAY, &one, sizeof(one)))
            die("setsockopt");
    }

    /* set resource limits */
    if (cfg.cpu.set) {
        rlim.rlim_cur = rlim.rlim_max = cfg.cpu.lim;
        if (0 > setrlimit(RLIMIT_CPU, &rlim))
            die("setrlimit");
    }
    if (cfg.mem.set) {
        rlim.rlim_cur = rlim.rlim_max = cfg.mem.lim;
#ifndef RLIMIT_AS
        if (0 > setrlimit(RLIMIT_DATA, &rlim))
#else
        if (0 > setrlimit(RLIMIT_AS, &rlim))
#endif
            die("setrlimit");
    }
    if (cfg.proc.set) {
        rlim.rlim_cur = rlim.rlim_max = cfg.proc.lim;
        if (0 > setrlimit(RLIMIT_NPROC, &rlim))
            die("setrlimit");
    }

    /* renice */
    if (cfg.nice.set && setpriority(PRIO_PROCESS, 0, cfg.nice.val))
        die("setpriority");

    /* make next process PID 1 */
    if (0 != unshare(CLONE_NEWPID | CLONE_NEWNS)) {
        die("unshare");
    }

    if (-1 == (pid = fork())) {
        die("fork");
    }

    if (pid) {
        /* parent - connection */

        while (-1 != wait(NULL)) {
            ;
        }

        /* clean up the child's cgroups */
        cgroup_child_cleanup(&cgroup_state);

        exit(0);
    }

    /* child - pid 1 */

    if (1 != getpid()) {
        exit(1);
    }

    /* set cgroup limits */
    cgroup_child_apply_limits(&cgroup_state, &cfg);

    /* mount /proc for the new PID namespace */
    if ((0 != mount("none", "/", NULL, MS_REC|MS_PRIVATE, NULL)) ||
        (0 != mount("none", "/proc", NULL, MS_REC|MS_PRIVATE, NULL)) ||
        (0 != mount("proc", "/proc", "proc", MS_NOSUID|MS_NOEXEC|MS_NODEV, NULL))) {
        die("mount");
    }

    if (-1 == (pid = fork())) {
        die("fork");
    }

    if (pid) {
        /* parent - pid 1 */

        /* register timeout handler */
        if (cfg.timeout.set) {
            signal(SIGALRM, timeout_handler);
            alarm(cfg.timeout.val);
        }

        while (-1 != wait(NULL)) {
            ;
        }
        exit(0);
    }

    /* child */

    /* drop privileges */
    if (cfg.ids.set) {
        if (setgroups(0, NULL))
            die("setgroups");
        if (setgid(cfg.ids.gid))
            die("setgid");
        if (setuid(cfg.ids.uid))
            die("setuid");
    }

    /* change working directory */
    if (cfg.dir && chdir(cfg.dir))
        die("chdir");

    if (cfg.powbits && !proof_of_work(sock, cfg.powbits))
        exit(0);

    /* duplicate socket to stdio */
    if (cfg.in && fileno(stdin) != dup2(sock, fileno(stdin)))
        die("dup2");
    if (cfg.out && fileno(stdout) != dup2(sock, fileno(stdout)))
        die("dup2");
    if (cfg.err && fileno(stderr) != dup2(sock, fileno(stderr)))
        die("dup2");
    if (close(sock))
        die("close");

    /* FIXME does nobody care about the environment? */

    /* execute command */
    if (cfg.shell) {
        execle("/bin/sh", "sh", "-c", cfg.cmd, NULL, NULL);
        die("execle");
    }
    else {
        /* FIXME support more arguments? */
        execle(cfg.cmd, cfg.cmd, NULL, NULL);
        die("execle");
    }
}

int main(int argc, char **argv)
{
    pid_t pid;
    int lsock, sock;
    struct sigaction sigact;

    /* configuration options */
    struct config cfg = {
        .ids = {.set = false},

        .family = AF_INET6,
        .addr = {.ipv6 = in6addr_any},
        .port = 1024,

        .cmd = NULL,
        .dir = NULL,
        .shell = true,
        .in = true, .out = true, .err = false,
        .tcp_nodelay = true,
        .allow_new_privs = false,
        .cpu = {.set = true, .lim = 3}, .mem = {.set = true, .lim = 32*1024*1024}, .proc = {.set = false},
        .nice = {.set = false},
        .cgroups = {.set = false},
        .timeout = {.set = true, .val = 300},
        .pids = {.set = true, .val = 16}, .memory_limit = {.set = false},
        .powbits = 0,
    };

    /* "parse" arguments */
    parse_args(argc, argv, &cfg);

    /* prevent setuid binaries from gaining rights */
    if (!cfg.allow_new_privs && 0 != prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        die("prctl");
    }

    /* set up cgroups */
    if (cfg.cgroups.set)
        cgroup_state.version = cfg.cgroups.val; /* otherwise autodetect */
    cgroup_init(&cgroup_state);

    /* make sure dead children are cleaned up properly */
    memset(&sigact, 0, sizeof(sigact));
    sigact.sa_flags = SA_RESTART | SA_NOCLDSTOP;
    sigact.sa_handler = &handle_sigchld;
    if(sigemptyset(&sigact.sa_mask))
        die("sigemptyset");

    if (sigaction(SIGCHLD, &sigact, NULL))
        die("sigaction");

    /* set up listening socket */
    lsock = bind_listen(cfg);

    /* accept loop */
    while (1) {

        if (0 > (sock = accept(lsock, NULL, NULL)))
            continue;

        if ((pid = fork())) {
            /* parent */
            /* note: if the fork failed, we just drop the connection
             * and continue as usual, so we don't catch that case. */
            if (close(sock))
                die("close");
            continue;
        }

        /* child - connection */
        if (close(lsock))
            die("close");

        /* detach from terminal */
        if (0 > setsid())
            die("setsid");

        handle_connection(cfg, sock);
    }
}

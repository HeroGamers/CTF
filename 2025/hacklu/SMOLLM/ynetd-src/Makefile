all: CFLAGS ?= -O2 -Wl,-s \
               -Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now,-z,separate-code -fpic -pie -D_FORTIFY_SOURCE=3 -fstack-protector-all -fno-plt -fstack-clash-protection -fcf-protection
all: CFLAGS += -std=c11 -pedantic -Wall -Wextra -DNDEBUG
all: ynetd

debug: CFLAGS ?= -O0 -g \
                 -fsanitize=address -static-libasan \
                 -Wl,-z,relro,-z,now -fpic -pie -fstack-protector-all
debug: CFLAGS += -std=c11 -pedantic -Wall -Wextra -Werror
debug: ynetd

test: CFLAGS ?= -O2 -Wl,-s \
               -Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now -fpic -pie -D_FORTIFY_SOURCE=3 -fstack-protector-all -fno-plt -fstack-clash-protection -fcf-protection \
               -fsanitize=address -static-libasan \
               -fsanitize=undefined -static-libubsan \
               -fno-sanitize-recover=all
test: CFLAGS += -std=c11 -pedantic -Wall -Wextra -DNDEBUG
test: ynetd

ynetd: ynetd.c cgroups.c sha256.c
	$(CC) \
		$(CFLAGS) \
		ynetd.c \
		-o ynetd

pow-solver: pow-solver.cpp
	g++ \
		-std=c++11 -pedantic -Wall -Wextra -Werror \
		-O2 -funroll-loops \
		pow-solver.cpp \
		-lcrypto -lpthread \
		-o pow-solver

clean:
	rm -f pow-solver ynetd


#!/bin/bash

# TL;DR: just `./plzhalp.sh`, but please read on; you might learn something.


# WHY WON'T THIS THING RUN?!
#
# This binary most likely won't run on your system (otherwise: what are you, a
# wizard?):
#
#   user@localhost$ ./main
#   bash: ./main: cannot execute: required file not found
#
# You might try to investigate with `strace`:
#
#   user@localhost$ strace ./main
#   execve("./main", ["./main"], 0x7ffe2a4f4300 /* 47 vars */) = -1 ENOENT (No such file or directory)
#   strace: exec: No such file or directory
#   +++ exited with 1 +++
#
# No bueno.
#
# The problem here is that you don't have the interpreter that the binary needs.
# Wait, an interpreter? This is a binary, it's not interpreted! I hear you
# exclaim.
#
# Well, yes.  But the Linux kernel uses the term "interpreter" a bit more
# broadly than you may be used to.  Mostly (as in practically always) a
# program's interpreter is the dynamic linker.  It is responsible for loading
# libraries (I hear libc is very popular) and resolving symbols in them.
#
# The way it works is that the kernel loads *both* your binary and its
# interpreter (which is why `execve` returns `-ENOENT`) then hands over control
# to *the interpreter*.  See, it's right there in `man execve` (emphasis mine):
#
#   ...
#     ENOENT The file pathname or a script _or ELF interpreter_ does not exist.
#   ...
#
# If you're interested in the details of how programs are actually loaded and
# run on Linux see:
#
#   https://github.com/torvalds/linux/blob/master/fs/binfmt_elf.c
#
# This reminds me of a neat trick which, sadly, isn't that useful anymore with
# the rise of personal computers and all.  Bear with me.
#
# Anyway, it went like this: You would like `root` on your university's server,
# so you write a program that installs a backdoor.  Now you just need `root` to
# run your program.  So you write another program and set its interpreter to the
# first program you wrote.  Then you whine to BOFH that the program you wrote
# for the homework exercises in `Advanced Quantum Algorithms` complains about a
# version mismatch in `libquantum.so.28` or something.  The BOFH goes to
# investigate by running
#
#   root@mainframe# ldd /home/hxg183/advanced_quantum_algorithms/whyyounowork
#
# Bam! you're in!
#
# But why? you ask.  What does `ldd` do? I ask you back.  From `man ldd`:
#
#   ...
#   In the usual case, ldd invokes the standard dynamic linker (see ld.so(8))
#   with the LD_TRACE_LOADED_OBJECTS environment variable set to 1.
#   ...
#   Be aware that in some circumstances (e.g., where the program specifies an
#   ELF interpreter other than ld-linux.so), some versions of ldd may attempt to
#   obtain the dependency information by attempting to directly execute the
#   program, which may lead to the execution of whatever code is defined in the
#   program's ELF interpreter, ...
#
# Try it for yourself:
#
#   user@localhost$ LD_TRACE_LOADED_OBJECTS=1 /bin/sh
#   linux-vdso.so.1 (0x00007fbd5cef8000)
#   libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fbd5ccf4000)
#   /lib64/ld-linux-x86-64.so.2 (0x00007fbd5cefa000)
#
# Where was I?  Oh yeah, you're playing a very important CTF and you just want
# to get that flag (før det' for sent).  Let's see what the interpreter of
# `main` is:
#
#   user@localhost$ readelf --program-headers main
#   ...
#     Type           Offset             VirtAddr           PhysAddr
#                    FileSiz            MemSiz              Flags  Align
#   ...
#     INTERP         0x0000000000000318 0x0000000000000318 0x0000000000000318
#                    0x0000000000000019 0x0000000000000019  R      0x1
#         [Requesting program interpreter: /lib/ld-musl-x86_64.so.1]
#   ...
#
# So the path to the interpreter is located at offset 0x318 in the file.  Let's
# change that to `./ld-musl-x86_64.so.1`, shall we?:

dd \
    bs=1 \
    conv=notrunc \
    if=<(echo -ne "./ld-musl-x86_64.so.1\0") \
    of=./main oseek=$((0x318))

# Maybe surprisingly this is enough to make the program run.  This is because
# MUSL libc and ld.so is actually the same file (see for yourself).  If the
# program had used e.g. the GNU toolchain we would have had to let the linker
# know where to find libc too.  The interface between an ELF file and its
# dynamic linker is the `DYNAMIC` section (also listed in the program headers).
# Let's see:
#
#   user@localhost$ readelf --dynamic main
#   Dynamic section at offset 0x2d88 contains 24 entries:
#     Tag        Type                         Name/Value
#    0x0000000000000001 (NEEDED)             Shared library: [libc.musl-x86_64.so.1]
#    0x000000000000000c (INIT)               0x1000
#    0x000000000000000d (FINI)               0x157d
#    0x0000000000000019 (INIT_ARRAY)         0x3d50
#    0x000000000000001b (INIT_ARRAYSZ)       8 (bytes)
#    0x000000000000001a (FINI_ARRAY)         0x3d58
#    0x000000000000001c (FINI_ARRAYSZ)       8 (bytes)
#    0x000000006ffffef5 (GNU_HASH)           0x390
#    0x0000000000000005 (STRTAB)             0x5d8
#   ...
#
# From `man ld.so` we can read that the dynamic linker looks for libraries in
# `DT_RUNPATH` if such an entry is present.  But this ELF doesn't have such an
# entry so setting it is a bit more tricky than overwriting the dynamic linker.
# Let me ask you: what good have destructors done for you lately? Exactly.
# Let's nuke `DT_FINI`!
#
# But hol'up.  We need to point to a string in the dynamic string table (at
# offset 0x5d8).  Let's overwrite `_fini`, fuck that guy:

dd \
    bs=1 \
    conv=notrunc \
    if=<(echo -ne ".\0") \
    of=./main oseek=$((0x628))

# A quick look with `readelf --dyn-syms` should confirm that it's byebye to
# `_fini`.  Finally we install `DT_RUNPATH` (which is 29 = 0x1d, see
# `/usr/include/elf.h`):

dd \
    bs=1 \
    conv=notrunc \
    if=<(echo -ne "\x1d\0\0\0\0\0\0\0"; echo -ne "\x50\0\0\0\0\0\0\0") \
    of=./main oseek=$((0x2da8))

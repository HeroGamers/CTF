# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.24

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/hw3a.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/hw3a.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/hw3a.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/hw3a.dir/flags.make

CMakeFiles/hw3a.dir/hw-3a.c.o: CMakeFiles/hw3a.dir/flags.make
CMakeFiles/hw3a.dir/hw-3a.c.o: /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/hw-3a.c
CMakeFiles/hw3a.dir/hw-3a.c.o: CMakeFiles/hw3a.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/hw3a.dir/hw-3a.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT CMakeFiles/hw3a.dir/hw-3a.c.o -MF CMakeFiles/hw3a.dir/hw-3a.c.o.d -o CMakeFiles/hw3a.dir/hw-3a.c.o -c /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/hw-3a.c

CMakeFiles/hw3a.dir/hw-3a.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/hw3a.dir/hw-3a.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/hw-3a.c > CMakeFiles/hw3a.dir/hw-3a.c.i

CMakeFiles/hw3a.dir/hw-3a.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/hw3a.dir/hw-3a.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/hw-3a.c -o CMakeFiles/hw3a.dir/hw-3a.c.s

# Object files for target hw3a
hw3a_OBJECTS = \
"CMakeFiles/hw3a.dir/hw-3a.c.o"

# External object files for target hw3a
hw3a_EXTERNAL_OBJECTS =

hw3a: CMakeFiles/hw3a.dir/hw-3a.c.o
hw3a: CMakeFiles/hw3a.dir/build.make
hw3a: CMakeFiles/hw3a.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable hw3a"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/hw3a.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/hw3a.dir/build: hw3a
.PHONY : CMakeFiles/hw3a.dir/build

CMakeFiles/hw3a.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/hw3a.dir/cmake_clean.cmake
.PHONY : CMakeFiles/hw3a.dir/clean

CMakeFiles/hw3a.dir/depend:
	cd /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug /mnt/d/Projekter/Git/DTU/HKUST/COMP-2633/hw-3-a-c/cmake-build-debug/CMakeFiles/hw3a.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/hw3a.dir/depend


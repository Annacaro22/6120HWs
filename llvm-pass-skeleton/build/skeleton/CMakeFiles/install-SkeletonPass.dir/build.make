# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

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
CMAKE_SOURCE_DIR = /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build

# Utility rule file for install-SkeletonPass.

# Include any custom commands dependencies for this target.
include skeleton/CMakeFiles/install-SkeletonPass.dir/compiler_depend.make

# Include the progress variables for this target.
include skeleton/CMakeFiles/install-SkeletonPass.dir/progress.make

skeleton/CMakeFiles/install-SkeletonPass:
	cd /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build/skeleton && /usr/bin/cmake -DCMAKE_INSTALL_COMPONENT="SkeletonPass" -P /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build/cmake_install.cmake

install-SkeletonPass: skeleton/CMakeFiles/install-SkeletonPass
install-SkeletonPass: skeleton/CMakeFiles/install-SkeletonPass.dir/build.make
.PHONY : install-SkeletonPass

# Rule to build all files generated by this target.
skeleton/CMakeFiles/install-SkeletonPass.dir/build: install-SkeletonPass
.PHONY : skeleton/CMakeFiles/install-SkeletonPass.dir/build

skeleton/CMakeFiles/install-SkeletonPass.dir/clean:
	cd /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build/skeleton && $(CMAKE_COMMAND) -P CMakeFiles/install-SkeletonPass.dir/cmake_clean.cmake
.PHONY : skeleton/CMakeFiles/install-SkeletonPass.dir/clean

skeleton/CMakeFiles/install-SkeletonPass.dir/depend:
	cd /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/skeleton /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build/skeleton /home/annabelbaniak/Documents/SP25/Compilers/llvm-pass-skeleton/build/skeleton/CMakeFiles/install-SkeletonPass.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : skeleton/CMakeFiles/install-SkeletonPass.dir/depend


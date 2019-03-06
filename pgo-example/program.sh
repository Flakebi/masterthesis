#!/usr/bin/env bash
set -e

# Compile with static optimizations
clang++ -O2 program.cpp -o program-nopgo

# Compile with instrumentation
clang++ -O2 -fprofile-instr-generate program.cpp -o program
# Run program
./program input.txt
# Get row profile data into the right format
llvm-profdata merge -output=program.profdata default.profraw
# Build with pgo
clang++ -O2 -fprofile-instr-use=program.profdata program.cpp -o program-pgo

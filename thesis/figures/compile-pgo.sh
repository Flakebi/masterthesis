# Compile with instrumentation
clang++ -O2 -fprofile-instr-generate program.cpp -o program
# Run program
./program input.txt
# Transform raw profile data into the right format
llvm-profdata merge -output=program.profdata default.profraw
# Compile again with pgo
clang++ -O2 -fprofile-instr-use=program.profdata program.cpp -o program-pgo

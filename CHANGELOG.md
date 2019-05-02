# 2019-04-29 – 2019-05-05
- Passing PGO data to LLVM works but is in the wrong format
- Set filename from environment variable and include pipeline id
- Fix written profiling data
- Learn profile data format: CounterPtr inside data section is GPU address (relocation), in profraw header is CPU address (section start)

# 2019-04-22 – 2019-04-28
- Writing some profile data works but creates invalid files
- Upstream order independent section loading in PAL
- Add some text about ELF to the background
- Link PGO runtime library into PAL
- Look at how LLVM writes out PGO data

# 2019-04-15 – 2019-04-21
- Add notes to implementation part of the thesis
- DotA performance test: RADV: 120-130 fps, AMDVLK: 120 fps, AMDVLK (with PGO): 10 fps
- Relocations work, getting PGO counters
- Load more sections (without relocations)
- Start with relocation code

# 2019-04-08 – 2019-04-14
- Look into using lld as linker
- Fix 32-bit counters
- Use atomic counters and reduce to 32-bit (not completely working)
- Read ISA
- Print shader data segment
- Read more PAL code

### 2019-04-01 – 2019-04-07

# 2019-03-25 – 2019-03-31
- Correct introduction again
- Start reading more PAL code
- Fix sh_link in PAL
- Read ELF code in PAL
- Write about LLVM instrumentation for counting basic block executions

# 2019-03-18 – 2019-03-24
- Write software part of introduction
- Successfully enable PGO when compiling (though it obviously crashes when running)
- Non-working driver issue: Find linker error
- Look at LLVM pgo infrastructure
- Look at LLVM amdgpu infrastructure
- Test amdvlk driver

# 2019-03-11 – 2019-03-17
- Build amdvlk
- Add section about branching
- Add Nicolai’s corrections
- Read about llvm instruction scheduling and branch weights/probabilities to finally find linearization
- Start with software part of GPUs
- Improve optimization list
- Improve introduction

# 2019-03-04 – 2019-03-10
- Search some literature
- Start writing introduction

# 2019-01-29
Continue reading GCN ISA

# 2019-01-28
Read about derivatives in shaders for texture lookups and how that works with branches: Not possible in branches, needs to be fetched before (or explicitely specify derivative).

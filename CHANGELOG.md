# 2019-03-18 – 2019-03-24
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

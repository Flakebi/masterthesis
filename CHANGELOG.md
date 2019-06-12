# 2019-06-10 – 2019-06-16
- Using wave, normal instrumentation changed 1 shader in Dota (and linearization), wave-late changed more
- init_exec intrinsic does not work for some reason
- Write a script to automate things
- Cleanup code and introduce runtime options
- Plan finding uniform values
- Try to use gpuvis, overrides LD_LIBRARY_PATH and other things

# 2019-06-03 – 2019-06-09
- Create PGO analysis pass to find 0-counts
- LTTng: Can trace things, but how can it trace frames?
- Install games
- gpuvis: Supports Tracing a few frames but not continuously
- Benchmark Ashes
- Ashes never destroys pipelines → implement dumping every 10 seconds
- Create script to parse Ashes of the Singularity output files
- More Dota benchmarks

# 2019-05-27 – 2019-06-02
- OCAT runs on Windows only
- Steam claims negative fps, Ashes writes result to /mnt/bigdata/Dateien/Programme/Steam/steamapps/compatdata/507490/pfx/drive_c/users/steamuser/My Documents/My Games/Ashes of the Singularity - Escalation
- Start Ashes of the Singularity with proton from command line
- vkmark: No difference in pipelines
- Ask about VComputeBench
- 5 runs Dota benchmark: 11:54, everywhere 51.1 fps (89.7 for lower graphic settings)
- Increment counters only once per wave, increases fps while instrumenting to 35 in benchmark
- Scripted Dota benchmark, needs 6:48, 96 fps without PGO, 97.5 with PGO
- Problems
	- RGP always claims things are CPU limited, but it makes things run slower itself
	- Dota runs slow until reboot (again)
	- Dota demos have less fps (96) than real game (120)
- Run RGP, renderdoc, their integration is not working
- More Dota benchmarks, also with custom scene: 98 fps without PGO, 95 with PGO

# 2019-05-20 – 2019-05-26
- Benchmark Dota, no change in performance with PGO on the phoronix example
- Dota is (subjectively) 5–10 fps faster with PGO, changes are mostly basic block ordering
- VulkanSponza is (subjectively) 0.5 fps faster with modified SSAO shader and PGO
- Try to apply PGO intrumentation and usage after StructurizeCFG pass but function hashes do not match
- Shader differenzes for VulkanSponza with/without PGO: None, except text.hot/text.unlikely section
- Dota has the same 58 fps with PGO as without and with RADV
- Mark export instruction as convergent and don’t apply ControlHeightReduction

# 2019-05-13 – 2019-05-19
- Get Radeon GPU Profiler to start, needs libncurses from Ubuntu 18.04
- Dota is (subjectively) 10 fps slower with PGO
- Create pass to merge export instructions
- Add figures to GPU background
- Try to (ab)use llpcSpirvLowerGlobalPass to merge export instructions

# 2019-05-06 – 2019-05-12
- VulkanSponza is (subjectively) 0.5 fps slower with modified SSAO shader and PGO
- Was a problem of bfd, works with gold
- PGO does not work in release mode: IR flag is not set
- Disabling ControlHeightReduction works for Dota
- Narrowed down to ControlHeightReduction pass in LLVM
- Manually patch code, problem seem to be multiple exp instructions
- Narrow down to pixel shader by replacing code
- Find rogue pipeline with binary search
- Try to play Dota with PGO – crashes
- Create script to convert profraw to profdata files
- Fix bug allowing only one file to be written

# 2019-04-29 – 2019-05-05
- Improve PAL, not hardcoding single code and data sections
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
- Dota performance test: RADV: 120-130 fps, AMDVLK: 120 fps, AMDVLK (with PGO): 10 fps
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

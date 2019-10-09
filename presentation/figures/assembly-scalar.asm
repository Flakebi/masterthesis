...
; in_value is in v1
; int a is in s0

v_mul_lo_i32 v0, s0, v1
s_mul_i32 s0, s0, 3
v_mov_b32_e32 v2, 0
v_mov_b32_e32 v1, s0
exp mrt0 v1, v0, v2, off done vm
s_endpgm

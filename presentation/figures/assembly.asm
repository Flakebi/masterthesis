...
; in_value is in v1
; int a is in v0

v_mov_b32_e32 v2, 0
v_mul_lo_i32 v1, v0, v1
v_mul_u32_u24_e32 v0, 3, v0
exp mrt0 v0, v1, v2, off done vm
s_endpgm

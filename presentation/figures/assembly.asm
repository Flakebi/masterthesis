	; v0 == 0
	v_cmp_neq_f32_e32 vcc, 0, v0
	s_and_saveexec_b64 s[0:1], vcc
	s_cbranch_execz flip_mask
	; then-branch
flip_mask:
else:
	; else-branch
endif:
	s_endpgm

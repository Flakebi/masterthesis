void main() {
	float a;
	if (in_value < 0.5)
		a = 2.0;
	else
		a = 0.0;

	float r = a * 0.5;
	float g = a * in_value;
	out_color = vec3(r, g, 0.0);
}

layout(location = 0) in float in_value;
layout(location = 1) out ivec3 out_color;
void main() {
    int a;
    if (in_value < 0.5)
        a = 2;
    else
        a = 0;

    int r = a * 3;
    int g = a * int(in_value);
    out_color = ivec3(r, g, 0);
}

#version 120

varying vec4 v_fg_color;
varying vec4 v_bg_color;
varying float v_radius;
varying float v_linewidth;
varying float v_antialias;

float calc(vec2 P, float size);

void main()
{
    float size = v_radius + 2 * (v_linewidth + v_antialias);
    float t = v_linewidth / 2.0 - v_antialias;
    float r = calc(gl_PointCoord, size);

    float d = abs(r) - t;
    float r_max = (v_linewidth / 2.0 + v_antialias);
    if(r > r_max) // Outside circle
        discard;
    else if(d < 0.0) // Border
       gl_FragColor = v_fg_color;
    else // Inner part
    {
        float alpha = d / v_antialias;
        alpha = exp(-alpha * alpha);
        if (r <= 0)
            gl_FragColor = mix(v_bg_color, v_fg_color, alpha);
        else
            gl_FragColor = vec4(v_fg_color.rgb, alpha * v_fg_color.a);
    }
}

float calc(vec2 P, float size)
{
    vec2 someVector = (P.xy - vec2(0.5, 0.5));
    float r = length(someVector) * size;
    r -= (v_radius / 2);
    return r;
}
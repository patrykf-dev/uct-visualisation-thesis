#version 120

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

attribute float a_x;
attribute float a_y;
attribute float a_width;
attribute vec4  a_color;

varying vec4 v_color;

void main (void)
{
    v_color = a_color;
    vec4 position = vec4(a_x, a_y, 1.0, 1.0);
    gl_Position = u_projection * u_view * u_model * position;
}
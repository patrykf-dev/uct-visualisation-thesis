uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;

attribute vec3 a_position;
attribute vec4 a_fg_color;
attribute vec4 a_bg_color;
attribute float a_size;
attribute float a_linewidth;

void main(){
    gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.);
}
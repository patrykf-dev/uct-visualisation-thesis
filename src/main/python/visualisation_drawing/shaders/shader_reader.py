class ShaderReader:
    def __init__(self):
        self.vertives_vshader = self._get_vertices_vshader()
        self.vertives_fshader = self._get_vertices_fshader()
        self.edges_vshader = self._get_edges_vshader()
        self.edges_fshader = self._get_edges_fshader()

    def _get_edges_fshader(self):
        return """ 
            #version 120

            varying vec4 v_color;
            
            void main()
            {
                gl_FragColor = v_color;
            }
            """

    def _get_vertices_fshader(self):
        return """
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
        """

    def _get_edges_vshader(self):
        return """
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
        """

    def _get_vertices_vshader(self):
        return """
        #version 120

        uniform mat4 u_model;
        uniform mat4 u_view;
        uniform mat4 u_projection;
        uniform float u_antialias;
        uniform float u_radius_multiplier;
        
        attribute vec3  a_position;
        attribute vec4  a_fg_color;
        attribute vec4  a_bg_color;
        attribute float a_linewidth;
        attribute float a_radius;
        
        varying vec4 v_fg_color;
        varying vec4 v_bg_color;
        varying float v_radius;
        varying float v_linewidth;
        varying float v_antialias;
        
        void main (void) {
            v_radius = a_radius * u_radius_multiplier;
            v_linewidth = a_linewidth;
            v_antialias = u_antialias;
            v_fg_color  = a_fg_color;
            v_bg_color  = a_bg_color;
            gl_Position = u_projection * u_view * u_model * vec4(a_position, 1.0);
            gl_PointSize = v_radius + 2 * (v_linewidth + 1.5 * v_antialias);
        }
        """

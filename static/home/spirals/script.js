const fractals = document.querySelector('#fractals');
gsap.registerPlugin(ScrollTrigger);
gsap.to('#fractals', {
  value: 100,
  ease: 'none',
  scrollTrigger: { scrub: 0.3 }
});
const glsl = x => x;

const frag = glsl`
    precision highp float;
    uniform float time;
    uniform float width;
    uniform float height;
    uniform float fractals;
    
    const float PI = 3.141592654;
    const float DEG = PI / 180.0;
    
    vec2 coords() {
      float vmin = min(width, height);
      return vec2((gl_FragCoord.x - width * .5) / vmin,
                  (gl_FragCoord.y - height * .5) / vmin);
    }
    
    vec2 rotate(vec2 p, float a) {
      return vec2(p.x * cos(a) - p.y * sin(a),
                  p.x * sin(a) + p.y * cos(a));
    }
    
    vec2 repeat(in vec2 p, in vec2 c) {
      return mod(p, c) - 0.5 * c;
    }
    
    // https://iquilezles.org/www/articles/distfunctions2d/distfunctions2d.htm
    float circle(in vec2 p, in vec2 pos, float radius) {
      return length((p - pos)) - radius;
    }
    
    float distanceField(vec2 p) {
      float d = 10000.0; 
      float l = length(coords());
      for (int i = 4; i < 40; i++) {
        float j = 1. + float(i) * 1.5;
        vec2 point = vec2(cos(j * time * .5 * DEG + j) * j, sin(j * time * .5 * DEG + j) * j) * .08;
        d = min(d, circle(p, point, j * .018));
      }
      return d;
    }
    
    vec3 shade(in vec2 p, in vec2 p0)
    {
      float l0 = length(p0);
      vec3 background = vec3(.4, .3, .7);
      vec3 foreground = vec3(.89, .56, .09 + .2 * l0);
      float sdf = distanceField(p);
      foreground *= 3.5 * max(0., .1 - sdf * 2.);
      if (sdf < 0.0) {
        return foreground;
      }  
    
      vec3 col = background;
      float l = length(p);
    
      // repeating lines
      col *= 0.8 + 0.05*cos(1.*sdf - time * .5);
    
      if (sdf > 0.0 && sdf < sqrt(l) * .01) {
        // anti alias
        return mix(col, foreground, .9);
      }
      return col;
    }
    
    
    void main () {
      vec2 p0 = coords();
      float zoom = 7.;
      vec2 p1 = rotate(p0 * zoom, -time * DEG);
      float l = length(p1);
      float a = atan(p1.y, p1.x);
      float f = 100.;
      float g = mix(f / l, f / log(1. + l), fractals / 100.);
      vec2 p2 = vec2(cos(a), sin(a)) * g;
      vec2 p3 = rotate(repeat(p2, vec2(11.67)), -time  * DEG);
      vec3 col = shade(p3, p0) * clamp(pow(length(p0), 2. - fractals / 400.), 0., 1.);
      gl_FragColor = vec4(col, 1.0);
    }
`;

const vert = glsl`
    precision mediump float;
    attribute vec2 position;
    
    void main () {
      gl_Position = vec4(position, 0, 1.0);
    }
`;




let texture = null;

const glea = new GLea({
  shaders: [
    GLea.fragmentShader(frag),
    GLea.vertexShader(vert)
  ],
  buffers: {
    'position': GLea.buffer(2, [1, 1,  -1, 1,  1,-1,  -1,-1])
  }
}).create();

function loop(time) {
  const { gl } = glea;
  glea.clear();
  glea.uni('width', glea.width);
  glea.uni('height', glea.height);
  glea.uni('time', time * .005);
  glea.uni('fractals', parseFloat(fractals.value));
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  requestAnimationFrame(loop);
}

function setup() {
  const { gl } = glea;
  window.addEventListener('resize', () => {
    glea.resize();
  });
  loop(0);
}

setup();
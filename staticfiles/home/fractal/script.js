let image, canvas, tex, ctx, rect, uscale, uzoom, zoom, gl, iW, iH,
    init = true,
    touched = false,
    timeout,
    m = [0, 0],
    slowX = 0;

window.onload = start;
window.onresize = resize;
window.addEventListener('mousemove', mouse);
window.addEventListener('touchmove', mouse);

function resize() {
  iW = document.documentElement.clientWidth;
  iH = document.documentElement.clientHeight;

  let sq = iW > iH ? iW : iH;

  canvas.width = canvas.height = sq;
  canvas.style.top = ((iH - canvas.height) / 2) + 'px';
  canvas.style.left = ((iW - canvas.width) / 2) + 'px';

  let max = gl.getParameter(gl.MAX_TEXTURE_SIZE);
  if (max < image.height) {
    tex.width = Math.floor(image.width * (max / image.height));
    tex.height = max;
  } else {
    tex.width = image.width;
    tex.height = image.height;
  }

  rect = canvas.getBoundingClientRect();
  gl.viewport(0, 0, canvas.width, canvas.height);
}

function main() {
  const vshader = load_shader('vertex-shader', gl.VERTEX_SHADER);
  const fshader = load_shader('fragment-shader', gl.FRAGMENT_SHADER);

  gl.program = gl.createProgram();
  gl.attachShader(gl.program, vshader);
  gl.attachShader(gl.program, fshader);
  gl.linkProgram(gl.program);
  gl.useProgram(gl.program);

  let acoords = gl.getAttribLocation(gl.program, 'a_coords');

  uscale = gl.getUniformLocation(gl.program, 'u_scale');
  uzoom = gl.getUniformLocation(gl.program, 'u_zoom');

  let texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);

  with (gl) {
    texParameteri(TEXTURE_2D, TEXTURE_WRAP_S, CLAMP_TO_EDGE);
    texParameteri(TEXTURE_2D, TEXTURE_WRAP_T, CLAMP_TO_EDGE);
    texParameteri(TEXTURE_2D, TEXTURE_MIN_FILTER, NEAREST);
    texParameteri(TEXTURE_2D, TEXTURE_MAG_FILTER, NEAREST);
  }

  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, tex);
  gl.uniform1f(uscale, tex.width / tex.height / 10);

  const buffer = gl.createBuffer();

  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.enableVertexAttribArray(acoords);
  gl.vertexAttribPointer(acoords, 2, gl.FLOAT, false, 0, 0);

  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
      -1.0, -1.0,
       1.0, -1.0,
      -1.0,  1.0,
      -1.0,  1.0,
       1.0, -1.0,
       1.0,  1.0
  ]), gl.STATIC_DRAW);

  if (init) {
    init = false;
    loop();
  }

  touched = false;
  clearTimeout(timeout);
  demo();

}

function load_shader(el, type) {
  const script = document.getElementById(el);
  const shader = gl.createShader(type);

  gl.shaderSource(shader, script.text);
  gl.compileShader(shader);

  return shader;
}

function loop() {
  slowX *= 0.95;
  slowX += 0.05 * m[0] / iW;

  zoom = Math.pow(10, -36 * Math.max(0.003, Math.min(1, slowX)));

  gl.uniform1f(uzoom, zoom);
  gl.drawArrays(gl.TRIANGLES, 0, 6);

  requestAnimationFrame(loop);
}

function demo() {
  if (touched) return;
  if (m[0] < iW * 0.99) {
    m[0]+= iW / 100 >> 0;
    timeout = setTimeout(demo, 100);
  }
}

function mouse(e) {
  e.preventDefault();
  if (typeof(e.touches) != 'undefined') e = e.touches[0];
  touched = true;
  m[0] = e.pageX;
  m[1] = e.pageY;
}
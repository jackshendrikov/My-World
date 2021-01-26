let canvas = document.getElementById("canvas");
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Initialize the GL context
let gl = canvas.getContext('webgl');
if (!gl) {
  console.error("Unable to initialize WebGL.");
}

// Time step
let dt = 0.03;

// Time
let time = 0.0;

// --- Shader sources ---
let vertexSource = `
  attribute vec2 position;
  void main() {
    gl_Position = vec4(position, 0.0, 1.0);
  }
`;

let fragmentSource = `
  precision highp float;
  
  uniform float width;
  uniform float height;
  vec2 resolution = vec2(width, height);
  
  uniform float time;
  
  void main(){
  
      //Normalized pixel coordinates (from 0 to 1)
    vec2 uv = gl_FragCoord.xy/resolution.xy;
  
      float t = time/6.0;
      
    vec2 pos = uv;
    pos.y /= resolution.x/resolution.y;
    pos = 4.0*(vec2(0.5, 0.5) - pos);
      
    float strength = 0.4;
    for(float i = 1.0; i < 7.0; i+=1.0){ 
      pos.x += strength * sin(2.0*t+i*1.5 * pos.y)+t*0.5;
      pos.y += strength * cos(2.0*t+i*1.5 * pos.x);
      }
  
      //Time varying pixel colour
    vec3 col = 0.5 + 0.5*cos(time/2.0+pos.xyx+vec3(0,2,4));
      
    //Fragment colour
    gl_FragColor = vec4(col,1.0);
  }
`;
// --- Utility functions ---
window.addEventListener( 'resize', onWindowResize, false );

function onWindowResize(){
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;

  gl.viewport(0, 0, canvas.width, canvas.height);
  gl.uniform1f(widthHandle, window.innerWidth);
  gl.uniform1f(heightHandle, window.innerHeight);
}


// Compile shader and combine with source
function compileShader(shaderSource, shaderType){
  let shader = gl.createShader(shaderType);
  gl.shaderSource(shader, shaderSource);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
  	throw "Shader compile failed with: " + gl.getShaderInfoLog(shader);
  }
  return shader;
}

// Utility to complain loudly if we fail to find the attribute/uniform
function getAttribLocation(program, name) {
  let attributeLocation = gl.getAttribLocation(program, name);
  if (attributeLocation === -1) {
  	throw 'Cannot find attribute ' + name + '.';
  }
  return attributeLocation;
}

function getUniformLocation(program, name) {
  let attributeLocation = gl.getUniformLocation(program, name);
  if (attributeLocation === -1) {
  	throw 'Cannot find uniform ' + name + '.';
  }
  return attributeLocation;
}

// --- Create shaders ---

// Create vertex and fragment shaders
let vertexShader = compileShader(vertexSource, gl.VERTEX_SHADER);
let fragmentShader = compileShader(fragmentSource, gl.FRAGMENT_SHADER);

// Create shader programs
let program = gl.createProgram();
gl.attachShader(program, vertexShader);
gl.attachShader(program, fragmentShader);
gl.linkProgram(program);
gl.useProgram(program);

// Set up rectangle covering entire canvas
let vertexData = new Float32Array([
  -1.0,  1.0, 	// top left
  -1.0, -1.0, 	// bottom left
   1.0,  1.0, 	// top right
   1.0, -1.0, 	// bottom right
]);

//Create vertex buffer
let vertexDataBuffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, vertexDataBuffer);
gl.bufferData(gl.ARRAY_BUFFER, vertexData, gl.STATIC_DRAW);

// Layout of our data in the vertex buffer
let positionHandle = getAttribLocation(program, 'position');

gl.enableVertexAttribArray(positionHandle);
gl.vertexAttribPointer(positionHandle,
  2, 			  // position is a vec2 (2 values per component)
  gl.FLOAT,           // each component is a float
  false,   // don't normalize values
  2 * 4, 		  // two 4 byte float components per vertex (32 bit float is 4 bytes)
  0 		      // how many bytes inside the buffer to start from
  );

// Set uniform handle
let timeHandle = getUniformLocation(program, 'time');
let widthHandle = getUniformLocation(program, 'width');
let heightHandle = getUniformLocation(program, 'height');

gl.uniform1f(widthHandle, window.innerWidth);
gl.uniform1f(heightHandle, window.innerHeight);

function draw(){
  //Update time
  time += dt;

	//Send uniforms to program
  gl.uniform1f(timeHandle, time);
  //Draw a triangle strip connecting vertices 0-4
  gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);

  requestAnimationFrame(draw);
}

draw();
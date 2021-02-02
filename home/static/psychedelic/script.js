let container, camera, scene, renderer, uniforms;

init();
animate();

function init() {
    container = document.getElementById('container');
    camera = new THREE.Camera();
    camera.position.z = 1;

    scene = new THREE.Scene();

    let geometry = new THREE.PlaneBufferGeometry(3, 3);

    uniforms = {
        time: { type: "f", value: 1.0 },
        resolution: { type: "v2", value: new THREE.Vector2() }
    };

    let material = new THREE.ShaderMaterial( {
        uniforms: uniforms,
        vertexShader: document.getElementById('vertexShader').textContent,
        fragmentShader: document.getElementById('fragmentShader').textContent
    });

    let mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    renderer = new THREE.WebGLRenderer();
    renderer.setPixelRatio(window.devicePixelRatio);

    container.appendChild( renderer.domElement );

    onWindowResize();
    window.addEventListener('resize', onWindowResize,false);
}

function onWindowResize( event ) {
    renderer.setSize(window.innerWidth, window.innerHeight);

    uniforms.resolution.value.x = renderer.domElement.width;
    uniforms.resolution.value.y = renderer.domElement.height;
}

function animate() {
    requestAnimationFrame(animate);
    render();
}

function render() {
    uniforms.time.value += 0.05;
    renderer.render( scene, camera );
}
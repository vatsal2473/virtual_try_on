var thumbnails = document.getElementById("thumbnails");
var imgs = thumbnails.getElementsByTagName("img");
var main = document.getElementById("images");
var counter = 0;
var loader = document.querySelector(".loader");
var menu = document.querySelector("#menu-items");
var loaded = false;
var c_main = document.querySelector(".c-main");

for (let i = 0; i < imgs.length; i++) {
  let img = imgs[i];
  img.addEventListener("click", function () {
    main.src = this.src;
  });
}

(function () {
  let scene = new THREE.Scene();
  let camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );

  let renderer = new THREE.WebGLRenderer({ alpha: true });
  renderer.setClearColor(0x000000, 0);
  renderer.setSize(window.innerWidth, window.innerHeight);
  document.getElementById("container").appendChild(renderer.domElement);
  warp = false;
  window.setTimeout(function () {
    warp = true;
  }, 2000);
  window.addEventListener("resize", function () {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
  });

  particleSystem = createParticleSystem();
  scene.add(particleSystem);
  let time = 0.0;
  let target = 10.0;
  let distance = 10;
  let assignedposition = 2;
  let frame;
  let pendingBlow = { x: 0.0, y: 0.0 };
  camera.up = new THREE.Vector3(0, 1, 0);
  let animate = function () {
    frame = requestAnimationFrame(animate);
    animating = false;
    if (warp) {
      animating = true;
      time += (target - time) / 25;
    }
    particleSystem.material.uniforms.time.value = time;

    particleSystem.material.uniforms.mx.value +=
      (pendingBlow.x - particleSystem.material.uniforms.mx.value) / 100;
    particleSystem.material.uniforms.my.value +=
      (pendingBlow.y - particleSystem.material.uniforms.my.value) / 100;
    camera.position.z = distance;
    camera.lookAt(new THREE.Vector3(0, 0, 0));
    distance += (assignedposition - distance) / 100;
    renderer.render(scene, camera);
  };

  animate();
  document.onmousemove = function (e) {
    pendingBlow.x = (e.pageX - window.innerWidth / 3) / window.innerWidth;
    pendingBlow.y = (e.pageY - window.innerHeight / 3) / window.innerHeight;
  };
})();

function createParticleSystem() {
  let icosa = new THREE.IcosahedronBufferGeometry(1, 7);

  let vertexShader = `
        varying vec3 v;
        varying vec3 pos;
        float posY;
        uniform float radius;
        uniform float time;
        uniform float mx;
        uniform float my;

        float rand(float n){
            return fract(sin(n) * 43758.5453123);
        }

        void main() {
            vec3 norm = normalize(normal);
            float phaseSin = 40.0*cos(mx*3.14)*cos((norm.x-norm.y/2.0+norm.z));
            float phaseCos = 40.0*sin(my*3.14)*cos((-norm.x/2.0+norm.y+norm.z));
            pos = (radius+0.1*rand(1.0)*sin(time + phaseSin)*cos(time + phaseCos)) * norm;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
        `;

  let fragmentShader = `#extension GL_OES_standard_derivatives : enable

        varying vec3 v;
        varying vec3 pos;
        uniform float time;
        uniform sampler2D texture;
        uniform float mx;
        uniform float my;
        float dProd;
        uniform vec3 highlight;
        uniform vec3 shadow;
        uniform vec3 light;
        float rand(float n)
        {
            return fract(sin(n) * 43758.5453123);
        }
        void main() {
            // N: normal vector
            vec3 N = normalize( cross( dFdx( pos.xyz ), dFdy( pos.xyz ) ) );
            float intensity = max(0.0, pow(2.71,-0.1*distance(pos,light))*dot(normalize(N), normalize(light)));
            vec3 col = (highlight*intensity + (1.0-intensity)*shadow)/(intensity+1.0);
            gl_FragColor = vec4(col,1.0);
        }
        `;
  let fire = new THREE.TextureLoader().load("./fire.png");
  let uniforms = THREE.UniformsUtils.merge([
    THREE.UniformsLib["ambient"],
    THREE.UniformsLib["lights"],
    {
      time: { type: "f", value: 1.0 },
      texture: { type: "t", value: fire },
      radius: { type: "f", value: 1.15 },
      light: { type: "v3", value: [1.0, 2.0, 6.0] },
      highlight: { type: "v3", value: [0.0, 0.0, 0.0] },
      shadow: { type: "v3", value: [0.0, 0.0, 1.0] },
      mx: { type: "f", value: 0.0 },
      my: { type: "f", value: 0.0 },
    },
  ]);

  // Create the material that will be used to render each vertex of the geometry
  let particleMaterial = new THREE.ShaderMaterial({
    uniforms: uniforms,
    vertexShader: vertexShader,
    fragmentShader: fragmentShader,
  });

  // Create the particle system
  particleSystem = new THREE.Mesh(icosa, particleMaterial);
  return particleSystem;
}

(function () {
  function FileUploader(selector) {
    if (undefined !== selector) {
      this.init(selector);
    }
  }

  FileUploader.prototype.init = function (selector) {
    if (undefined !== this.$el) {
      this.unsuscribe();
    }

    this.$el = document.querySelector(selector);
    this.$fileInput = this.$el.querySelector("input");
    this.$img = this.$el.querySelector("img");

    this.suscribe();
  };

  FileUploader.prototype.suscribe = function () {
    this.$fileInput.addEventListener("change", _handleInputChange.bind(this));
    this.$img.addEventListener("load", _handleImageLoaded.bind(this));
    this.$el.addEventListener("dragenter", _handleDragEnter.bind(this));
    this.$el.addEventListener("dragleave", _handleDragLeave.bind(this));
    this.$el.addEventListener("drop", _handleDrop.bind(this));
  };

  FileUploader.prototype.unsuscribe = function () {
    this.$fileInput.removeEventListener(
      "change",
      _handleInputChange.bind(this)
    );
    this.$img.removeEventListener("load", _handleImageLoaded.bind(this));
    this.$el.removeEventListener("dragenter", _handleDragEnter.bind(this));
    this.$el.removeEventListener("dragleave", _handleDragLeave.bind(this));
    this.$el.removeEventListener("drop", _handleDrop.bind(this));
  };

  function _handleDragEnter(e) {
    e.preventDefault();

    if (!this.$el.classList.contains("dragging")) {
      this.$el.classList.add("dragging");
    }
  }

  function _handleDragLeave(e) {
    e.preventDefault();

    if (this.$el.classList.contains("dragging")) {
      this.$el.classList.remove("dragging");
    }
  }

  function _handleDrop(e) {
    e.preventDefault();
    this.$el.classList.remove("dragging");
    this.$img.files = e.dataTransfer.files;
    this.$fileInput.files = e.dataTransfer.files;
    _handleInputChange.call(this);
  }

  function _handleImageLoaded() {
    file = this.$img.src;
    human_model = menu.value;
    console.log(human_model.length);
    console.log(file.length);
    let form = new FormData();
    form.append('file', file);
    form.append('human_model', human_model);
    console.log(form)


    fetch("https://vatsal2473-u9y0h6e2vtv1zj93.socketxp.com//file-upload", {
      method: "post",
      mode: "no-cors",
      headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS,DELETE,PUT',
        'Authorization': 'Bearer key',
      },
      body: form,
    })
      .then(function (response) {
        console.log(response)
        if (response.body) {
          return response.json();
        } else {
          return "Empty response";
        }
      })
      .then(function (data) {
        let next = document.getElementById("images");
        next.src="data:image/png;base64,"+data.output

      })
      .catch((error) => console.error("Error:", error));

    c_main.style.overflow = "scroll";
    this.$img.classList.add("loaded");
    let next = document.querySelector(".result");
    next.scrollIntoView({ behavior: "smooth" });
    loader.style.display = "none";
    main.src = this.$img.src;
    main.style.filter = "blur(0px)";
    for (let i = 0; i < imgs.length; i++) {
      imgs[i].style.filter = "blur(0px)";
    }

    loaded = true;
  }
  function _handleInputChange(e) {
    var file = undefined !== e ? e.target.files[0] : this.$img.files[0];

    var pattern = /image-*/;
    var reader = new FileReader();

    if (!file.type.match(pattern)) {
      alert("invalid format");
      return;
    }

    if (this.$el.classList.contains("loaded")) {
      this.$el.classList.remove("loaded");
    }

    reader.onload = _handleReaderLoaded.bind(this);
    reader.readAsDataURL(file);
  }

  function _handleReaderLoaded(e) {
    var reader = e.target;
    this.$img.src = reader.result;
    this.$el.classList.add("loaded");
  }

  window.FileUploader = FileUploader;
})();

new FileUploader(".uploader");

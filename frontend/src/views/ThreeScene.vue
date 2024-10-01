<template>
  <div>
    <base-header class="pb-3 pb-4 pt-3 pt-md-4 bg-img-with-overlay d-flex align-items-center justify-content-center">
      <h1 class="text-white shopname">影绘探索</h1>
      <b-button variant="info" @click="showIntroModal" class="mt-3">功能介绍</b-button>
    </base-header>
    <div ref="threeContainer" class="three-container">
      <!-- 嵌入的控制面板 -->
      <div class="embedded-controls">
        <!-- 响应式表单 -->
        <b-container fluid class="pt-3">
          <!-- 时间选择 -->
          <div class="time-selector-container text-style">
            <b-col sm="12">
              <b-form-group label="视频时间（秒）:">
                <b-form-select v-model="time" :options="timeOptions" class="custom-scroll"></b-form-select>
              </b-form-group>
            </b-col>
          </div>
          <b-form @submit.prevent="submitCameraInfo">
            <b-row>
              <b-col>
                <b-button type="submit" variant="primary bg-video text-style custom-button" class="w-100">生成视频</b-button>
              </b-col>
            </b-row>
          </b-form>
        </b-container>
      </div>
    </div>
    <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer>
      <div class="text-style">为模型设定一个角度，您可以任意转动模型。同时为视频选择一个合适的时长。发挥您的想象力，为作品注入灵魂！</div>
    </b-modal>
    <b-modal id="error-modal" v-model="errorModalShow" title="错误提示" ok-only @hide="errorModalShow = false">
      <div>{{ errorModalMessage }}</div>
    </b-modal>
    <div v-if="loading" class="overlay">
      <div class="loader"></div>
      <div class="loading-text">GPU正在飞速运转中...</div>
      <div class="loading-text">视频生成大概需要10分钟</div>
      <div class="loading-text">点击“后台加载”稍后在个人中心查看</div>
      <!-- 取消按钮 -->
      <b-button variant="danger" @click="cancelLoading">后台加载</b-button>
    </div>
  </div>
</template>



<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import axios from 'axios';

export default {
  name: 'threescene',
  data() {
    return {
      formVisible: false, // 控制表单的显示
      errorModalShow: false, // 控制错误提示弹窗的显示
      time:'4',
      timeOptions: [
        { value: '1', text: '1秒' },
        { value: '2', text: '2秒' },
        { value: '3', text: '3秒' },
        { value: '4', text: '4秒' },
        { value: '5', text: '5秒' },
        { value: '6', text: '6秒' },
        { value: '10', text: '10秒' },
        // 根据需要添加更多选项
      ],
      loading:false,   //遮罩层
      panel:null, 
      clock: new THREE.Clock(),
      model:null,
      modelUrl: '', // 添加这个属性以保证它是响应式的
      cameraInfo: {
        position: { x: '', y: '', z: '' },
        rotation: { x: '', y: '', z: '' },
      },
      renderer: null,
      camera: null,
      scene: null,
      controller: null,
      introModalShow:false,   //定义弹窗
    };
  },
  mounted() {
    // 从路由参数中提取 modelUrl
    // this.modelUrl = this.$route.query.modelUrl || '';
    // console.log(this.$route.query.modelUrl, 'aaa');
    this.fetchData();
    this.initThree();
    window.addEventListener('resize', this.onWindowResize);

    // this.loadModel('/models/200001-SoccerSpin.glb', this.scene);
    this.animate();
    // 检查 modelUrl 是否有效，并加载模型
    this.showIntroModal()   //自动调用显示功能的弹窗



},
  beforeDestroy() {
    window.removeEventListener('resize', this.onWindowResize);
  },
  methods: {
    cancelLoading() {
      this.loading = false; // 仅隐藏遮罩层
      this.$router.push('culture');
    },
    fetchData() {
      axios.get(`${process.env.VUE_APP_API_URL}/customize`)
        .then(response => {
          const modelUrl = `${process.env.VUE_APP_API_URL}/${response.data}`;
          this.loadModel(modelUrl, this.scene);
          console.log(modelUrl);
          // 直接从响应数据中获取姓名、邮箱和列表
        })
        .catch(error => {
          console.error("There was an error fetching the data:", error);
          this.errorModalMessage = '并不是所有输入都会有结果，终究要明白，这个算力的GPU能跑已经很难得...    ————来自“时光绘卷”的温馨提示'; // 可以根据实际错误设置更具体的消息
          this.errorModalShow = true; // 显示错误提示弹窗
          this.loading = false;
        });
    },
    showIntroModal() {
      this.introModalShow = true; // 新增，显示功能介绍弹窗
    },
    initThree() {
      const container = this.$refs.threeContainer;
      const width = container.clientWidth;
      const height = container.clientHeight;

      // 场景初始化
      this.scene =   new THREE.Scene();
      

      // 相机初始化
      this.camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
      this.camera.position.set(0, 3, 4);
      var target = new THREE.Vector3(0,0,1.2);
      this.camera.lookAt(target);

      // 渲染器初始化a
      this.renderer = new THREE.WebGLRenderer({ antialias: true });
      this.renderer.setSize(width, height);
      this.renderer.setPixelRatio(window.devicePixelRatio);
      this.renderer.setClearColor(0x333333);
      container.appendChild(this.renderer.domElement);

      // 灯光初始化
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
      this.scene.add(ambientLight);
      const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
      directionalLight.position.set(0, 1, 1);
      this.scene.add(directionalLight);

      // 控制初始化
      this.controller = new OrbitControls(this.camera, this.renderer.domElement);
      this.controller.addEventListener('change', this.updateCameraInfo);
      // 添加地面网格
      const size = 100; // 网格的大小
      const divisions = 100; // 网格被分成多少份

      const gridHelper = new THREE.GridHelper(size, divisions);
      this.scene.add(gridHelper);


    },

    loadModel(modelUrl) {
  const loader = new GLTFLoader();
  loader.load(modelUrl, (gltf) => {
    this.scene.add(gltf.scene); // 将模型添加到场景中

    if (gltf.animations && gltf.animations.length) {
      // 创建动画混合器实例
      this.mixer = new THREE.AnimationMixer(gltf.scene);

      // 遍历模型中的所有动画并播放它们
      gltf.animations.forEach((clip) => {
        const action = this.mixer.clipAction(clip);
        action.play();
      });
    }

    this.updateCameraInfo(); // 可选：加载模型后更新相机信息
  }, undefined, (error) => {
    console.error('An error happened while loading the model:', error);
  });
},
animate() {
  requestAnimationFrame(() => this.animate()); // 使用箭头函数确保 this 指向

  const delta = this.clock.getDelta();

  if (this.mixer) {
    this.mixer.update(delta);
  }

  this.renderer.render(this.scene, this.camera);
},




render(){
  this.controller.update();

  requestAnimationFrame(this.render);

},

    onWindowResize() {
      const container = this.$refs.threeContainer;
      this.camera.aspect = container.clientWidth / container.clientHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(container.clientWidth, container.clientHeight);
      this.renderer.render(this.scene, this.camera);
    },
    updateCameraInfo() {
      const pos = this.camera.position;
      const rot = this.camera.rotation;
      
      // 直接更新 cameraInfo 数据对象
      this.cameraInfo = {
        position: { 
          x: pos.x.toFixed(2), 
          y: pos.y.toFixed(2), 
          z: pos.z.toFixed(2) 
        },
        rotation: {
          x: THREE.MathUtils.radToDeg(rot.x).toFixed(2),
          y: THREE.MathUtils.radToDeg(rot.y).toFixed(2),
          z: THREE.MathUtils.radToDeg(rot.z).toFixed(2)
        }
      };
    },
    submitCameraInfo() {
      this.loading = true; //再开始上传的时候显示遮罩层
      // 假设已经在data中定义了time参数，或者通过其他方式获取
      // 假设你从sessionStorage中读取并解析数据
      const storedPath = sessionStorage.getItem('bg_path');
      const bg_path = JSON.parse(storedPath || '""');

      const storedGlb = sessionStorage.getItem('GLBfilename');
      const glbfilename = JSON.parse(storedGlb || '""');
      console.log(bg_path);
      console.log(glbfilename);
// 现在你可以使用data了

      // 构建要发送的表单数据
      const formData = new FormData();
      formData.append('time', this.time);
      formData.append('bg_path',bg_path);
      formData.append('gltf',glbfilename);
      formData.append('pos_x', this.cameraInfo.position.x);
      formData.append('pos_y', -this.cameraInfo.position.z);
      formData.append('pos_z', this.cameraInfo.position.y);
      formData.append('rad_x', -this.cameraInfo.rotation.x);
      formData.append('rad_y', this.cameraInfo.rotation.y);
      formData.append('rad_z', this.cameraInfo.rotation.z);
      
      // 发送POST请求到后端
      axios.post(`${process.env.VUE_APP_API_URL}/customize`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        this.loading = false;
        // 这里处理后端的响应，例如显示成功消息或者处理返回的数据
        console.log('Success:', response.data);
        const videoUrl = response.data.videoUrl;
        console.log(videoUrl);
        sessionStorage.setItem('videourl', JSON.stringify(videoUrl));
        // 使用 Vue Router 进行跳转，并通过 URL 参数传递视频URL
        this.$router.push({ name: 'videodisplaypage'});
      })
      .catch(error => {
        this.loading = false;
        console.error('Error submitting camera info:', error);
      });
    }

  
  }
};
</script>

<style>
/* 遮罩层效果 */
.overlay {
  position: fixed; /* 或者 'absolute', 取决于你的布局 */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.loading-text {
  color: #FFF; /* 根据背景调整颜色 */
  margin-top: 20px; /* 适当的间距，根据需要调整 */
  font-size: 16px; /* 根据需要调整字体大小 */
}
.three-container {
  width: 100%;
  height: 550px ; /* 从400px调整为600px或更高，根据需要 */
  position: relative; /* 为内嵌组件定位做准备 */
  overflow: hidden;
}
.dropdown-menu {
  max-height: 200px; /* 设置最大高度 */
  overflow-y: auto; /* 内容超出时可滚动 */
}
.custom-scroll .dropdown-menu {
  max-height: 200px; /* 设置最大高度 */
  overflow-y: auto; /* 内容超出时可滚动 */
}
.bg-img-with-overlay {
    background-image: url('/img/culture/yinhe.jpg');
    background-size: cover;
    background-position: center;
    position: relative;
  }
  .bg-img-with-overlay::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
  }
  @font-face {
    font-family: yishuzi;
    src: url('/img/ziti/汉仪瑞鹤.ttf') format('truetype');
  }
  @font-face {
    font-family: laolao;
    src: url('/img/ziti/姥姥字体.ttf') format('truetype');
  }
.text-style{
  font-family: laolao;
  font-size: 20px;
  font-weight: 3000;
  color: rgb(3, 3, 3);
}
.shopname{
  font-family: yishuzi;
  font-size: 50px;
  font-weight: 5000;
  color: rgb(255, 255, 255);
}
/* 内嵌控制面板样式 */
.embedded-controls {
  position: absolute; /* 相对于.three-container进行定位 */
  top: 50px; /* 距离顶部的距离，根据需要调整 */
  right: 20px; /* 距离右侧的距离，根据需要调整 */
  background: rgba(255, 255, 255, 0.8); /* 透明背景，可根据需要调整 */
  padding: 10px; /* 内边距 */
  border-radius: 8px; /* 圆角 */
  z-index: 10; /* 确保它在Three.js渲染界面之上 */
  display: flex; /* 使用Flex布局 */
  flex-direction: column; /* 项目垂直排列 */
  gap: 5px; /* 项目间距 */
}
.custom-button {
  background-color: rgb(255, 255, 255); /* 自定义的背景色 */
}

</style>

<template>
  <div>
    <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
      <h1 class="text-white shopname">人物动作选取</h1>
      <b-button variant="info" @click="showIntroModal" class="mt-3 custom-button">功能介绍</b-button>
    </base-header>
<b-container class="mt-3">
  <b-tabs>
    <!-- Character Tab -->
    <b-tab title="人物" active class="image-card-bg">
      <b-row>
        <b-col md="4" sm="6" v-for="(gif, index) in paginatedCharacterGifs" :key="'character-' + index" class="mb-3">
          <b-card :class="{ 'selected': isSelected(gif.id) }" @click="setFormInput(gif.id, 'character')" class="gallery-item">
              <b-img :src="`${gif.url}?${gif.key}`" alt="Character GIF" fluid @click="refreshGif(index, 'character')"></b-img>
              <b-card-text class="text-center text-style">{{ gif.name }}</b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-pagination v-model="characterPage" :total-rows="characterGifs.length" :per-page="perPage" align="center" limit="3"></b-pagination>
        </b-col>
      </b-row>
    </b-tab>
    <!-- Action Tab -->
    <b-tab title="武术动作" class="image-card-bg">
      <b-row>
        <b-col md="4" sm="6" v-for="(gif, index) in paginatedActionGifs" :key="'action-' + index" class="mb-3">
          <b-card :class="{ 'selected': isSelected(gif.id) }" @click="setFormInput(gif.id, 'action')" class="gallery-item">
              <b-img :src="`${gif.url}?${gif.key}`" alt="Action GIF" fluid @click="refreshGif(index, 'action') "></b-img>
              <b-card-text class="text-center text-style">{{ gif.name }}</b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-pagination v-model="actionPage" :total-rows="actionGifs.length" :per-page="perPage" align="center" limit="3"></b-pagination>
        </b-col>
      </b-row>
    </b-tab>
    <!-- 舞蹈动作 Tab -->
    <b-tab title="舞蹈动作" class="image-card-bg">
      <b-row>
        <b-col md="4" sm="6" v-for="(gif, index) in paginatedDanceGifs" :key="'dance-' + index" class="mb-3">
          <b-card :class="{ 'selected': isSelected(gif.id) }" @click="setFormInput(gif.id, 'dance') " class="gallery-item" >
              <b-img :src="`${gif.url}?${gif.key}`" alt="Dance GIF" fluid @click="refreshGif(index, 'dance')"></b-img>
              <b-card-text class="text-center text-style">{{ gif.name }}</b-card-text>
          </b-card>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-pagination v-model="dancePage" :total-rows="danceGifs.length" :per-page="perPage" align="center" limit="3"></b-pagination>
        </b-col>
      </b-row>
    </b-tab>

  </b-tabs>
</b-container>
        <b-col md="12">
          <b-card>
            <b-form @submit.prevent="submitForm" class="text-center ">
              <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
              <b-button type="submit" variant="primary" class="submit-btn image-card-bg">点击加载</b-button>
            </b-form>
          </b-card>
        </b-col>
        <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer>
          <div class="text-style">
            请在“人物”中选取喜欢的形象；
            在“武术动作”或“舞蹈动作”中选取喜欢的动作。发挥您的想象力，我们期待碰撞出不一样的火花。
          </div>
        </b-modal>
        <b-modal id="error-modal" v-model="errorModalShow" title="错误提示" ok-only @hide="errorModalShow = false">
          <div>{{ errorModalMessage }}</div>
        </b-modal>
        <div v-if="loading" class="overlay">
          <div class="loader"></div>
          <div class="loading-text">GPU正在飞速运转中...</div>
        </div>
  </div>
</template>

<script>
import axios from 'axios';
import ThreeScene from './ThreeScene.vue';

export default {
  components: {
    ThreeScene, // 注册子组件
  },
data() {
  return {
    loading:false,   //遮罩层
    formVisible: false, // 控制表单的显示
    errorModalShow: false, // 控制错误提示弹窗的显示
    errorModalMessage: '', // 错误消息内容
    perPage: 3, // 每页显示的项目数量
    characterPage: 1, // 当前人物GIFs的页码
    actionPage: 3, // 当前动作GIFs的页码
    dancePage:3,
    introModalShow:false,   //定义弹窗
    imagePreview: null,
    processedImageUrl: null,
    showClickEffect: false, // 控制点击效果是否显示
    clickEffectStyle: {}, // 定义点击效果的样式（位置）
    fileName:'',
    modelUrl:null,  //存储GLB模型的URL

    selectedCharacterId: '',
    selectedActionId: '',
    videoUrl: null,
    characterGifs: [
      { id: "200000", url: '/img/en3D/character/render_color_200000.png', key: 0,name:'斯蒂芬·库里'},
      { id: "200001", url: '/img/en3D/character/render_color_200001.png', key: 0,name:'利昂内尔·梅西' },
      { id: "200002", url: '/img/en3D/character/render_color_200002.png', key: 0,name:'蜘蛛侠' },
      { id: "200003", url: '/img/en3D/character/render_color_200003.png', key: 0,name:'奥普拉·温弗瑞' },
      { id: "200004", url: '/img/en3D/character/render_color_200004.png', key: 0,name:'钢铁侠' },
      // 更多人物GIF
    ],
    actionGifs: [
      { id: "Cartwheel", url: '/img/en3D/wushu/Cartwheel.gif', key: 0, name: '侧手翻' },
      { id: "BackFlipToUppercut", url: '/img/en3D/wushu/BackFlipToUppercut.gif', key: 0, name: '后空翻上勾拳' },
      { id: "ChapaGiratoria2", url: '/img/en3D/wushu/Chapa-Giratoria2.gif', key: 0, name: '旋转踢' },
      { id: "MagicSpellCasting", url: '/img/en3D/wushu/MagicSpellCasting.gif', key: 0, name: '组合拳' },
      { id: "MmaKick", url: '/img/en3D/wushu/MmaKick.gif', key: 0, name: '综合格斗踢' },
      { id: "PunchToElbowCombo", url: '/img/en3D/wushu/PunchToElbowCombo.gif', key: 0, name: '铁山靠' },
      // 根据需要添加更多动作GIF及其名称
    ],

    danceGifs:[
      { id: "ArmsHipHopDance", url: '/img/en3D/dance/ArmsHipHopDance.gif', key: 0, name: '嘻哈舞' },
      { id: "BboyHipHopMove", url: '/img/en3D/dance/BboyHipHopMove.gif', key: 0, name: 'Bboy嘻哈舞' },
      { id: "BboyUprock", url: '/img/en3D/dance/BboyUprock.gif', key: 0, name: 'Bboy战斗舞' },
      { id: "BreakdanceEnding1", url: '/img/en3D/dance/BreakdanceEnding1.gif', key: 0, name: '霹雳舞' },
      { id: "ChickenDance", url: '/img/en3D/dance/ChickenDance.gif', key: 0, name: '鸡仔舞' },
      { id: "Flair", url: '/img/en3D/dance/Flair.gif', key: 0, name: '街舞' },
      { id: "GangnamStyle", url: '/img/en3D/dance/GangnamStyle.gif', key: 0, name: '江南Style' },
      { id: "ModernDancing", url: '/img/en3D/dance/ModernDancing.gif', key: 0, name: '现代舞' },
      { id: "RobotHipHopDance", url: '/img/en3D/dance/RobotHipHopDance.gif', key: 0, name: '机器人嘻哈舞' },
      { id: "SambaDancing", url: '/img/en3D/dance/SambaDancing.gif', key: 0, name: '桑巴舞' },
      { id: "SwingDancing", url: '/img/en3D/dance/SwingDancing.gif', key: 0, name: '摇摆舞' },
      { id: "TutHipHopDance", url: '/img/en3D/dance/TutHipHopDance.gif', key: 0, name: '图坦卡蒙嘻哈舞' },
    ],

  };
},
mounted(){
      this.showIntroModal()   //自动调用显示功能的弹窗
    },
computed: {
  processedFileName() {
    return this.$store.state.processedFileName;
  },
    paginatedCharacterGifs() {
    const start = (this.characterPage - 1) * this.perPage;
    const end = start + this.perPage;
    return this.characterGifs.slice(start, end);
  },
  paginatedActionGifs() {
    const start = (this.actionPage - 1) * this.perPage;
    const end = start + this.perPage;
    return this.actionGifs.slice(start, end);
  },
  paginatedDanceGifs() {
    // 新增：舞蹈动作的分页逻辑
    const start = (this.dancePage - 1) * this.perPage;
    const end = start + this.perPage;
    return this.danceGifs.slice(start, end);
  },

},
methods: {
  cancelLoading() {
      this.loading = false; // 仅隐藏遮罩层
      this.$router.push('culture');
    },
  isSelected(id) {
    return id === this.selectedCharacterId || id === this.selectedActionId;
  },
  showIntroModal() {
      this.introModalShow = true; // 新增，显示功能介绍弹窗
    },
  goToCustomizePage() {
      this.$router.push({ name: 'THREESCENE', query: { modelUrl: this.modelUrl } });
    },
  onFileChange(e) {
    this.selectedFile = e.target.files[0];
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  },
  downloadVideo() {
    const link = document.createElement('a');
    link.href = this.videoUrl;
    link.download = 'generated-video.mp4'; // Modify as needed for video files
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  },
  setFormInput(id, type) {
    if (type === 'character') {
      this.selectedCharacterId = id;
    } else if (type === 'action' || type === 'dance') { // 允许动作ID来自武术或舞蹈
      this.selectedActionId = id;
    }
  },
  submitForm() {
    // 首先，检查是否选择了人物和动作
    if (!this.selectedCharacterId || !this.selectedActionId) {
      // 设置错误消息
      this.errorModalMessage = '请选择一个人物和一个动作！';
      // 显示错误提示弹窗
      this.errorModalShow = true;
      // 既然条件不满足，就直接返回，不执行后面的代码
      return;
    }

    // 如果条件满足，继续执行后面的代码
    this.loading = true; //显示遮罩层
    const formData = new FormData();
    formData.append('charac_id', this.selectedCharacterId);
    formData.append('action_id', this.selectedActionId);

    axios.post(`${process.env.VUE_APP_API_URL}/en3d`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      responseType: 'blob'
    })
    .then(response => {
      this.loading = false;
      // 文件生成成功后的操作，这里可以根据实际需要进行调整
      this.$router.push({ name: 'THREESCENE' });
    })
    .catch(error => {
      this.loading = false;
      console.error('Error:', error);
      this.errorModalMessage = '处理您的请求时出现错误，请稍后再试。';
      this.errorModalShow = true;
    });
  },

  handleCameraInfoUpdated(info) {
    this.cameraInfo = info;
  },
  refreshGif(index, type) {
  if (type === 'character') {
    this.characterGifs[index].key += 1;
  } else if (type === 'action') {
    this.actionGifs[index].key += 1;
  }
},

},
};
</script>
<style scoped>
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
.selected {
  border: 2px solid #559dfa; /* 蓝色边框 */
  padding: 4px; /* 保持内容内边距，以避免边框覆盖内容 */
}

.upload-section, .processed-image-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}
@media (max-width: 767px) {
  .upload-section, .processed-image-section {
    flex-direction: column;
  }
}
.video-generator {
text-align: center;
}
.upload-section, .processed-image-section {
display: flex;
flex-direction: column;
align-items: center;
}
.form-group {
margin-bottom: 20px;
}
.input-group input[type="file"], .input-group input, .input-group button {
  margin: 10px 0;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 80%;
}

.input-group button, .processed-image button {
  background-color: #559dfa;
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px 20px;
  margin-top: 10px;
}

.input-group button:hover, .processed-image button:hover {
  background-color: #1057c9;
}

.image-preview img, .processed-image img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ccc;
  padding: 5px;
  margin-top: 20px;
}
.image-uploader .b-form-file,
.image-uploader .b-form-input {
  max-width: 100%;
  margin: auto;
}

.image-preview,
.processed-image {
  position: relative;
}

.image-preview img,
.processed-image img {
  max-width: 100%;
  height: auto;
}

/* 加载动画样式 */
.image-uploading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.loader {
  border: 5px solid #f3f3f3; /* Light grey */
  border-top: 5px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.input-field, .submit-btn {
margin: 10px 0;
padding: 10px;
border-radius: 4px;
width: 80%;
margin-left: auto;
margin-right: auto;
}

.submit-btn {
color: white;
border: none;
cursor: pointer;
}

.video-preview {
position: relative;
width: 100%; /* Adjust width as necessary */
padding-top: 56.25%; /* 16:9 Aspect Ratio */
}

.video-preview video {
position: absolute;
top: 0;
left: 0;
width: 100%;
height: 100%;
}
.input-group input[type="file"], .input-group input, .input-group button {
  margin: 10px 0;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
  width: 80%;
}

.input-group button, .processed-image button {
  background-color: #559dfa;
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px 20px;
  margin-top: 10px;
}

.input-group button:hover, .processed-image button:hover {
  background-color: #1057c9;
}

.image-preview img, .processed-image img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ccc;
  padding: 5px;
  margin-top: 20px;
}
.image-uploader .b-form-file,
.image-uploader .b-form-input {
  max-width: 100%;
  margin: auto;
}

.image-preview,
.processed-image {
  position: relative;
}

.image-preview img,
.processed-image img {
  max-width: 100%;
  height: auto;
}

/* 加载动画样式 */
.image-uploading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.loader {
  border: 5px solid #f3f3f3; /* Light grey */
  border-top: 5px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
}
.selectable-image{
  cursor: pointer;  /*表示这个图片可点击*/ 
}
.click-effect {
  position: absolute;
  border-radius: 50%;
  width: 10px;
  height: 10px;
  background-color: red;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s ease-in-out;
}
.bg-img-with-overlay {
    background-image: url('/img/culture/xiangulou.jpg');
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
    .image-card-bg {
      background: linear-gradient(135deg,#B17D4E, #E48A18,#736E5B);
  }

  .gallery-item {
  flex: 0 0 calc(33% - 20px); /* 为每个项目分配25%的宽度，并减去边距 */
  margin: 10px;
  text-align: center; /* 确保图片居中 */
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
  font-size: 45px;
  font-weight: 3500;
  color: rgb(255, 255, 255);
}
.custom-button {
  background-color: #fda085; /* 自定义的背景色 */
  color: white; /* 文本色 */
}
::v-deep .nav-tabs .nav-link {
  font-family: 'laolao', sans-serif;
}
.nav-tabs .nav-link {
  font-family: 'laolao', sans-serif;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

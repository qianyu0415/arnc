<template>
    <div>
      <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
        <h1 class="text-white shopname">古典艺术动态新生</h1>
        <b-button variant="info" @click="showIntroModal" class="mt-3 custom-button">功能介绍</b-button>
      </base-header>
      <b-container fluid class="mt-3">
        
            <b-row>
          <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer>
            <div class="text-style">
              请在“古风人物”中选取喜欢的人物或通过本地进行上传；
              在“动作视频”中选取合适的动作为人物赋能，打破静态壁垒，让古风人物焕发新机！
              “墨舞千秋”期待您的创作！
            </div>
          </b-modal>
          <b-col md="12">
            <b-card no-body class="gallery">
              <b-tabs card>
                <!-- 图片选项卡 -->
                <b-tab title="古风人物" >
                  <div class="gallery">
                    <div v-for="image in paginatedImages" :key="image.id" @click="selectImage(image.id)"
                        :class="{'selected': imagePath === image.id}" class="gallery-item">
                      <img :src="image.url">
                      <div class="label text-style">{{ image.description }}</div>
                    </div>
                  </div>
                  <!-- 图片分页控制 -->
                  <div class="pagination-container">
                  <b-pagination v-model="imagePage" :total-rows="images.length" :per-page="perPage" @change="updateImagePage" class="my-4" limit="3"></b-pagination>
                  </div>
                </b-tab>
              
                <!-- 视频选项卡 -->
                <b-tab title="动作视频">
                  <div class="gallery">
                    <div v-for="video in paginatedVideos" :key="video.id" @click="selectVideo(video.id)"
                        :class="{'selected': vidPath === video.id}" class="gallery-item">
                      <video controls>
                        <source :src="video.url" type="video/mp4">
                        Your browser does not support the video tag.
                      </video>
                      <div class="label text-style">{{ video.description }}</div>
                    </div>
                  </div>
                  <!-- 视频分页控制 -->
                  <div class="pagination-container">
                  <b-pagination v-model="videoPage" :total-rows="videos.length" :per-page="perPage" @change="updateVideoPage" class="my-4" limit="3"></b-pagination>
                  </div>
                </b-tab>
              </b-tabs>
            </b-card>
          </b-col>
        </b-row>
        <b-row>
          <b-col md="12">
            <b-card no-body class="gallery">
              <!-- Update: Hide only the input fields, not the submit button -->
              <b-form @submit.prevent="submitForm" >
                <!-- 文件上传字段 -->
                <div class="form-group" >
                  <b-form-file v-model="file" @change="fileSelected" placeholder="本地上传图片" drop-placeholder="Drop file here..."></b-form-file>
                </div>
                <!-- Submit Button remains visible -->
                <!-- 用户选择提示，可选实现
                <div v-if="imagePath" class="selected-feedback">Selected Image Path: {{ imagePath }}</div> -->
                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
                <b-button type="submit" class="submit-btn">点击生成视频</b-button>
              </b-form>
            </b-card>
          </b-col>
        </b-row>
        <b-row>
              <b-col md="12" class="mt-3" v-if="videoUrl">
                <b-card>
                  <h3 class="text-center">生成的视频:</h3>
                  <div class="video-preview">
                    <video controls class="w-100">
                      <source :src="videoUrl" type="video/mp4">
                      Your browser does not support the video tag.
                    </video>
                  </div>
                </b-card>
              </b-col>
            </b-row>
      </b-container>
      <b-modal id="error-modal" v-model="errorModalShow" title="错误提示" ok-only @hide="errorModalShow = false">
        <div>{{ errorModalMessage }}</div>
      </b-modal>
      <div v-if="loading" class="overlay">
          <div class="loader"></div>
          <div class="loading-text">GPU正在飞速运转中...</div>
          <div class="loading-text">视频生成大概需要5分钟</div>
          <div class="loading-text">点击“后台加载”稍后在个人中心查看</div>
          <!-- 取消按钮 -->
          <b-button variant="danger" @click="cancelLoading">后台加载</b-button>
        </div>

    </div>
  </template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
          // 其他已有的数据属性
      errorModalShow: false, // 控制错误提示弹窗的显示
      errorModalMessage: '', // 错误消息内容
      errorMessage: '', // 用于显示错误消息
      loading:false,   //遮罩层
      imageModalShow:false,   //控制图片模态窗口的展示
      selectImageUrl:'',    //被选中显示的图片URL
      perPage: 3, // 每页显示的项目数量
      imagePage: 1, // 当前图片页码
      videoPage: 1, // 当前视频页码
      introModalShow:false,   //定义弹窗
      file:null,
      imagePath: '',
      vidPath: '',
      videoUrl: null,
      images: [
        { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/woman4.jpg',
          url: 'img/ma/woman4.jpg',
          description: '凭栏佳丽'  },
        { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/woman1.png',
        url: 'img/ma/woman1.png',
        description: '绣扇倩影'  },
        { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/four.jpg',
          url: 'img/ma/four.jpg',
          description: '松风红袖'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/five.jpg',
          url: 'img/ma/five.jpg',
          description: '月影笛声'  },

          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/six-1.jpg',
          url: 'img/ma/six-1.jpg',
          description: '细赏樱花'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/nine.jpg',
          url: 'img/ma/nine.jpg',
          description: '素衣静妍'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/three.jpg',
          url: 'img/ma/three.jpg',
          description: '低眉思玉'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/seven.jpg',
          url: 'img/ma/seven.jpg',
          description: '花间雅坐'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/eight.jpg',
          url: 'img/ma/eight.jpg',
          description: '春光倩影'  },

          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/ten.jpg',
          url: 'img/ma/ten.jpg',
          description: '花间淑思'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/eleven.jpg',
          url: 'img/ma/eleven.jpg',
          description: '红裳佳丽'  },
          { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/source_image/twelve.jpg',
          url: 'img/ma/twelve.jpg',
          description: '春风轻扇'  },
      ],
      videos:[
      { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/driving/densepose/wuqinxi.mp4',
      url: 'img/ma/wuqinxi.mp4',
      description: '五禽戏'},
      { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/driving/densepose/jugong.mp4',
      url: 'img/ma/jugong.mp4',
      description: '鞠躬礼'},
      { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/driving/densepose/daquan1.mp4',
      url: 'img/ma/daquan1.mp4',
      description: '传统拳法'},
      { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/driving/densepose/demo4.mp4',
        url: 'img/ma/demo4.mp4',
        description: '舞蹈'},
      { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/driving/densepose/running.mp4',
      url: 'img/ma/running.mp4',
      description: '跑步'},
      { id: '/root/autodl-tmp/arnc_project/models/ma/inputs/applications/driving/densepose/shizishou.mp4',
      url: 'img/ma/shizishou.mp4',
      description: '十字手'},

      ],
    };
  },
  mounted() {
    this.showIntroModal();
  },
  computed: {
    // 计算当前页的图片
    paginatedImages() {
      const start = (this.imagePage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.images.slice(start, end);
    },
    // 计算当前页的视频
    paginatedVideos() {
      const start = (this.videoPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.videos.slice(start, end);
    },
  },
  methods: {
    cancelLoading() {
      this.loading = false; // 仅隐藏遮罩层
      this.$router.push('culture');
    },
    // 更新图片分页
    updateImagePage(pageNumber) {
      this.imagePage = pageNumber;
    },
    // 更新视频分页
    updateVideoPage(pageNumber) {
      this.videoPage = pageNumber;
    },
    showIntroModal() {
        this.introModalShow = true; // 新增，显示功能介绍弹窗
      },
    fileSelected(event) {
      if (event.target.files.length > 0) {
        this.file = event.target.files[0];
        this.imagePath = ''; // Reset imagePath if user decides to upload a file
      }
    },
    showImageModal(url) {
      this.selectedImageUrl = url;
      this.imageModalShow = true;
    },
    selectImage(id) {
      this.imagePath = id;
      this.showImageModal(image.url);
    },
      // 显示图片模态窗口并设置图片URL

    selectVideo(id) {
      this.vidPath = id;
    },
    submitForm() {
      // 重置错误信息
      this.errorMessage = '';

      // 检查是否同时选择了人物和动作
      if (!this.file && !this.imagePath) {
        this.errorMessage = '请选择一个人物！';
        return; // 阻止表单提交
      }
      if (!this.vidPath) {
        this.errorMessage = '请选择一个动作！';
        return; // 阻止表单提交
      }

      // 如果已选择人物和动作，则继续表单提交的处理
      this.loading = true;
      const formData = new FormData();
      if (this.file) {
        // 如果用户上传了文件，则添加到formData
        formData.append('imageFile', this.file);
      } else {
        // 否则，发送选择的imagePath
        formData.append('path_img', this.imagePath);
      }
      formData.append('path_vid', this.vidPath);

      axios.post(`${process.env.VUE_APP_API_URL}/magic-animate`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob' // Assuming the response is a video file
      })
      .then(response => {
        this.loading = false;
        // Create a URL for the blob response for video display
        const url = URL.createObjectURL(new Blob([response.data], { type: 'video/mp4' }));
        this.videoUrl = url;
      })
      .catch(error => {
        console.error('Error:', error);
        this.errorModalMessage = '并不是所有输入都会有结果，终究要明白，这个算力的GPU能跑已经很难得...    ————来自“墨舞千秋”的温馨提示'; // 可以根据实际错误设置更具体的消息
        this.errorModalShow = true; // 显示错误提示弹窗
        this.loading = false;
      });
    }
  }
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
.gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.gallery-item.selected {
  border: 2px solid #559dfa; /* 高亮选中的图片或视频 */
  padding: 4px;
}
.gallery-item {
  flex: 0 0 calc(30% - 20px); /* 每个项目宽度调整为30%，左右间距总和20px */
  margin: 10px; /* 上下各10px间距，左右各10px间距 */
  text-align: center; /* 确保图片居中 */
  background-color: #f8f9fa; /* 添加浅灰色背景色 */
  border-radius: 5px; /* 添加圆角效果 */
  padding: 10px; /* 添加内边距 */
}

.gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between; /* 确保图片之间有空隙且对齐 */
}
.image-uploader {
    text-align: center;
  }
.gallery-item img, .gallery-item video {
  width: 100%; /* Adjust as necessary */
  margin-bottom: 5px; /* Spacing between image/video and label */
  transition: transform 0.2s; /* 添加简单的放大效果 */
}
.gallery-item video {
  width: 100%; /* Ensure the width of the video is 100% of its container */
  height: 380px; /* Maintain the aspect ratio */
  object-fit: cover; /* Ensure the video covers the whole area without distortion */

}

.img-fluid {
  max-height: 80vh; /* 最大高度不超过视口的80% */
  object-fit: contain; /* 保持图片比例 */
}
.label {
  background: linear-gradient(111.4deg, #443532,#D1A574,#FDD894,#A65A06);
  color: white;
  padding: 20px 5px;
  border-radius: 5px;
  font-size: 1.0em;
  opacity: 0.7; /* 减少标签的不透明度 */
  font-family: "微软雅黑", sans-serif;
}

.gallery,.text-center {
  background: linear-gradient(111.4deg, #443532,#D1A574,#FDD894,#A65A06);
  border-radius: 5px; /* 圆角 */
  padding: 10px; /* 内边距 */
  width: auto; /* 宽度自适应 */
  margin: 20px auto; /* 上下间距20px，左右自动调整以居中 */
  text-align: center; /* 文字居中 */
}
.b-form-file, .b-button {
  margin: 10px 0; /* 为上传按钮和提交按钮添加上下间距 */
}
.input-field, .submit-btn {
  margin: 10px 0;
  padding: 10px;
  border-radius: 4px;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  background: linear-gradient(111.4deg, #443532,#D1A574,#FDD894,#A65A06);
}


.video-preview video {
  width: 100%; /* 视频宽度调整为100% */
  border-radius: 5px; /* 视频添加圆角 */
  margin-bottom: 20px; /* 视频下方留出一些空间 */
}

.video-preview {
  background-color: #e9ecef; /* 背景颜色 */
  padding: 10px; /* 内边距 */
  border-radius: 5px; /* 圆角 */
}
.pagination-centered {
  display: flex;
  justify-content: center;
}
.bg-img-with-overlay {
    background-image: url('/img/culture/yuanmingyuan.jpg');
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
  .pagination-container {
    display: flex;
    justify-content: center;
  }
  ::v-deep .nav-tabs .nav-link {
    font-family: 'laolao', sans-serif;
  }
  .nav-tabs .nav-link {
    font-family: 'laolao', sans-serif;
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
.custom-button {
  background: linear-gradient(#A65A06);
  color: white; /* 文本色 */
}
::v-deep .custom-file-input ~ .custom-file-label,
::v-deep .custom-file-input:lang(en) ~ .custom-file-label::after {
  background: linear-gradient(111.4deg, #443532,#D1A574,#FDD894,#A65A06);
  color: #000000; /* 字体颜色为白色 */
}
.video-preview {

  max-width: 600px; /* 最大宽度为800px，可根据需求调整 */
  margin: auto; /* 自动边距使其在容器中居中 */
}

video.w-100 {
  width: 100%; /* 确保视频在其容器内宽度为100% */
  height: auto; /* 高度自动调整以保持视频比例 */
}





</style>

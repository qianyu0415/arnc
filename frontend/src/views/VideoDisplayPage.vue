<template>
    <div>
      <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
        <h1 class="text-white shopname">视频展示</h1>
        <b-button variant="info" @click="showIntroModal" class="mt-3 custom-button">功能介绍</b-button>
      </base-header>
      <b-container fluid class="mt-3">
        <b-row>
          <b-col md="12">
            <b-card>
              <div class="video-container">
                <video controls>
                  <source :src="videoUrl" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
              </div>
            </b-card>
          </b-col>
        </b-row>
      </b-container>
      <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer>
        <div class="text-style">
          恭喜你，成功地穿梭了"时光绘卷"的所有篇章，您是时光的编织者，打破了传统创意的限制，创造出独特的视频故事。我们期待着您的下次创作。
        </div>
      </b-modal>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        introModalShow: false, // 控制功能介绍弹窗的显示
        videoUrl: '', // 视频URL
      };
    },
    mounted() {
      // 从URL参数中获取视频URL
      const storedPath = sessionStorage.getItem('videourl');
      const videourl = JSON.parse(storedPath || '"默认视频地址，如果没有接收到参数"');
      this.videoUrl = `${process.env.VUE_APP_API_URL}/${videourl}`;
      console.log(this.videoUrl);
      this.showIntroModal()   //自动调用显示功能的弹窗
    },
    methods: {
      showIntroModal() {
        this.introModalShow = true;
      },
    },
  };
  </script>
  
  <style scoped>
  /* 你可以根据需要调整或添加更多的CSS样式 */
  .video-container video {
    max-width: 100%;
    height: auto; /* 调整视频大小 */
  }
  .bg-img-with-overlay {
    background-image: url('/img/culture/baota.png');
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
  color: rgb(0, 0, 0);
}
.custom-button {
  background-color: #002C47; /* 自定义的背景色 */
  color: white; /* 文本色 */
}
.video-container {
  max-width: 480px; /* 最大宽度，可根据需要调整 */
  margin: auto; /* 自动边距使其在容器中居中 */
  box-shadow: 0 4px 8px rgba(0,0,0,0.1); /* 添加阴影效果 */
  border-radius: 8px; /* 轻微的圆角效果 */
  overflow: hidden; /* 防止内容溢出 */
}

video {
  width: 100%; /* 确保视频宽度响应容器大小 */
  height: auto; /* 高度自动以保持比例 */
}

.b-card {
  border: none; /* 去掉默认边框 */
  background-color: #fff; /* 卡片背景色，可根据主题调整 */
  padding: 20px; /* 卡片内边距 */
}

  </style>
  
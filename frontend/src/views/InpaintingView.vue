<template>
    <div>
      <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
        <h1 class=" shopname">画作元素去除平台</h1>
        <b-button variant="info" @click="showIntroModal" class="mt-3 custom-button">功能介绍</b-button>
      </base-header>
        <b-container fluid class="mt-3">
        <b-row>
          <b-col md="12" class="image-uploader">
            <b-row>
              <b-col md="6" class="mt-3">
                <b-card class="upload-card-bg">
                  <div v-if="!imagePreview" class="title-style">
                    原始图像
                  </div>
                  <div v-else class="image-preview">
                    <b-card-img :src="imagePreview" alt="Selected Image" class="selectable-image" @click="setImageClickCoords"></b-card-img>
                    <div v-if="showClickEffect" :style="clickEffectStyle" class="click-effect"></div>
                  </div>
                  <b-card-footer v-if="imagePreview">
                    <small class="title-style">原始图像</small>
                  </b-card-footer>
                </b-card>
              </b-col>

              <b-col md="6" class="mt-3">
                <b-card class="upload-card-bg">
                  <div v-if="!processedImageUrl" class="title-style">
                    结果图像
                  </div>
                  <div v-else class="processed-image">
                    <b-card-img :src="processedImageUrl" alt="Processed Image"></b-card-img>
                  </div>
                  <b-card-footer v-if="processedImageUrl">
                    <b-button @click="downloadImage" variant="title-style custom-button">下载</b-button>
                  </b-card-footer>
                </b-card>
              </b-col>
              <b-col md="12" class="image-uploader">
                <b-card class="image-uploader upload-card-bg">
                  <b-form @submit.prevent="uploadImage" class="text-center">
                    <b-form-file v-model="selectedFile" @change="onFileChange" placeholder="点击上传图片" class="mb-2"></b-form-file>
                    <b-form-input v-model="pointCoords" placeholder="选中的坐标(x,y)" class="mb-2"></b-form-input>
                    <b-button type="submit" variant="primary custom-button">点击运行</b-button>
                  </b-form>
                </b-card>
              </b-col> 
            </b-row>
          </b-col>
        </b-row>
        <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer class="title-style">
          <div class="title-style">
            “古境留韵”允许用户上传任何中国古代名画的数字版本，应通过先进的图像处理技术，选择性地去除画作中的特定元素或细节。
            该功能可以为后续的“时光绘卷”功能生成想要的背景。
          </div>
        </b-modal>
        <b-modal id="error-modal" v-model="errorModalShow" title="温馨提示" ok-only @hide="errorModalShow = false">
          <div>{{ errorModalMessage }}</div>
        </b-modal>
        <div v-if="loading" class="overlay">
          <div class="loader"></div>
          <div class="loading-text">GPU正在飞速运转中...</div>
        </div>
      </b-container>
    </div>
  </template>

  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        errorModalShow: false, // 控制错误提示弹窗的显示
        errorModalMessage: '', // 错误消息内容
        loading:false,   //遮罩层
        images:[],//加载图片
        introModalShow:false,   //定义弹窗
        selectedFile: null,
        imagePreview: null,
        pointCoords: '',
        processedImageUrl: null,
        showClickEffect: false, // 控制点击效果是否显示
        clickEffectStyle: {}, // 定义点击效果的样式（位置）
      };
    },
    mounted(){
      this.showIntroModal()   //自动调用显示功能的弹窗
    },
    watch: {
      'processedFileName'(newFileName) {
        console.log(`New processed file name: ${newFileName}`);
      }
    },
    methods: {
      showIntroModal() {
        this.introModalShow = true; // 新增，显示功能介绍弹窗
      },
      fetchImages() {
        axios.get(`${process.env.VUE_APP_API_URL}/get-image`)
          .then(response => {
            // 这里处理响应数据
            console.log(response.data);
            console.log(this.images[0]);
            // 假设你想将响应数据存储在Vue组件的data属性中
            this.images = response.data;
          })
          .catch(error => {
            console.error('Error:', error);
            this.errorModalMessage = '并不是所有输入都会有结果，终究要明白，这个算力的GPU能跑已经很难得...    ————来自“古境留韵”的温馨提示'; // 可以根据实际错误设置更具体的消息
            this.errorModalShow = true; // 显示错误提示弹窗
            this.loading = false;
          });
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

      uploadImage() {
          // 检查是否选择了文件
        if (!this.selectedFile) {
          this.errorModalMessage = '请先上传一张图片。';
          this.errorModalShow = true;
          return; // 停止方法执行
        }

        // 检查是否设置了点的坐标
        if (!this.pointCoords || this.pointCoords.split(',').length !== 2) {
          this.errorModalMessage = '请在图片上选择一个点，或确保坐标格式正确（x,y）。';
          this.errorModalShow = true;
          return; // 停止方法执行
        }
        this.loading = true; //再开始上传的时候显示遮罩层
        const formData = new FormData();
        formData.append('image', this.selectedFile);
        formData.append('point_coords', this.pointCoords);

        axios.post(`${process.env.VUE_APP_API_URL}/inpainting`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          responseType: 'blob', // Important for handling the binary image response
        }).then(response => {
          this.loading = false;
          const url = URL.createObjectURL(new Blob([response.data]));
          this.processedImageUrl = url;
          this.$store.dispatch('setProcessedImageURL', url);     
        }).catch(error => {
          console.error('Error:', error);
          this.loading = flase;
        });
      },
      downloadImage() {
        const link = document.createElement('a');
        link.href = this.processedImageUrl;
        link.download = 'processed-image.png'; // 可以根据需要修改文件名
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      },
      navigateToMagicAnimate() {
        // 使用编程式导航跳转到 /magicanimate 路径
        this.$router.push({ path: '/creationplatform' });
      },
      setImageClickCoords(event) {
        const imageElement = event.target;

        // 获取图片显示的尺寸
        const displayedWidth = imageElement.offsetWidth;
        const displayedHeight = imageElement.offsetHeight;

        // 获取图片的原始尺寸
        const naturalWidth = imageElement.naturalWidth;
        const naturalHeight = imageElement.naturalHeight;

        // 计算缩放比例
        const scaleX = naturalWidth / displayedWidth;
        const scaleY = naturalHeight / displayedHeight;

        // 获取点击的坐标（相对于图片显示的尺寸）
        const rect = event.target.getBoundingClientRect();
        let x = event.clientX - rect.left;
        let y = event.clientY - rect.top;
        // 调整坐标以匹配原图尺寸
        x = Math.round(x * scaleX);
        y = Math.round(y * scaleY);

        // 更新坐标数据
        this.pointCoords = `${x},${y}`;

        // 更新点击效果的位置和显示状态
        this.clickEffectStyle = {
          left: `${x / scaleX}px`, // 这里需要根据缩放调整回去，以便效果在正确的位置显示
          top: `${y / scaleY}px`, // 这里需要根据缩放调整回去，以便效果在正确的位置显示
          transform: 'translate(-50%, -50%)',
        };
        this.showClickEffect = true;
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
  .image-uploader {
    text-align: center;
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

  .image-preview, .processed-image {
    min-height: 300px; /* 设置最小高度 */
    display: flex;
    justify-content: center;
    align-items: center;
    border: 2px dashed #ccc; /* 添加虚线边框作为占位符 */
    border-radius: 5px; /* 轻微圆角 */
    background-color: #f8f9fa; /* 轻灰色背景 */
    position: relative;
    overflow: hidden;
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
    padding: 20px; /* 给上传器部分添加一些内边距 */
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
    z-index: 2; /* 确保点击效果显示在图片上方 */
  }
  .bg-img-with-overlay {
    background-image: url('/img/culture/tiantan.jpg');
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
  .upload-card-bg {
    background: linear-gradient(135deg, #1385BB, #4AB9EE);
    border-radius: 5px; /* 轻微的圆角效果 */
}
.upload-card-bg h2, .upload-card-bg {
  color: #ffffff; /* 白色文字 */
}
.processed-placeholder {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px; /* 设置一个最小高度 */
  background-color: #17a2b8; /* 自定义背景色 */
  color: #ffffff; /* 文字颜色 */
  border-radius: 5px; /* 圆角效果 */
  text-align: center;
  font-size: 20px;
}

@font-face {
  font-family: yishuzi;
  src: url('/img/ziti/汉仪瑞鹤.ttf') format('truetype');
}
@font-face {
  font-family: laolao;
  src: url('/img/ziti/姥姥字体.ttf') format('truetype');
}
.shopname{
  font-family: yishuzi;
  font-size: 45px;
  font-weight: 3500;
  color: rgb(255, 255, 255);
}
.title-style{
  font-family: laolao;
  font-size: 22px;
  font-weight: 3000;
  color: rgb(3, 3, 3);
}
.custom-button {
  background-color: #02078e; /* 自定义的背景色 */
  color: white; /* 文本色 */
}
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
  </style>


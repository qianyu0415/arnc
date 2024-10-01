<template>
  <div>
    <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
        <h1 class="text-white shopname">背景选取</h1>
        <b-button variant="info" @click="showIntroModal" class="mt-3 custom-button">功能介绍</b-button>
      </base-header>
    <b-container fluid class="mt-3">
      <b-row>
        <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer>
          <div class="text-style">
            请在下面“预留背景”中选取喜欢的图片作为背景；
            或者从“用户个人背景”中加载您仓库中的图片（古境留韵中生成）
         </div>
          </b-modal>
      </b-row>
    </b-container>
    <b-container fluid class="image-uploader mt-4">
      <b-row>
        <b-col md="12">
          <b-card no-body class="image-card-bg custom-card">
            <b-tabs card>
              <!-- Predefined Images Tab -->
              <b-tab title="预设背景" class="image-card-bg">
                <div class="gallery">
                  <div v-for="image in paginatedPredefinedImages" :key="image.id" @click="selectImage(image.id)"
                      :class="{'selected': selectedImageId === image.id.toString()}" class="gallery-item">
                      <img :src="image.url" :alt="`Image ${image.id}`" class="img-thumbnail cursor-pointer">
                  </div>
                </div>
                <div class="pagination-container">

                <b-pagination v-model="imagePage" :total-rows="predefinedImages.length" :per-page="perPage" @change="updateImagePage" class="my-4" limit="3"></b-pagination>
                </div>
              </b-tab>
              <!-- Fetched Images Tab -->
              <b-tab title="用户个人背景" class="image-card-bg">
                <b-button @click="fetchImages" variant="info" class="mb-2">点击加载</b-button>
                <div class="gallery">
                  <div v-for="image in paginatedFetchedImages" :key="image.id" @click="selectImage(image.id)"
                      :class="{'selected': selectedImageId === image.id.toString()}" class="gallery-item">
                      <img :src="image.url" :alt="`Fetched Image ${image.id}`" class="img-thumbnail cursor-pointer">
                  </div>
                </div>
                <div class="pagination-container">
                <b-pagination v-model="fetchedImagesPage" :total-rows="fetchedImages.length" :per-page="perPageFetchedImages" @change="updateFetchedImagePage" class="my-4" limit="3"></b-pagination>
                </div>
              </b-tab>
            </b-tabs>
          </b-card>
        </b-col>
        <b-col cols="12">
          <div class="text-center">
            <b-form @submit.prevent="submitSelectedImageId">
              <!-- <b-form-input v-model="selectedImageId" placeholder="选择背景编号" class="mb-2 text-center" readonly></b-form-input> -->
              <b-button type="submit" variant="primary custom-button">上传背景</b-button>
            </b-form>
          </div>
        </b-col>
      </b-row>
      <b-row v-if="errorMessage">
        <b-col>
          <b-alert variant="danger" show>{{ errorMessage }}</b-alert>
        </b-col>
      </b-row>
    </b-container>
    <b-modal id="error-modal" v-model="errorModalShow" title="温馨提示" ok-only @hide="errorModalShow = false">
  <div>{{ errorMessage }}</div>
</b-modal>

  </div>
</template>

  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
            // 其他数据属性
        errorMessage: '', // 用于存储和显示错误信息
        errorModalShow: false, // 控制错误提示弹窗的显示
        introModalShow:false,   //定义弹窗
        selectedImageId: '',
        perPage: 3, // 每页显示的项目数量
        imagePage: 1, // 当前图片页码
        videoPage: 1, // 当前视频页码
        fetchedImagesPage: 1, // 当前“Fetched Images”的页码
        perPageFetchedImages: 3, // 每页显示的“Fetched Images”数量
        predefinedImages: [
          // 示例预定义图片
          { id: '/root/autodl-tmp/arnc_project/arnc/static/images/bg/2.png',
             url: 'img/timescroll/002.jpg'
             },
             { id: '/root/autodl-tmp/arnc_project/arnc/static/images/bg/4.jpg',
          url: 'img/timescroll/004.jpg'
          },
          { id: '/root/autodl-tmp/arnc_project/arnc/static/images/bg/1.jpg',
            url: 'img/timescroll/001.jpg',
            },

          { id: '/root/autodl-tmp/arnc_project/arnc/static/images/bg/5.png',
          url: 'img/timescroll/005.png'
          },
          { id: '/root/autodl-tmp/arnc_project/arnc/static/images/bg/6.jpg',
          url: 'img/timescroll/006.jpg'
          },
          { id: '/root/autodl-tmp/arnc_project/arnc/static/images/bg/7.jpg',
          url: 'img/timescroll/007.jpg'
          },
        ],
        videos: [], // 确保定义了videos数组，即使它暂时为空
        fetchedImages: [],
      };
    },
    mounted(){
      this.showIntroModal()   //自动调用显示功能的弹窗
    },
    computed: {
      // 计算当前页的预定义图片
      paginatedPredefinedImages() {
        const start = (this.imagePage - 1) * this.perPage;
        const end = start + this.perPage;
        return this.predefinedImages.slice(start, end);
      },
      // 计算当前页的获取的图片
      paginatedFetchedImages() {
        const start = (this.fetchedImagesPage - 1) * this.perPageFetchedImages;
        const end = start + this.perPageFetchedImages;
        return this.fetchedImages.slice(start, end);
      },
    },

    methods: {
    // 更新图片分页
    updateImagePage(pageNumber) {
      this.imagePage = pageNumber;
    },
    updateFetchedImagePage(newPage) {
      this.fetchedImagesPage = newPage;
    },
    showIntroModal() {
      this.introModalShow = true; // 新增，显示功能介绍弹窗
    },
    fetchImages() {
        axios.get(`${process.env.VUE_APP_API_URL}/select-bg`)
        .then(response => {
            this.fetchedImages = response.data.map((item) => {
                const dir = Object.keys(item)[0]; // 获取字典的键，即文件目录作为id
                const relativeUrl = item[dir]; // 获取字典的值，即相对URL路径
                const url = `${process.env.VUE_APP_API_URL}${relativeUrl}`; // 构造完整的URL
                // 打印图片的ID和URL到控制台
                console.log(`ID: ${dir}, URL: ${url}`);
                return { id: dir, url: url };
            });
            })
            .catch(error => {
            console.error('Error fetching images:', error);
            this.errorMessage = 'Failed to load images.';
            });
        },
      selectImage(id) {
        // 判断当前点击的图片ID是否已经被选中
        if (this.selectedImageId === id.toString()) {
        // 如果已经选中，则清空selectedImageId以取消选择
        this.selectedImageId = '';
        } else {
        // 如果没有选中，则更新selectedImageId为当前点击的图片ID
        this.selectedImageId = id.toString();
        }
    },
    submitSelectedImageId() {
        // 检查是否已选择图片
        if (!this.selectedImageId) {
          // 设置错误消息
          this.errorMessage = '请先选择一张图片。';
          // 显示错误提示弹窗
          this.errorModalShow = true;
          return; // 停止方法执行
        }

        // 如果有选中的图片，继续处理
        const formData = new FormData();
        formData.append('bg_path', this.selectedImageId);
        sessionStorage.setItem('bg_path', JSON.stringify(this.selectedImageId));

        // 这里添加发送到后端的代码或其他逻辑
        console.log('Submitting ID:', this.selectedImageId);

        // 假设所有处理均成功，跳转到下一个页面
        this.$router.push({ name: 'creationplatform' });
      },
    },
  };
  </script>
  
  <style scoped>
.gallery {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center; /* 添加这行来确保垂直居中 */
}

.gallery-item {
  flex: 0 0 calc(33% - 20px); /* 为每个项目分配25%的宽度，并减去边距 */
  margin: 10px;
  text-align: center; /* 确保图片居中 */
}
  .image-uploader {
    text-align: center;
  }
  
  .img-thumbnail {
    max-width: 100%; /* 确保图片宽度自适应容器宽度 */
    height: auto;
    margin: 5px;
  }
  
  .cursor-pointer {
    cursor: pointer;
  }
  
  .checkmark-container {
    display: none; /* 默认隐藏，通过JavaScript动态显示 */
  }
  
  .p-2 {
    position: relative;
    display: inline-block;
  }
  
  .gallery-item.selected {
    border: 2px solid #030303; /* 选中项显示蓝色边框 */
    padding: 4px; /* 调整内边距以避免边框覆盖图片 */
  }
  
  @media (min-width: 768px) {
  .gallery-item {
    width: calc(50% - 20px); /* 在较大屏幕上设置为横向分布，每行两个图片 */
  }
}

@media (max-width: 767px) {
  .gallery-item {
    width: calc(100% - 20px); /* 在较小屏幕上保持单列显示 */
  }
}
.pagination-centered {
  display: flex;
  justify-content: center;
}
.pagination-container {
  display: flex;
  justify-content: center;
}
.bg-img-with-overlay {
    background-image: url('/img/culture/tengwangge.jpg');
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
    background: linear-gradient(135deg, #6db6fe, #b3e8ff, #a7ecf6);
    border-radius: 5px; /* 轻微圆角 */
  }
  .img-thumbnail {
    max-height: 450px; /* 根据需要调整 */
    width: auto; /* 保持宽高比 */
  }
.custom-card .card-body {
  padding: 0.5rem; /* 减少内边距 */
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
  background-color: #02078e; /* 自定义的背景色 */
  color: white; /* 文本色 */
}
::v-deep .nav-tabs .nav-link {
  font-family: 'laolao', sans-serif;
}
.nav-tabs .nav-link {
  font-family: 'laolao', sans-serif;
}


  </style>
  
  

  
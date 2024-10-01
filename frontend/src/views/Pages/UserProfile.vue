<template>
  <div>
    <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
      <h1 class="display-2 text-white shopname">你好, {{ userName }}</h1>
      <p class="text-white mt-0 mb-5 text-style">这是您的个人仓库，在这里面您可以看到生成过的视频和照片。</p>
    </base-header>
    <!-- Navigation Bar -->
    <!-- Main Content -->
    <b-container fluid class="mt--6">
      <b-row>
        <b-container fluid class="mt-6">
          <b-tabs v-model="activeTab" card>
            <b-tab title="古境留韵" >
              <b-row>
                <b-col md="4" sm="6" v-for="bg in paginatedBgs" :key="bg.id" class="mb-3">
                  <b-card class="media-card" :img-src="bg.url" img-alt="Background image" img-top @click="openFullScreen(bg.url)" ></b-card>
                </b-col>
              </b-row>
              <b-pagination v-model="bgsPage" :total-rows="bgsList.length" :per-page="perPage" align="center"></b-pagination>
            </b-tab>
            <b-tab title="时光绘卷" >
            <b-row>
              <b-col md="4" v-for="video in paginated3DVideos" :key="video.id" class="mb-3">
                <video class="media-card" width="100%" controls @click="openFullScreen(video.url)" height="500px">
                  <source :src="video.url" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
              </b-col>
            </b-row>
            <b-pagination v-model="threeDVideosPage" :total-rows="video3DList.length" :per-page="perPage" align="center"></b-pagination>
          </b-tab>
          <b-tab title="墨舞千秋" >
            <b-row>
              <b-col md="4" v-for="video in paginatedMAVideos" :key="video.id" class="mb-3">
                <video class="media-card" width="100%" controls @click="openFullScreen(video.url)">
                  <source :src="video.url" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
              </b-col>
            </b-row>
            <b-pagination v-model="maVideosPage" :total-rows="videoMAList.length" :per-page="perPage" align="center"></b-pagination>
          </b-tab>
          </b-tabs>
        </b-container>
</b-row>
</b-container>

  </div>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      userName: '',
      userEmail: '',
      video3DList: [],
      videoMAList: [],
      bgsList: [],
      perPage: 3, 
      bgsPage: 1,
      maVideosPage: 1,
      threeDVideosPage: 1,
      activeTab: 0, 
    };
  },
  computed: {
    paginatedBgs() {
      const start = (this.bgsPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.bgsList.slice(start, end);
    },
    paginatedMAVideos() {
      const start = (this.maVideosPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.videoMAList.slice(start, end);
    },
    paginated3DVideos() {
      const start = (this.threeDVideosPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.video3DList.slice(start, end);
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    openFullScreen(url) {
      const videoWin = window.open(url, '_blank');
      videoWin.onload = function() {
        const video = this.document.getElementsByTagName('video')[0];
        if (video.requestFullscreen) {
          video.requestFullscreen();  // 触发全屏
        }
        video.play();  // 自动播放
      }
    },
    setActiveTab(tabIndex) {
      this.activeTab = tabIndex; // 设置当前激活的 Tab 索引

    },
    fetchData() {
      axios.get(`${process.env.VUE_APP_API_URL}/user`)
        .then(response => {
          const { name, email, Video3D, VideoMA, Backgrounds } = response.data;
          this.userName = name;
          this.userEmail = email;
          this.video3DList = Video3D.map(video => ({
            id: video.id,
            url: `${process.env.VUE_APP_API_URL}${video.url}`
          }));
          console.log(this.video3DList);
          this.videoMAList = VideoMA.map(video => ({
            id: video.id,
            url: `${process.env.VUE_APP_API_URL}${video.url}`
          }));
          console.log(this.videoMAList);
          this.bgsList = Backgrounds.map(bg => ({
            id: bg.id,
            url: `${process.env.VUE_APP_API_URL}${bg.url}`
          }));
        })
        .catch(error => {
          console.error("There was an error fetching the data:", error);
        });
    }
  }
};
</script>
<style>
.pagination-centered {
  display: flex;
  justify-content: center;
}
.bg-img-with-overlay {
  background-image: url('/img/culture/xingkong.jpg') ;
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
.media-card img {
  width: 100%; /* 保持宽度与卡片相同 */
  height: 600px; /* 设置一个固定高度 */
  object-fit: cover; /* 覆盖整个内容区域，可能会裁剪部分内容 */
}
.media-card video {
  width: 100%; /* 保持宽度与卡片相同 */
  height: 200px; /* 设置一个固定高度 */
}

.media-card {
  cursor: pointer; /* 提示用户这是可点击的 */
}

.text-style{
  font-family: laolao;
  font-size: 30px;
  font-weight: 3000;
  color: rgb(3, 3, 3);
}
.shopname{
  font-family: yishuzi;
  font-size: 45px;
  font-weight: 3500;
  color: rgb(255, 255, 255);
}
  ::v-deep .nav-tabs .nav-link {
    font-family: 'laolao', sans-serif;
  }
  .nav-tabs .nav-link {
    font-family: 'laolao', sans-serif;
  }
</style>
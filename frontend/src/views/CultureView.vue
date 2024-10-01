<template>
  <div>
    <base-header class="pb-3 pb-4 pt-3 pt-md-8 bg-img-with-overlay d-flex align-items-center justify-content-center">
      <h1 class="text-white shopname">名画赏析</h1>
      <b-button variant="info" @click="showIntroModal" class="mt-3 custom-button">功能介绍</b-button>
    </base-header>
    <b-container fluid class="mt-3">
      <b-row id="my-gallery">
        <b-col md="6" lg="4" v-for="(item, index) in paginatedItems" :key="index" class="mb-4">
          <b-card class="h-100 shadow-sm hover-shadow bg-card">
            <b-card-img :src="item.imgUrl" :alt="item.title" top @click="showModal(item)"></b-card-img>
            <b-card-body >
              <b-card-title class="title-style">{{ item.title }}</b-card-title>
              <b-card-text class="text-style">{{ item.description }}</b-card-text>
            </b-card-body>
            <b-card-footer class="bg-card">
              <b-button variant="primary custom-button" @click="showModal(item)">查看</b-button>
            </b-card-footer>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
    <b-pagination
      v-model="currentPage"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="my-gallery"
      class="mb-4 d-flex justify-content-center"
    ></b-pagination>
    <b-modal v-model="modalShow" size="lg">
      <template #modal-header="{ close }">
        <h5>{{ currentImage.title }}</h5>
        <b-button size="sm" variant="outline-danger" @click="close">关闭</b-button>
      </template>
      <img :src="currentImage.imgUrl" :alt="currentImage.title" class="img-fluid">
    </b-modal>
    <b-modal id="intro-modal" v-model="introModalShow" title="功能介绍" hide-footer>
      <div class="text-style">
        欢迎来到“古韵流光——中国古代名画赏析”，一个专为艺术爱好者和历史探索者量身打造的虚拟展览。在这里，我们将带你穿越时空，
        体验那些定格在画卷中、传承千年的中国古代美学精髓。
      </div>
    </b-modal>
  </div>
</template>
<script>
export default {
  data() {
    return {
      perPage:3,
      currentPage:1,
      galleryItems: [
      {
        title: "富春山居图 【元·黄公望】",
        description: "此画以横幅长卷的形式描绘了富春江两岸秀丽的山光水色。峰峦坡石随势起伏，山涧深处清泉飞泻。在群山环抱中，茅屋村舍参差其间，渔舟小桥错落有致，真可谓人随景迁、景随人移。",
        imgUrl: '/img/culture/fuchunshanjutu.png',
      },
      {
        title: "洛神赋图 【晋·顾恺之】",
        description: "在平静的水面上，风姿绝世、含情脉脉的洛神衣带飘逸、动态从容，凌波而来。柳岸边，曹植身体微微前倾，伸出双手挡住众随从。随从们目光呆滞，而曹植目光灼灼地注视着前方水面上美丽的洛神。",
        imgUrl: '/img/culture/luoshenfutu.png', 
      },
      {
        title: "百骏图 【清·郎世宁】",
        description: "此图共绘有100匹骏马，姿势各异，或立、或奔、或跪、或卧，可谓曲尽骏马之态。画面的首尾各有牧者数人，控制着整个马群，体现了一种人与自然界其他生物间的和谐关系。",
        imgUrl: '/img/culture/baijuntu.png',
      },
      {
        title: "韩熙载夜宴图 【五代·顾闳中】",
        description: "作品如实地再现了南唐大臣韩熙载夜宴宾客的历史情景，细致地描绘了宴会上弹丝吹竹、清歌艳舞、主客揉杂、调笑欢乐的热闹场面，又深入地刻画了主人公超脱不羁、沉郁寡欢的复杂性格。",
        imgUrl: "/img/culture/hanxizaiyeyantu.png",
      },
      {
        title: "步辇图 【唐·阎立本】",
        description: "李世民端坐在由六名宫女抬着的步辇上，另有三个宫女分别在前后掌扇和持华盖。唐太宗面前站立三人：最右者，身穿大红袍，是这次仪式的引见官员；中间是吐蕃的使臣禄东赞，拱手而立，发型和服饰与中原地区不同；最左为一穿白袍的内官。",
        imgUrl: "/img/culture/buniantu.jpg",
      },
      ],
      modalShow: false,
      currentImage: {},
      introModalShow:false,
    };
  },
  mounted(){
      this.showIntroModal()   //自动调用显示功能的弹窗
    },
  computed: {
    rows() {
      return this.galleryItems.length;
    },
    paginatedItems() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.galleryItems.slice(start, end);
    }
  },
  methods: {
    showModal(item) {
      this.currentImage = item;
      this.modalShow = true;
    },
    showIntroModal() {
      this.introModalShow = true; // 新增，显示功能介绍弹窗
    }
  }
};
</script>
<style scoped>

.custom-button:hover {
    background-color: #338EB8;  
}

.hover-shadow {
  transition: box-shadow 0.3s;
}
.hover-shadow:hover {
  box-shadow: 0 0 11px rgba(33, 33, 33, 0.2);
}
.bg-img-with-overlay {
  background-image: url('/img/culture/gugong.jpg');
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
.custom-button {
  background-color: #020568; /* 自定义的背景色 */
  color: white; /* 文本色 */
}
.bg-card{
  background-color:#3CA4D6;
}
@font-face {
  font-family: yishuzi;
  src: url('/img/ziti/汉仪瑞鹤.ttf') format('truetype');
}
@font-face {
  font-family: laolao;
  src: url('/img/ziti/姥姥字体.ttf') format('truetype');
}
.title-style{
  font-size: 22px;
  font-weight: 3000;
  color: rgb(3, 3, 3);
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


</style>

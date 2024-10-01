<template>
  <div class="header">
    <!-- Header -->
    <div class="py-4 py-lg-6 pt-lg-4">
      <b-container>
        <button @click="goToHomePage" class="back-to-home-btn text-style">返回主页</button>
        <div class="header-body text-center mb-7">
          <b-row class="justify-content-center">
            <b-col xl="5" lg="6" md="8" class="px-5">
              <h1 class="text-white shopname">欢迎！</h1>
            </b-col>
          </b-row>
        </div>
      </b-container>
      <div class="separator separator-bottom separator-skew zindex-100">
        <svg x="0" y="0" viewBox="0 0 2560 100" preserveAspectRatio="none" version="1.1"
             xmlns="http://www.w3.org/2000/svg">
          <polygon class="fill-default" points="2560 0 2560 100 0 100"></polygon>
        </svg>
      </div>
    </div>
    <!-- Page content -->
    <b-container class="mt--8 pb-5">
      <b-row class="justify-content-center">
        <b-col lg="5" md="7">
          <b-card no-body class="border-0 mb-0 form-card-transparent">
            <b-card-body class="px-lg-5 py-lg-5 form-card-body">
              <div class="text-center text-muted mb-4 custom-title-light">
                <small>使用个人信息登录</small>
              </div>
              
              <b-form @submit.prevent="onSubmit">
                  <base-input alternative
                              class="mb-3"
                              name="Email"
                              :rules="{required: true, email: true}"
                              prepend-icon="ni ni-email-83"
                              placeholder="邮箱"
                              v-model="model.email">
                  </base-input>

                  <base-input alternative
                              class="mb-3"
                              name="Password"
                              :rules="{required: true, min: 6}"
                              prepend-icon="ni ni-lock-circle-open"
                              type="password"
                              placeholder="密码"
                              v-model="model.password">
                  </base-input>
                  <div class="text-center">
                    <base-button native-type="submit" class="custom-bg-color">登录</base-button>
                  </div>
                </b-form>

            </b-card-body>
          </b-card>
          <b-row class="mt-3">
            <b-col cols="3" class="text-right">
              <router-link to="/register" class="text-light custom-text-light"><small>创建账号</small></router-link>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
    </b-container>
    <!-- Error Modal -->
    <b-modal id="error-modal" title="登录错误" hide-footer>
      <p class="mb-0">{{ errorMessage }}</p>
    </b-modal>
  </div>
</template>
<script>
import axios from 'axios';  //引入axios
export default {
  data() {
    return {
      model: {
        email: '',
        password: '',
        rememberMe: false
      },
      apiUrl:process.env.VUE_APP_API_BASE_URL,
      errorMessage: '' // 用于存储和显示错误信息
    };
  },
  methods: {
    goToHomePage() {
      this.$router.push({ name: 'culture' }); // 使用路由名称跳转
    },

    onSubmit() {
      // 使用 FormData 或 JSON 根据后端需求
      const formData = new FormData();
      formData.append('email', this.model.email);
      formData.append('password', this.model.password);

      axios.post(`${process.env.VUE_APP_API_URL}/user/login`, formData)
        .then(response => {
          //假设JWT在response的data中的token字段
          const token = response.data.access_token;
          //存储JWT到LocalStorage
          if(token) {
            // 存储JWT到LocalStorage
            localStorage.setItem('userToken', token);
          导航到其他页面
          this.$router.push('/culture');
          } else {
            // 如果没有Token，可能需要处理错误
            this.errorMessage = '登录成功，但未接收到令牌。';
            this.$bvModal.show('error-modal');
          }

          导航到素材库页面
          this.$router.push('/culture');
        })
        .catch(error => {
          // Handle error response
          this.errorMessage = error.response && error.response.data && error.response.data.message
                        ? error.response.data.message
                        : '登录失败，请重试。';
          this.$bvModal.show('error-modal');
        });
    }
  }
};
</script>
<style>
.header {
  background-image: url('/img/culture/luoshenfutu.png');
  background-size: cover; /* 背景图覆盖整个元素 */
  background-position: center; /* 背景图居中 */
  padding-top: 1rem;
  padding-bottom: 9rem;
}
@font-face {
  font-family: yishuzi;
  src: url('/img/ziti/汉仪瑞鹤.ttf') format('truetype');
}
.shopname{
  font-family: yishuzi;
  font-size: 45px;
  font-weight: 3500;
  color: rgb(255, 255, 255);
}
.back-to-home-btn {
  position: absolute; /* 绝对定位 */
  top: 20px; /* 距离顶部20px */
  left: 20px; /* 距离左边20px */
  background-color: rgba(255, 255, 255, 0.5); /* 半透明的白色背景 */
  border: none; /* 无边框 */
  padding: 10px 20px; /* 内边距 */
  border-radius: 5px; /* 轻微的圆角 */
  cursor: pointer; /* 鼠标悬停时显示指针 */
}
.b-card {
  background-color: rgba(255, 255, 255, 0.5); /* 设置半透明背景 */
}
.form-card-transparent {
  background-image: linear-gradient(120deg, rgba(246, 211, 101, 0.2) 0%, rgba(253, 160, 133, 0.2) 100%), url('/img/culture/luoshenfutu.png');
  background-size: cover;
  background-position: center;
}
.form-card-body {
  background-color: rgba(132, 26, 26, 0); /* 半透明的白色背景 */
}
.custom-title-light{
  font-family: yishuzi;

  font-size: 30px; /* 修改字体大小 */
  color: #ffffff !important; /* 保留text-light的浅色字体，或者自定义颜色 */
}
.custom-text-light {
  font-family: yishuzi;

  font-size: 23px; /* 修改字体大小 */
  color: #ffffff !important; /* 保留text-light的浅色字体，或者自定义颜色 */
}
.custom-bg-color {
  background-color: #342c00; /* 您想要的背景颜色 */
  color: #ffffff;
}

</style>

<template>
  <div class="header">
    <div class="py-4 py-lg-6 pt-lg-4">
      <button @click="goToHomePage" class="back-to-home-btn text-style">返回主页</button>
      <b-container class="container">
        <div class="header-body text-center mb-7">
          <b-row class="justify-content-center">
            <b-col xl="5" lg="6" md="8" class="px-5">
              <h1 class="text-white shopname">创建账户</h1>
              <p class="text-lead text-white text-style">您可以免费创建一个账户，以便存储您的创作信息。</p>
            </b-col>
          </b-row>
        </div>
      </b-container>
    </div>
    <!-- Page content -->
    <b-container class="mt--9 pb-5">
      <!-- Table -->
      <b-row class="justify-content-center">
        <b-col lg="6" md="8" >
          <b-card no-body class="border-0 form-card-transparent" >
            <!-- <b-card-header class="bg-transparent pb-5">
              <div class="text-muted text-center mt-2 mb-4"><small>Sign up with</small></div>
              <div class="text-center">
                <a href="#" class="btn btn-neutral btn-icon mr-4">
                  <span class="btn-inner--icon"><img src="img/icons/common/github.svg"></span>
                  <span class="btn-inner--text">Github</span>
                </a>
                <a href="#" class="btn btn-neutral btn-icon">
                  <span class="btn-inner--icon"><img src="img/icons/common/google.svg"></span>
                  <span class="btn-inner--text">Google</span>
                </a>
              </div>
            </b-card-header> -->
            <b-card-body class="px-lg-5 py-lg-5 form-card-body">
              <div class="text-center text-muted mb-4 custom-title-light">
                <small>填写信息注册新账号</small>
              </div>
              <!-- <validation-observer v-slot="{handleSubmit}" ref="formValidator"> -->
                <b-form @submit.prevent="onSubmit">
                  <base-input alternative
                              class="mb-3"
                              prepend-icon="ni ni-hat-3"
                              placeholder="姓名"
                              name="name"
                              :rules="{required: true}"
                              v-model="model.name">
                  </base-input>

                  <base-input alternative
                              class="mb-3"
                              prepend-icon="ni ni-email-83"
                              placeholder="电子邮箱"
                              name="email"
                              :rules="{required: true, email: true}"
                              v-model="model.email">
                  </base-input>

                  <base-input alternative
                              class="mb-3"
                              prepend-icon="ni ni-lock-circle-open"
                              placeholder="密码"
                              type="password"
                              name="Password"
                              :rules="{required: true, min: 6}"
                              v-model="model.password">
                  </base-input>
                  <b-row class=" my-4">
                  </b-row>
                  <div class="text-center">
                    <b-button type="submit" class="custom-button">创建账户</b-button>
                  </div>
                </b-form>
              <!-- </validation-observer> -->
            </b-card-body>
          </b-card>
          <b-modal id="errorModal" title="注册错误">
            <p class="mb-0">{{ errorMessage }}</p>
          </b-modal>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import axios from 'axios';

  export default {
    name: 'register',
    data() {
      return {
        model: {
          name: '',
          email: '',
          password: '',
        },
        isSubmitAttempted: false, // 新增：标记是否尝试提交表单
        errorMessage: '', // 用于显示错误消息
              // 新增验证状态
        emailValid: true,
        passwordValid: true,
      }
    },
    methods: {
    goToHomePage() {
      this.$router.push({ name: 'culture' }); // 使用路由名称跳转
    },
    onSubmit() {
      // 标记为尝试提交
      this.isSubmitAttempted = true;
      this.passwordValid = this.model.password.length >= 6;
      const formData = new FormData();
      formData.append('name', this.model.name);
      formData.append('email', this.model.email);
      formData.append('password', this.model.password);

      axios.post(`${process.env.VUE_APP_API_URL}/user/register`, formData)
        .then(response => {
          this.$router.push({ name: 'login' }); // 假设登录路由的名称为'login'
        })
        .catch(error => {
          // 注册失败时的处理
          this.handleRegistrationError(error);
        });
    },
    handleRegistrationError(error) {
      if (error.response && error.response.data) {
        // 显示后端返回的错误消息
        this.errorMessage = error.response.data.error;
      } else {
        this.errorMessage = '发生了未知错误。';
      }
      this.$bvModal.show('errorModal');
    },
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
.form-card-body {
  background-color: rgba(132, 26, 26, 0); /* 半透明的白色背景 */
}
.custom-title-light{
  font-family: laolao;

  font-size: 30px; /* 修改字体大小 */
  color: #ffffff !important; /* 保留text-light的浅色字体，或者自定义颜色 */
}
.custom-button{
  background-color: #342c00; /* 您想要的背景颜色 */
  color: #ffffff;
}


</style>

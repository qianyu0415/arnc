/*!

=========================================================
* BootstrapVue Argon Dashboard - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/bootstrap-vue-argon-dashboard
* Copyright 2020 Creative Tim (https://www.creative-tim.com)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Vue from 'vue';
import DashboardPlugin from './plugins/dashboard-plugin';
import App from './App.vue';
import VueLazyload from 'vue-lazyload';
import { store } from '../store'; // 使用正确的路径导入store
import '@google/model-viewer';


// router setup
import router from './routes/router';
import axios from 'axios';


//为了在后续请求中携带JWT，使用axios设置一个全局的请求拦截器，每次请求都会加上Authorization头
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('userToken');
    if (token) {
      config.headers['Authorization'] = 'Bearer ' + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
//处理过期的JWT
// axios.interceptors.response.use(response => {
//   return response;
// }, error => {
//   if (error.response && error.response.status === 401) {
//     // 如果用户未授权（例如，令牌过期），则重定向到登录页
//     localStorage.removeItem('userToken'); // 清除过期的或无效的令牌
//     router.push('/login');
//   }
//   return Promise.reject(error);
// });
// router.beforeEach((to, from, next) => {
//   const publicPages = ['/login', '/register']; // 公开访问的页面路径
//   const authRequired = !publicPages.includes(to.path); // 需要认证的页面
//   const loggedIn = localStorage.getItem('userToken'); // 检查是否存储了Token

  // 尝试访问需要认证的页面但没有登录
//   if (authRequired && !loggedIn) {
//     return next('/login');
//   }

//   next(); // 确保一定要调用 next()
// });
// plugin setup
Vue.use(DashboardPlugin);
Vue.use(VueLazyload);
// 忽略model-viewer组件，防止Vue给出未知元素的警告
Vue.config.ignoredElements = ['model-viewer'];

/* eslint-disable no-new */
new Vue({
  router,
  store, // 使用 store
  render: h => h(App)
}).$mount('#app');
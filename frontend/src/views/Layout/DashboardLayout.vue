<template>
  <div class="wrapper">
    <notifications></notifications>
    <side-bar class="base-nav">
      <template slot="links">
        <sidebar-item
          :link="{
            name: '古韵流光',
            path: '/culture',
            icon: 'ni ni-istanbul',
          }"
        >
        </sidebar-item>
        <sidebar-item
              :link="{
                name: '古境留韵',
                path: '/ia',
                icon: 'ni ni-bulb-61'
              }">
        </sidebar-item>
        <sidebar-item
                  :link="{
                    name: '时光绘卷',
                    path: '/timescroll',
                    icon: 'ni ni-planet'
                  }">
        </sidebar-item>
        <sidebar-item
              :link="{
                name: '墨舞千秋',
                path: '/magicanimate',
                icon: 'ni ni-palette'
              }">
        </sidebar-item>
        <sidebar-item
              :link="{
                name: '个人中心',
                path: '/profile',
                icon: 'ni ni-single-02 text-yellow'
                }">
        </sidebar-item>

        <sidebar-item
                  :link="{
                    name: '登录',
                    path: '/login',
                    icon: 'ni ni-key-25 text-info'
                  }">
        </sidebar-item>
        <sidebar-item
                  :link="{
                    name: '注册',
                    path: '/register',
                    icon: 'ni ni-circle-08 text-pink'
                  }">
        </sidebar-item>
      </template>
    </side-bar>
    <div class="main-content">
      <dashboard-navbar :type="$route.meta.navbarType"></dashboard-navbar>

      <div @click="$sidebar.displaySidebar(false)">
        <fade-transition :duration="200" origin="center top" mode="out-in">
          <!-- your content here -->
          <router-view></router-view>
        </fade-transition>
      </div>
      <content-footer v-if="!$route.meta.hideFooter"></content-footer>
    </div>
  </div>
</template>
<script>
  /* eslint-disable no-new */
  import PerfectScrollbar from 'perfect-scrollbar';
  import 'perfect-scrollbar/css/perfect-scrollbar.css';

  function hasElement(className) {
    return document.getElementsByClassName(className).length > 0;
  }

  function initScrollbar(className) {
    if (hasElement(className)) {
      new PerfectScrollbar(`.${className}`);
    } else {
      // try to init it later in case this component is loaded async
      setTimeout(() => {
        initScrollbar(className);
      }, 100);
    }
  }

  import DashboardNavbar from './DashboardNavbar.vue';
  import ContentFooter from './ContentFooter.vue';
  import DashboardContent from './Content.vue';
  import { FadeTransition } from 'vue2-transitions';

  export default {
    components: {
      DashboardNavbar,
      ContentFooter,
      DashboardContent,
      FadeTransition
    },
    methods: {
      initScrollbar() {
        let isWindows = navigator.platform.startsWith('Win');
        if (isWindows) {
          initScrollbar('sidenav');
        }
      }
    },
    mounted() {
      this.initScrollbar()
    }
  };
</script>
<style lang="scss">
.base-nav{
  background: linear-gradient(135deg, #6db6fe, #b3e8ff, #a7ecf6);
  background-size: cover; /* 保持渐变覆盖整个容器 */
  background-position: center; /* 渐变居中显示 */
}

</style>


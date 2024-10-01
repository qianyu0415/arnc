<template>
  <nav class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light bg-white" id="sidenav-main">
      <div class="container-fluid">

          <!--Toggler-->
          <navbar-toggle-button @click.native="showSidebar">
              
          </navbar-toggle-button>
          <router-link class="navbar-brand" to="/">
              <img :src="logo" class="navbar-brand-img" alt="...">
          </router-link>

        
          <slot></slot>
          <div v-show="$sidebar.showSidebar" class="navbar-collapse collapse show" id="sidenav-collapse-main">

              <div class="navbar-collapse-header d-md-none">
                  <div class="row">
                      <div class="col-6 collapse-brand">
                          <router-link to="/">
                              <img :src="logo">
                          </router-link>
                      </div>
                      <div class="col-6 collapse-close">
                          <navbar-toggle-button @click.native="closeSidebar"></navbar-toggle-button>
                      </div>
                  </div>
              </div>

              <ul class="navbar-nav">
                  <slot name="links">
                  </slot>
              </ul>
              <!--Divider-->
              <hr class="my-3">
              <!--Heading-->

              
          </div>
          </div>
  </nav>
</template>
<script>
import NavbarToggleButton from '@/components/NavbarToggleButton'

export default {
  name: 'sidebar',
  components: {
    NavbarToggleButton
  },
  props: {
    logo: {
      type: String,
      default: 'img/brand/logo1.png',
      description: 'Sidebar app logo'
    },
    autoClose: {
      type: Boolean,
      default: true,
      description: 'Whether sidebar should autoclose on mobile when clicking an item'
    }
  },
  provide() {
    return {
      autoClose: this.autoClose
    };
  },
  methods: {
    closeSidebar() {
      this.$sidebar.displaySidebar(false)
    },
    showSidebar() {
      this.$sidebar.displaySidebar(true)
    }
  },
  beforeDestroy() {
    if (this.$sidebar.showSidebar) {
      this.$sidebar.showSidebar = false;
    }
  }
};
</script>

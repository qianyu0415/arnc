<template>
  <div class="header" :class="{[`bg-${type}`]: type}">
     <b-container fluid>
      <div class="header-body">
        <slot></slot>
      </div>
     </b-container>
  </div>
</template>
<script>
  export default {
    name: 'base-header',
    props: {
      type: {
        type: String,
        default: 'success',
        description: 'Header background type'
      },
      bgImage: {
        type: String,
        default: '', // 默认没有背景图片
      }
    },
    computed: {
      bgImageStyle() {
        return this.bgImage ? {
          backgroundImage: `url('${this.bgImage}')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center center',
        } : {};
      },
    },
  }
</script>
<style>
</style>

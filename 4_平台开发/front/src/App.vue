<template>
  <div id="app" class="appClass">
    <router-view></router-view>
  </div>
</template>


<script>
export default {
  name: 'App'
}
</script >


<style scoped>
  .appClass{
    width: 100%;
    height: 100%;
    position:fixed;
    margin-top: -10px;/*上边距*/
    margin-left: -8px;/*左边距*/
    /*background-size:100% 100%;*/
  }
</style>

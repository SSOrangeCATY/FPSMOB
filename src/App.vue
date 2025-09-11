<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
// App组件仅作为路由容器
</script>

<style>
/* 全局样式重置 - 基础设置由style.css管理 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  width: 100%;
  min-height: 100vh;
}

/* 确保路由器视图占满整个容器 */
.router-view {
  width: 100%;
  height: 100%;
}
</style>

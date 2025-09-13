<template>
  <div class="live-container" :style="liveContainerStyle">
    <FPSLiveOverlay :config="configs" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import FPSLiveOverlay from '../components/FPSLiveOverlay.vue'
import axios from 'axios'

// 配置数据
const configs = ref({
  uiConfig: {
    showPlayerCards: true,
    showRoundInfo: true,
    showTeamScores: true,
    showTime: true,
    showAdCard: false,
    adCardConfig: {
      enabled: false,
      text: '',
      imageUrl: '',
      position: 'bottom-right',
      duration: 30,
      interval: 300
    }
  },
  styleConfig: {
    fontFamily: 'Arial, sans-serif',
    cssFile: 'default.css'
  },
  syncConfig: {
    syncMode: 'active',
    syncInterval: 5000,
    apiUrl: 'http://localhost:8080',
    apiKey: '',
    localFilePath: '',
    localFileInterval: 10
  }
})

// 实时容器样式
const liveContainerStyle = computed(() => {
  return {
    fontFamily: configs.value.styleConfig.fontFamily,
    position: 'relative',
    width: '100%',
    height: '100vh',
    overflow: 'hidden'
  }
})

// 从后端获取配置
async function loadConfigs() {
  try {
    const response = await axios.get('/api/config')
    configs.value = response.data
    applyCustomCSS()
  } catch (error) {
    console.error('加载配置失败:', error)
    // 使用默认配置继续运行
  }
}

// 应用自定义CSS
function applyCustomCSS() {
  // 移除旧的自定义样式
  const oldStyle = document.getElementById('fpsmob-custom-css')
  if (oldStyle) {
    oldStyle.remove()
  }
  
  // 加载外部CSS文件
  if (configs.value.styleConfig.cssFile) {
    const link = document.createElement('link')
    link.id = 'fpsmob-custom-css'
    link.rel = 'stylesheet'
    link.href = `/css/${configs.value.styleConfig.cssFile}`
    document.head.appendChild(link)
  }
}

// 初始化
onMounted(() => {
  loadConfigs()
})
</script>

<style>
/* 确保背景透明 */
body, #app {
  background-color: transparent;
  background-image: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.live-container {
  background-color: transparent;
}
</style>
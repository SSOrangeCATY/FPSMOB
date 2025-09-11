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
    showTime: true
  },
  styleConfig: {
    fontFamily: 'Arial, sans-serif',
    customCSS: ''
  },
  apiConfig: {
    apiUrl: 'http://localhost:8000',
    apiKey: '',
    refreshInterval: 5
  },
  syncConfig: {
    syncInterval: 5
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
  if (configs.value.styleConfig.customCSS) {
    // 移除旧的自定义样式
    const oldStyle = document.getElementById('fpsmob-custom-css')
    if (oldStyle) {
      oldStyle.remove()
    }
    
    // 添加新的自定义样式
    const style = document.createElement('style')
    style.id = 'fpsmob-custom-css'
    style.textContent = configs.value.styleConfig.customCSS
    document.head.appendChild(style)
  }
}

// 定期刷新配置
function startConfigRefresh() {
  // 每30秒刷新一次配置
  setInterval(() => {
    loadConfigs()
  }, 30000)
}

// 初始化
onMounted(() => {
  loadConfigs()
  startConfigRefresh()
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
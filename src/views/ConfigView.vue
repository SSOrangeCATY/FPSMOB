<template>
  <div class="config-container">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <h1>FPSMOB <span class="subtitle">配置中心</span></h1>
        <p class="header-desc">定制您的FPS游戏直播数据展示界面</p>
        <a href="/live" target="_blank" class="live-link-btn">
          <i class="icon-external-link"></i> 打开Live页面
        </a>
      </div>
    </header>
    
    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 分类导航 -->
      <div class="category-tabs">
        <button 
          v-for="category in categories" 
          :key="category.id"
          :class="['tab', { active: activeCategory === category.id }]"
          @click="switchCategory(category.id)"
        >
          <i :class="category.icon"></i>
          <span>{{ category.name }}</span>
        </button>
      </div>
      
      <!-- 配置内容区 -->
      <div class="config-content">
        <!-- API配置 -->
        <div v-if="activeCategory === 'api'" class="category-content">
          <!-- API设置卡片 -->
          <div class="card">
            <div class="card-header">
              <h2 class="section-title">
                <i class="icon-cog"></i> API配置
              </h2>
            </div>
            
            <div class="card-body">
              <div class="form-group">
                <label class="form-label" for="apiUrl">API地址</label>
                <input 
                  type="text" 
                  id="apiUrl" 
                  class="form-input" 
                  v-model="apiConfig.apiUrl"
                  placeholder="输入API地址，如 http://localhost:8080"
                >
              </div>
              
              <div class="form-group">
                <label class="form-label" for="apiKey">API密钥</label>
                <input 
                  type="password" 
                  id="apiKey" 
                  class="form-input" 
                  v-model="apiConfig.apiKey"
                  placeholder="输入API密钥"
                >
              </div>
              
              <div class="form-group">
                <label class="form-label" for="refreshInterval">刷新间隔 (秒)</label>
                <input 
                  type="number" 
                  id="refreshInterval" 
                  class="form-input" 
                  v-model="apiConfig.refreshInterval"
                  min="1"
                  max="60"
                  placeholder="输入数据刷新间隔"
                >
              </div>
              
              <div class="divider"></div>
              
              <!-- 数据同步设置 -->
              <h3 class="section-subtitle">数据同步设置</h3>
              
              <!-- 被动同步 -->
              <div class="sync-option">
                <h4 class="option-title">被动同步</h4>
                <p class="option-desc">本地API将接收外部系统的POST请求进行数据同步</p>
                <div class="sync-info">
                  <p class="sync-endpoint">
                    <strong>同步端点：</strong> 
                    <code>{{ localSyncEndpoint }}</code>
                  </p>
                  <button @click="copyEndpoint" class="btn btn-secondary btn-small">
                    <i class="icon-copy"></i> 复制端点
                  </button>
                </div>
              </div>
              
              <div class="divider"></div>
              
              <!-- 主动同步 -->
              <div class="sync-option">
                <h4 class="option-title">主动同步</h4>
                <p class="option-desc">定时从外部API获取最新数据</p>
                <div class="form-group">
                  <label class="form-label" for="syncInterval">同步间隔 (分钟)</label>
                  <input 
                    type="number" 
                    id="syncInterval" 
                    class="form-input"
                    v-model="syncConfig.syncInterval"
                    min="1"
                    max="60"
                  >
                </div>
              </div>
              
              <div class="form-actions">
                <button @click="saveApiConfig" class="btn btn-primary">
                  <i class="icon-save"></i> 保存配置
                </button>
                <button @click="testApiConnection" class="btn btn-secondary">
                  <i class="icon-check"></i> 测试连接
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- UI配置 -->
        <div v-if="activeCategory === 'ui'" class="category-content">
          <!-- UI设置卡片 -->
          <div class="card">
            <div class="card-header">
              <h2 class="section-title">
                <i class="icon-desktop"></i> 界面配置
              </h2>
            </div>
            
            <div class="card-body">
              <div class="form-group">
                <div class="toggle-group">
                  <label class="toggle-option">
                    <input type="checkbox" v-model="uiConfig.showPlayerCards">
                    <span class="toggle-label">显示选手信息卡</span>
                  </label>
                  
                  <label class="toggle-option">
                    <input type="checkbox" v-model="uiConfig.showRoundInfo">
                    <span class="toggle-label">显示回合信息</span>
                  </label>
                  
                  <label class="toggle-option">
                    <input type="checkbox" v-model="uiConfig.showTeamScores">
                    <span class="toggle-label">显示队伍分数</span>
                  </label>
                  
                  <label class="toggle-option">
                    <input type="checkbox" v-model="uiConfig.showTime">
                    <span class="toggle-label">显示时间</span>
                  </label>
                </div>
              </div>
              
              <div class="form-actions">
                <button @click="saveUiConfig" class="btn btn-primary">
                  <i class="icon-save"></i> 保存配置
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 样式配置 -->
        <div v-if="activeCategory === 'style'" class="category-content">
          <!-- 样式设置卡片 -->
          <div class="card">
            <div class="card-header">
              <h2 class="section-title">
                <i class="icon-paint-brush"></i> 样式配置
              </h2>
            </div>
            
            <div class="card-body">
              <div class="form-group">
                <label class="form-label" for="fontFamily">字体</label>
                <div class="font-selector">
                  <div class="font-search-container">
                    <input 
                      type="text" 
                      id="fontFamily" 
                      class="form-input font-search-input"
                      v-model="fontSearchQuery"
                      @focus="showFontDropdown = true"
                      @input="showFontDropdown = true"
                      placeholder="搜索或选择字体..."
                    >
                    <div class="font-dropdown" v-if="showFontDropdown">
                      <div 
                        v-for="font in filteredFonts" 
                        :key="font.value"
                        class="font-option"
                        :class="{ 'active': styleConfig.fontFamily === font.value }"
                        @click="selectFont(font.value)"
                      >
                        <span :style="{ fontFamily: font.value }">{{ font.name }}</span>
                        <small>{{ font.preview }}</small>
                      </div>
                      <div v-if="filteredFonts.length === 0" class="font-no-result">
                        未找到匹配的字体
                      </div>
                    </div>
                  </div>
                  <div class="font-preview" :style="{ fontFamily: styleConfig.fontFamily }">
                    预览文本：The quick brown fox jumps over the lazy dog. 1234567890
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <label class="form-label" for="customCss">自定义CSS</label>
                <textarea 
                  id="customCss" 
                  class="form-input textarea"
                  v-model="styleConfig.customCss"
                  rows="6"
                  placeholder="输入自定义CSS样式"
                ></textarea>
              </div>
              
              <div class="form-actions">
                <button @click="saveStyleConfig" class="btn btn-primary">
                  <i class="icon-save"></i> 保存配置
                </button>
              </div>
            </div>
          </div>
        </div>
        


      </div>
    </main>
    
    <!-- 页脚 -->
    <footer class="page-footer">
      <p>&copy; 2024 FPSMOB - FPS游戏数据展示工具</p>
    </footer>
    
    <!-- 通知组件 -->
    <div 
      v-if="notification.show" 
      class="notification"
      :class="[notification.type, { show: notification.show }]"
    >
      <i :class="notification.icon"></i>
      <span>{{ notification.message }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'


// 导航分类
const categories = ref([
  { id: 'api', name: 'API配置', icon: 'icon-cog' },
  { id: 'ui', name: '界面配置', icon: 'icon-desktop' },
  { id: 'style', name: '样式配置', icon: 'icon-paint-brush' },

])

// 当前激活的分类
const activeCategory = ref('api')

// 切换分类
function switchCategory(categoryId) {
  activeCategory.value = categoryId
}

// API配置
const apiConfig = ref({
  apiUrl: 'http://localhost:8000',
  apiKey: '',
  refreshInterval: 5
})

// UI配置
const uiConfig = ref({
  showPlayerCards: true,
  showRoundInfo: true,
  showTeamScores: true,
  showTime: true
})

// 样式配置
const styleConfig = ref({
  fontFamily: 'Arial, sans-serif',
  customCss: `/* 默认样式配置 */
.round-info-card {
  backdrop-filter: blur(5px);
  z-index: 1000;
}

.round-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  gap: 20px;
}

.player-card {
  backdrop-filter: blur(5px);
  transition: all 0.3s ease;
  min-width: 180px;
}

.player-card.player-dead {
  opacity: 0.5;
  border-color: #666;
}

.player-cards-container {
  position: absolute;
  bottom: 20px;
  left: 20px;
  display: flex;
  flex-wrap: wrap;
  z-index: 999;
}`
})

// 同步配置
const syncConfig = ref({
  syncInterval: 5
})

// 元素管理配置
const elementsConfig = ref({
  customElements: [],
  enableCustomElements: true
})

// 字体选择相关变量
const fontSearchQuery = ref('')
const showFontDropdown = ref(false)

// 系统字体列表
const systemFonts = ref([
  { name: 'Arial', value: 'Arial, sans-serif', preview: '现代无衬线字体' },
  { name: 'Helvetica', value: 'Helvetica, Arial, sans-serif', preview: '经典无衬线字体' },
  { name: 'Times New Roman', value: '"Times New Roman", Times, serif', preview: '经典衬线字体' },
  { name: 'Georgia', value: 'Georgia, serif', preview: '优雅衬线字体' },
  { name: 'Courier New', value: '"Courier New", Courier, monospace', preview: '等宽字体' },
  { name: 'Verdana', value: 'Verdana, sans-serif', preview: '屏幕优化字体' },
  { name: 'Tahoma', value: 'Tahoma, sans-serif', preview: '紧凑无衬线字体' },
  { name: 'Trebuchet MS', value: '"Trebuchet MS", sans-serif', preview: '人文无衬线字体' },
  { name: 'Impact', value: 'Impact, sans-serif', preview: '粗体显示字体' },
  { name: 'Comic Sans MS', value: '"Comic Sans MS", cursive', preview: '手写风格字体' },
  { name: '微软雅黑', value: '"Microsoft YaHei", "微软雅黑", sans-serif', preview: 'Windows系统默认中文字体' },
  { name: '宋体', value: 'SimSun, "宋体", serif', preview: '传统中文衬线字体' },
  { name: '黑体', value: 'SimHei, "黑体", sans-serif', preview: '中文无衬线字体' },
  { name: '楷体', value: 'KaiTi, "楷体", serif', preview: '中文楷体字体' },
  { name: '仿宋', value: 'FangSong, "仿宋", serif', preview: '中文仿宋字体' },
  { name: '幼圆', value: 'YouYuan, "幼圆", sans-serif', preview: '中文圆体字体' },
  { name: '华文细黑', value: 'STXihei, "华文细黑", sans-serif', preview: '华文细黑字体' },
  { name: '华文楷体', value: 'STKaiti, "华文楷体", serif', preview: '华文楷体字体' },
  { name: '华文宋体', value: 'STSong, "华文宋体", serif', preview: '华文宋体字体' },
  { name: '华文仿宋', value: 'STFangsong, "华文仿宋", serif', preview: '华文仿宋字体' },
  { name: '苹方', value: '"PingFang SC", "Helvetica Neue", Helvetica, Arial, sans-serif', preview: '苹果系统默认中文字体' },
  { name: '冬青黑体', value: '"Hiragino Sans GB", "冬青黑体", sans-serif', preview: '苹果系统黑体字体' },
  { name: '思源黑体', value: '"Source Han Sans CN", "思源黑体", sans-serif', preview: 'Adobe开源黑体字体' },
  { name: '思源宋体', value: '"Source Han Serif CN", "思源宋体", serif', preview: 'Adobe开源宋体字体' }
])

// 过滤后的字体列表
const filteredFonts = computed(() => {
  if (!fontSearchQuery.value) return systemFonts.value
  const query = fontSearchQuery.value.toLowerCase()
  return systemFonts.value.filter(font => 
    font.name.toLowerCase().includes(query) || 
    font.preview.toLowerCase().includes(query)
  )
})

// 选择字体的方法
function selectFont(fontValue) {
  styleConfig.value.fontFamily = fontValue
  showFontDropdown.value = false
  fontSearchQuery.value = ''
}

// 点击外部关闭下拉菜单
function closeFontDropdown() {
  showFontDropdown.value = false
}

// 本地同步端点
const localSyncEndpoint = computed(() => {
  const port = window.location.port || (window.location.protocol === 'https:' ? '443' : '80')
  return `${window.location.protocol}//${window.location.hostname}:${port}/api/data`
})

// 通知状态
const notification = ref({
  show: false,
  message: '',
  type: 'success',
  icon: 'icon-check'
})

// 显示通知
function showNotification(message, type = 'success', icon = 'icon-check') {
  notification.value = {
    show: true,
    message,
    type,
    icon
  }
  
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

// 从后端获取配置
async function loadConfigs() {
  try {
    const response = await axios.get('/api/config')
    const configs = response.data
    if (configs.apiConfig) apiConfig.value = configs.apiConfig
    if (configs.uiConfig) uiConfig.value = configs.uiConfig
    if (configs.styleConfig) styleConfig.value = configs.styleConfig
    if (configs.syncConfig) syncConfig.value = configs.syncConfig
  } catch (error) {
    console.error('加载配置失败:', error)
    showNotification('加载配置失败，使用默认配置', 'error', 'icon-times')
  }
}

// 保存配置到后端
async function saveConfigToBackend() {
  const configs = {
    apiConfig: apiConfig.value,
    uiConfig: uiConfig.value,
    styleConfig: styleConfig.value,
    syncConfig: syncConfig.value
  };
  
  try {
    await axios.post('/api/config', configs)
    showNotification('配置保存成功', 'success', 'icon-check')
  } catch (error) {
    console.error('保存配置失败:', error)
    showNotification('保存配置失败', 'error', 'icon-times')
  }
}

// 保存API配置
function saveApiConfig() {
  saveConfigToBackend()
}

// 保存UI配置
function saveUiConfig() {
  saveConfigToBackend()
}

// 保存样式配置
function saveStyleConfig() {
  saveConfigToBackend()
}



// 测试API连接
function testApiConnection() {
  if (!apiConfig.value.apiUrl) {
    showNotification('请输入API地址', 'error', 'icon-times')
    return
  }
  
  axios.post('/api/config/test-connection', {
    apiUrl: apiConfig.value.apiUrl,
    apiKey: apiConfig.value.apiKey
  })
    .then(response => {
      showNotification('API连接成功', 'success', 'icon-check')
    })
    .catch(error => {
      showNotification(`API连接失败: ${error.response?.data?.message || error.message}`, 'error', 'icon-times')
    })
}

// 复制同步端点
function copyEndpoint() {
  navigator.clipboard.writeText(localSyncEndpoint.value)
    .then(() => {
      showNotification('端点已复制到剪贴板', 'success', 'icon-check')
    })
    .catch(() => {
      showNotification('复制失败，请手动复制', 'error', 'icon-times')
    })
}



// 初始化加载配置
loadConfigs()

// 添加全局点击事件监听，用于关闭字体下拉菜单
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.font-selector')) {
      closeFontDropdown()
    }
  })
})

// 组件卸载时移除事件监听
onUnmounted(() => {
  document.removeEventListener('click', closeFontDropdown)
})
</script>

<style scoped>
/* CSS变量定义 */
:root {
  --primary: #FF4500;
  --primary-dark: #CC3700;
  --secondary: #2E8B57;
  --secondary-dark: #256E45;
  --success: #27AE60;
  --success-dark: #219A52;
  --error: #E74C3C;
  --warning: #F39C12;
  --info: #3498DB;
  --gray: #95A5A6;
  --dark-gray: #34495E;
  --light-gray: #ECF0F1;
  --white: #FFFFFF;
  --black: #000000;
  --border-radius: 8px;
  --transition: all 0.3s ease;
}

/* 容器样式 */
.config-container {
  width: 100%;
  min-height: 100vh;
  background-color: #242424;
  color: rgba(255, 255, 255, 0.87);
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  padding: 10px;
  box-sizing: border-box;
  overflow-x: hidden; /* 防止水平滚动 */
}

/* 页面头部样式 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--border-radius);
}

.header-content h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: var(--white);
}

.header-content h1 .subtitle {
  font-size: 1.2rem;
  font-weight: normal;
  color: var(--gray);
}

.header-desc {
  color: var(--gray);
  font-size: 1rem;
  margin-bottom: 15px;
}

.live-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--primary);
  color: var(--white);
  text-decoration: none;
  border-radius: var(--border-radius);
  font-weight: 500;
  transition: all 0.3s ease;
  margin-top: 10px;
}

.live-link-btn:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 69, 0, 0.3);
}

.live-link-btn:active {
  transform: translateY(0);
}

/* 主内容区样式 */
.main-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 10px;
  box-sizing: border-box;
}



/* 分类导航样式 */
.category-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  overflow-x: auto;
  padding-bottom: 10px;
}

/* 标签样式 */
.tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius);
  color: var(--gray);
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
  justify-content: center;
}

.tab:hover {
  background: rgba(0, 0, 0, 0.4);
  color: var(--white);
  border-color: rgba(255, 255, 255, 0.2);
}

.tab.active {
  background: var(--primary);
  color: var(--white);
  border-color: var(--primary);
}

/* 配置内容区样式 */
.config-content {
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--border-radius);
  padding: 20px;
  max-height: 600px;
  overflow-y: auto;
}

/* 分类内容样式 */
.category-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 卡片样式 */
.card {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius);
  margin-bottom: 20px;
  overflow: hidden;
}

.card-header {
  background: rgba(0, 0, 0, 0.5);
  padding: 15px 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.section-title {
  color: var(--white);
  font-size: 1.3rem;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-body {
  padding: 20px;
}

/* 表单组样式 */
.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  color: var(--white);
  margin-bottom: 8px;
  font-weight: 500;
}

.form-input {
  width: 100%;
  padding: 12px 15px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius);
  color: var(--white);
  font-size: 1rem;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(255, 69, 0, 0.2);
}

.form-input::placeholder {
  color: var(--gray);
}

.form-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.form-group-half {
  flex: 1;
  min-width: 200px;
}

/* 按钮样式 */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: var(--border-radius);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  font-family: inherit;
}

.btn-primary {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary-dark) 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 69, 0, 0.3);
}

.btn-secondary {
  background: linear-gradient(135deg, var(--dark-gray) 0%, #2c3e50 100%);
  color: white;
}

.btn-secondary:hover {
  background: linear-gradient(135deg, #2c3e50 0%, #2c3e50 100%);
  transform: translateY(-2px);
}

.btn-small {
  padding: 6px 12px;
  font-size: 0.875rem;
}

.btn-success {
  background: linear-gradient(135deg, var(--success) 0%, var(--success-dark) 100%);
  color: white;
}

.btn-success:hover {
  background: linear-gradient(135deg, var(--success-dark) 0%, var(--success-dark) 100%);
}

/* UI切换选项样式 */
.ui-toggle-options {
  padding: 15px 0;
}

.toggle-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.toggle-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
}

.toggle-option:hover {
  background: rgba(255, 255, 255, 0.1);
}

.toggle-option input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: var(--primary);
}

.toggle-label {
  cursor: pointer;
  font-weight: 400;
}

/* 同步设置样式 */
.sync-option {
  margin-bottom: 20px;
}

.option-title {
  font-size: 1.2rem;
  margin-bottom: 8px;
  color: var(--white);
}

.option-desc {
  color: var(--gray);
  margin-bottom: 15px;
  font-size: 0.9rem;
}

.sync-info {
  background: rgba(255, 255, 255, 0.05);
  padding: 15px;
  border-radius: var(--border-radius);
  border-left: 4px solid var(--primary);
}

.sync-endpoint {
  margin: 0 0 10px 0;
  word-break: break-all;
}

.sync-endpoint code {
  background: rgba(0, 0, 0, 0.3);
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

.divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 20px 0;
}

/* 页脚样式 */
.page-footer {
  text-align: center;
  margin-top: 50px;
  padding: 20px 0;
  color: var(--gray);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--border-radius);
}

/* 字体选择器样式 */
.font-selector {
  position: relative;
}

.font-search-container {
  position: relative;
}

.font-search-input {
  cursor: pointer;
}

.font-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 300px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius);
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.font-option {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.font-option:last-child {
  border-bottom: none;
}

.font-option:hover {
  background: rgba(255, 255, 255, 0.1);
}

.font-option.active {
  background: rgba(255, 69, 0, 0.2);
  border-left: 3px solid var(--primary);
}

.font-option span {
  font-weight: 500;
}

.font-option small {
  color: var(--gray);
  font-size: 0.8rem;
}

.font-no-result {
  padding: 15px;
  text-align: center;
  color: var(--gray);
  font-style: italic;
}

.font-preview {
  margin-top: 10px;
  padding: 15px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--border-radius);
  font-size: 1rem;
  line-height: 1.5;
  color: var(--white);
}

/* 字体下拉菜单滚动条样式 */
.font-dropdown::-webkit-scrollbar {
  width: 8px;
}

.font-dropdown::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.font-dropdown::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.font-dropdown::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .config-container {
    padding: 15px;
  }
  
  .form-row {
    flex-direction: column;
    gap: 15px;
  }
  
  .form-group-half {
    min-width: 100%;
    width: 100%;
  }
  
  .config-content {
    max-height: 400px; /* 移动端配置区域高度调整 */
  }
  
  .category-tabs {
    flex-direction: column;
  }
  
  .tab {
    min-width: 100%;
  }
  
  .toggle-group {
    grid-template-columns: 1fr;
  }
  
  .header-content h1 {
    font-size: 2rem;
  }
}

/* 通知样式 */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: var(--border-radius);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  transform: translateX(150%);
  transition: transform 0.3s ease;
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 250px;
  backdrop-filter: blur(10px);
}

.notification.show {
  transform: translateX(0);
}

.notification.success {
  background: rgba(39, 174, 96, 0.8);
  color: var(--white);
}

.notification.error {
  background: rgba(231, 76, 60, 0.8);
  color: var(--white);
}

.notification.warning {
  background: rgba(243, 156, 18, 0.8);
  color: var(--white);
}

.notification.info {
  background: rgba(52, 152, 219, 0.8);
  color: var(--white);
}
</style>
<template>
  <div class="config-container">
    <!-- 页面头部 -->
    <header class="page-header">
      <div class="header-content">
        <h1>FPSMOB <span class="subtitle">配置中心</span></h1>
        <p class="header-desc">可定制FPS游戏直播数据展示界面</p>
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
                <select 
                  id="syncMode" 
                  class="form-input" 
                  v-model="syncConfig.syncMode"
                >
                  <option value="passive">被动同步</option>
                  <option value="active">主动同步</option>
                  <option value="local">本地文件</option>
                </select>
              </div>
              
              <!-- 被动同步配置 -->
              <div v-if="syncConfig.syncMode === 'passive'" class="sync-option">
                <h4 class="option-title">被动同步配置</h4>
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
              
              <!-- 主动同步配置 -->
              <div v-if="syncConfig.syncMode === 'active'" class="sync-option">
                <h4 class="option-title">主动同步配置</h4>
                <p class="option-desc">定时从外部API获取最新数据</p>
                
                <div class="form-group">
                  <label class="form-label" for="activeApiUrl">API地址</label>
                  <input 
                    type="text" 
                    id="activeApiUrl" 
                    class="form-input" 
                    v-model="syncConfig.apiUrl"
                    placeholder="输入API地址，如 http://localhost:8080"
                  >
                </div>
                
                <div class="form-group">
                  <label class="form-label" for="activeApiKey">API密钥</label>
                  <input 
                    type="password" 
                    id="activeApiKey" 
                    class="form-input" 
                    v-model="syncConfig.apiKey"
                    placeholder="输入API密钥"
                  >
                </div>
                
                <div class="form-group">
                  <label class="form-label" for="activeSyncInterval">同步间隔 (毫秒)</label>
                  <input 
                    type="number" 
                    id="activeSyncInterval" 
                    class="form-input"
                    v-model="syncConfig.syncInterval"
                    min="100"
                    max="60000"
                    step="100"
                  >
                  <p class="field-hint">100-60000毫秒 (0.1-60秒)</p>
                </div>

                <div class="form-group">
                  <label class="form-label" for="httpMethod">HTTP请求方法</label>
                  <select 
                    id="httpMethod" 
                    class="form-input" 
                    v-model="syncConfig.httpMethod"
                  >
                    <option value="GET">GET</option>
                    <option value="POST">POST</option>
                  </select>
                </div>

                <!-- 仅在 GET/POST 时显示参数配置 -->
                <div class="form-group" v-if="syncConfig.httpMethod === 'GET'">
                  <label class="form-label" for="requestParams">GET 查询参数 (查询字符串或JSON)</label>
                  <textarea 
                    id="requestParams" 
                    class="form-input" 
                    v-model="requestParamsText"
                    placeholder='示例: key=value&page=1 或 {"key": "value", "page": 1}'
                    rows="4"
                  ></textarea>
                  <p class="field-hint">支持 a=1&b=2 或 JSON，均会转换为查询参数</p>
                </div>
                <div class="form-group" v-if="syncConfig.httpMethod === 'POST'">
                  <label class="form-label" for="requestParams">POST 请求体 (JSON格式)</label>
                  <textarea 
                    id="requestParams" 
                    class="form-input" 
                    v-model="requestParamsText"
                    placeholder='示例: {"key": "value"}'
                    rows="4"
                  ></textarea>
                  <p class="field-hint">作为 JSON 请求体发送</p>
                </div>
              </div>
              
              <!-- 本地文件配置 -->
              <div v-if="syncConfig.syncMode === 'local'" class="sync-option">
                <h4 class="option-title">本地文件配置</h4>
                <p class="option-desc">直接从本地JSON文件获取数据</p>
                
                <div class="form-group">
                  <label class="form-label" for="localFilePath">文件路径</label>
                  <input 
                    type="text" 
                    id="localFilePath" 
                    class="form-input" 
                    v-model="syncConfig.localFilePath"
                    placeholder="输入本地JSON文件路径，如 data/match.json"
                  >
                </div>
                

              </div>
              
              <div class="divider"></div>
              
              <div class="form-actions">
                <button @click="saveSyncConfig" class="btn btn-primary">
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
                  
                  <label class="toggle-option">
                    <input type="checkbox" v-model="uiConfig.showAdCard">
                    <span class="toggle-label">显示广告卡</span>
                  </label>
                </div>
              </div>
              
              <!-- 团队配置 -->
              <div class="form-group">
                <h4>CT阵营配置</h4>
                <div class="form-row">
                  <div class="form-group-half">
                    <label class="form-label">队伍名称</label>
                    <input 
                      type="text" 
                      class="form-input"
                      v-model="uiConfig.teamConfig.ctTeam.name" 
                      placeholder="输入CT队伍名称"
                    >
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">图标文件</label>
                    <input 
                      type="text" 
                      class="form-input"
                      v-model="uiConfig.teamConfig.ctTeam.icon" 
                      placeholder="输入图标文件名"
                    >
                    <p class="field-hint">图标文件应放置在 <code>src/assets/</code> 目录下</p>
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">主题颜色</label>
                    <input 
                      type="color" 
                      class="form-input"
                      v-model="uiConfig.teamConfig.ctTeam.color"
                    >
                  </div>
                </div>
              </div>
              
              <div class="form-group">
                <h4>T阵营配置</h4>
                <div class="form-row">
                  <div class="form-group-half">
                    <label class="form-label">队伍名称</label>
                    <input 
                      type="text" 
                      class="form-input"
                      v-model="uiConfig.teamConfig.tTeam.name" 
                      placeholder="输入T队伍名称"
                    >
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">图标文件</label>
                    <input 
                      type="text" 
                      class="form-input"
                      v-model="uiConfig.teamConfig.tTeam.icon" 
                      placeholder="输入图标文件名"
                    >
                    <p class="field-hint">图标文件应放置在 <code>src/assets/</code> 目录下</p>
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">主题颜色</label>
                    <input 
                      type="color" 
                      class="form-input"
                      v-model="uiConfig.teamConfig.tTeam.color"
                    >
                  </div>
                </div>
              </div>
              
              <!-- 广告卡配置 -->
              <div class="form-group" v-if="uiConfig.showAdCard">
                <h4>广告卡配置</h4>
                <div class="form-row">
                  <div class="form-group-half">
                    <label class="form-label">启用广告</label>
                    <label class="toggle-option">
                      <input type="checkbox" v-model="uiConfig.adCardConfig.enabled">
                      <span class="toggle-label">开启/关闭</span>
                    </label>
                  </div>
                  <div class="form-group-full">
                    <label class="form-label">广告文字</label>
                    <input 
                      type="text" 
                      class="form-input"
                      v-model="uiConfig.adCardConfig.text" 
                      placeholder="输入广告文字内容"
                    >
                  </div>
                  <div class="form-group-full">
                    <label class="form-label">图片URL</label>
                    <input 
                      type="text" 
                      class="form-input"
                      v-model="uiConfig.adCardConfig.imageUrl" 
                      placeholder="输入图片URL或上传图片"
                    >
                    <p class="field-hint">支持本地文件路径或网络URL</p>
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">显示位置</label>
                    <select class="form-input" v-model="uiConfig.adCardConfig.position">
                      <option value="top-left">左上角</option>
                      <option value="top-right">右上角</option>
                      <option value="bottom-left">左下角</option>
                      <option value="bottom-right">右下角</option>
                    </select>
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">显示时长 (秒)</label>
                    <input 
                      type="number" 
                      class="form-input"
                      v-model="uiConfig.adCardConfig.duration" 
                      min="5"
                      max="300"
                    >
                  </div>
                  <div class="form-group-half">
                    <label class="form-label">显示间隔 (秒)</label>
                    <input 
                      type="number" 
                      class="form-input"
                      v-model="uiConfig.adCardConfig.interval" 
                      min="30"
                      max="1800"
                    >
                  </div>
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
                      :placeholder="getSelectedFontName() || '搜索或选择字体...'"
                    >
                    <div class="font-dropdown" v-if="showFontDropdown">
                      <div 
                        v-for="font in filteredFonts" 
                        :key="font.value"
                        class="font-option"
                        :class="{ 'active': styleConfig.fontFamily === font.value }"
                        @click="selectFont(font)"
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
                <label class="form-label" for="cssFile">CSS文件</label>
                <select 
                  id="cssFile" 
                  class="form-input"
                  v-model="styleConfig.cssFile"
                >
                  <option value="default.css">默认样式</option>
                  <option value="custom.css">自定义样式</option>
                </select>
                <div v-if="styleConfig.cssFile === 'custom.css'" class="css-file-info">
                  <p class="info-text">请将自定义CSS文件放置在 <code>css/custom.css</code></p>
                </div>
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'


// 导航分类
const categories = ref([
  { id: 'api', name: 'API配置', icon: 'icon-cog' },
  { id: 'ui', name: '界面配置', icon: 'icon-desktop' },
  { id: 'style', name: '样式配置', icon: 'icon-paint-brush' }
])

// 当前激活的分类
const activeCategory = ref('api')

// 切换分类
function switchCategory(categoryId) {
  activeCategory.value = categoryId
}

// UI配置
const uiConfig = ref({
  showPlayerCards: true,
  showRoundInfo: true,
  showTeamScores: true,
  showTime: true,
  showAdCard: false, // 新增：是否显示广告卡
  
  // 团队配置迁移到UI配置中
  teamConfig: {
    ctTeam: {
      name: 'CT',
      icon: 'ct_logo.svg',
      color: '#2196F3'
    },
    tTeam: {
      name: 'T',
      icon: 't_logo.svg',
      color: '#FF9800'
    }
  },
  
  // 广告卡配置
  adCardConfig: {
    enabled: false,
    text: '赞助商广告',
    imageUrl: '',
    position: 'bottom-right', // top-left, top-right, bottom-left, bottom-right
    duration: 30, // 显示时长（秒）
    interval: 300 // 显示间隔（秒）
  }
})

// 样式配置
const styleConfig = ref({
  fontFamily: 'Arial, sans-serif',
  cssFile: 'default.css'
})

// 字体选择器相关变量
const fontSearchQuery = ref('')
const showFontDropdown = ref(false)
const fonts = ref([])

// 过滤后的字体列表
const filteredFonts = computed(() => {
  if (!fontSearchQuery.value) {
    return fonts.value
  }
  return fonts.value.filter(font => 
    font.name.toLowerCase().includes(fontSearchQuery.value.toLowerCase()) ||
    font.preview.toLowerCase().includes(fontSearchQuery.value.toLowerCase())
  )
})

// 本地同步端点
const localSyncEndpoint = computed(() => {
  return `${window.location.origin}/api/sync`
})

// 通知配置
const notification = ref({
  show: false,
  type: 'info',
  message: '',
  icon: ''
})

// 显示通知
function showNotification(message, type = 'info', icon = 'icon-info') {
  notification.value = {
    show: true,
    type,
    message,
    icon
  }
  
  // 3秒后自动隐藏通知
  setTimeout(() => {
    notification.value.show = false
  }, 3000)
}

// 同步配置
const syncConfig = ref({
  syncMode: 'active', // 'passive', 'active', or 'local'
  syncInterval: 5000,
  apiUrl: '',
  apiKey: '',
  localFilePath: '',
  httpMethod: 'GET',
  requestParams: {}
})

// 请求参数文本（用于文本编辑）
const requestParamsText = ref('')

// 监听请求参数变化，同步到syncConfig
watch(requestParamsText, (newValue) => {
  try {
    if (newValue.trim()) {
      if (syncConfig.value.httpMethod === 'GET' && newValue.includes('=')) {
        // 解析查询字符串为对象
        const params = {}
        newValue.split('&').forEach(part => {
          const [k, v] = part.split('=')
          if (k) params[decodeURIComponent(k.trim())] = v ? decodeURIComponent(v.trim()) : ''
        })
        syncConfig.value.requestParams = params
      } else {
        syncConfig.value.requestParams = JSON.parse(newValue)
      }
    } else {
      syncConfig.value.requestParams = {}
    }
  } catch (error) {
    // JSON解析错误时保持原值
    console.warn('JSON解析错误:', error)
  }
})

// 监听syncConfig.requestParams变化，同步到文本
watch(() => syncConfig.value.requestParams, (newValue) => {
  try {
    requestParamsText.value = JSON.stringify(newValue, null, 2)
  } catch (error) {
    requestParamsText.value = '{}'
  }
}, { immediate: true })


function saveUiConfig() {
  const configData = {
    uiConfig: {
      showPlayerCards: uiConfig.value.showPlayerCards,
      showRoundInfo: uiConfig.value.showRoundInfo,
      showTeamScores: uiConfig.value.showTeamScores,
      showTime: uiConfig.value.showTime,
      showAdCard: uiConfig.value.showAdCard,
      teamConfig: uiConfig.value.teamConfig,
      adCardConfig: uiConfig.value.adCardConfig
    }
  }
  
  // 保存配置到后端
  saveConfigToBackend(configData)
}

function saveSyncConfig() {
  const configData = {
    syncConfig: syncConfig.value,
  }
  
  // 保存配置到后端
  saveConfigToBackend(configData)
}

// 保存配置到后端
async function saveConfigToBackend(configs) {
  try {
    await axios.post('/api/config', configs)
    showNotification('配置保存成功', 'success', 'icon-check')
  } catch (error) {
    console.error('保存配置失败:', error)
    showNotification('保存配置失败', 'error', 'icon-times')
  }
}

// 保存样式配置
function saveStyleConfig() {
  saveConfigToBackend()
}


// 测试API连接
function testApiConnection() {
  if (!syncConfig.value.apiUrl) {
    showNotification('请输入API地址', 'error', 'icon-times')
    return
  }
  
  axios.post('/api/config/test-connection', {
    apiUrl: syncConfig.value.apiUrl,
    apiKey: syncConfig.value.apiKey
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

// 从后端获取配置
async function loadConfigs() {
  try {
    const response = await axios.get('/api/config')
    const configs = response.data
    if (configs.uiConfig) {
      uiConfig.value = { ...uiConfig.value, ...configs.uiConfig }
      // 确保团队配置存在
      if (!uiConfig.value.teamConfig) {
        uiConfig.value.teamConfig = {
          ctTeam: { name: 'CT', icon: 'ct_logo.svg', color: '#2196F3' },
          tTeam: { name: 'T', icon: 't_logo.svg', color: '#FF9800' }
        }
      }
      // 确保广告卡配置存在
      if (!uiConfig.value.adCardConfig) {
        uiConfig.value.adCardConfig = {
          enabled: false,
          text: '赞助商广告',
          imageUrl: '',
          position: 'bottom-right',
          duration: 30,
          interval: 300
        }
      }
    }
    if (configs.styleConfig) styleConfig.value = configs.styleConfig
    if (configs.syncConfig) {
      syncConfig.value = { ...syncConfig.value, ...configs.syncConfig }
    }
  } catch (error) {
    console.error('加载配置失败:', error)
    showNotification('加载配置失败，使用默认配置', 'error', 'icon-times')
  }
}

// 加载字体配置
async function loadFonts() {
  try {
    const response = await axios.get('/api/fonts')
    fonts.value = response.data
    console.log('系统字体加载完成，共', fonts.value.length, '种字体')
  } catch (error) {
    console.error('加载系统字体失败:', error)
    showNotification('加载系统字体失败，使用默认字体列表', 'warning', 'icon-warning')
    // 出错时使用默认字体列表作为后备
    fonts.value = [
      { value: 'Arial, sans-serif', name: 'Arial', preview: '系统字体' },
      { value: 'Times New Roman, serif', name: 'Times New Roman', preview: '系统字体' },
      { value: 'Courier New, monospace', name: 'Courier New', preview: '系统字体' },
      { value: 'Georgia, serif', name: 'Georgia', preview: '系统字体' },
      { value: 'Verdana, sans-serif', name: 'Verdana', preview: '系统字体' },
      { value: 'Tahoma, sans-serif', name: 'Tahoma', preview: '系统字体' },
      { value: 'Trebuchet MS, sans-serif', name: 'Trebuchet MS', preview: '系统字体' },
      { value: 'Impact, sans-serif', name: 'Impact', preview: '系统字体' },
      { value: 'Comic Sans MS, cursive', name: 'Comic Sans MS', preview: '系统字体' }
    ]
  }
}

// 关闭字体下拉菜单
function closeFontDropdown() {
  showFontDropdown.value = false
}

// 选择字体
function selectFont(font) {
  styleConfig.value.fontFamily = font.value
  closeFontDropdown()
}

// 获取选中的字体名称
function getSelectedFontName() {
  const selectedFont = fonts.value.find(font => font.value === styleConfig.value.fontFamily)
  return selectedFont ? selectedFont.name : null
}



// 初始化加载配置和字体
loadConfigs()
loadFonts()

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
  border-color: transparent;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.3);
  transform: translateY(-1px);
}

/* 配置内容区样式 */
.config-content {
  background: rgba(0, 0, 0, 0.2);
  border-radius: var(--border-radius);
  padding: 20px;
  max-height: 600px;
  overflow-y: auto;
}

/* 统一滚动条样式 */
.config-content::-webkit-scrollbar {
  width: 8px;
}

.config-content::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.config-content::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 4px;
}

.config-content::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
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
  max-height: 200px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius);
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  margin-top: 5px;
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

/* 下拉选择框样式 */
select.form-input {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2395A5A6' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  cursor: pointer;
  background-color: rgba(0, 0, 0, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: var(--border-radius);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  color: var(--white);
}

select.form-input:focus {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23FF4500' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(255, 69, 0, 0.1);
}

/* 颜色选择器样式 */
input[type="color"].form-input {
  height: 44px;
  padding: 6px;
  cursor: pointer;
}

input[type="color"].form-input::-webkit-color-swatch {
  border: none;
  border-radius: calc(var(--border-radius) - 2px);
}

input[type="color"].form-input::-webkit-color-swatch-wrapper {
  padding: 0;
}

/* 同步选项动画 */
.sync-option {
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 同步模式标签样式 */
.sync-mode-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--white);
}

/* 同步选项标题样式 */
.sync-option .option-title {
  color: var(--primary);
  border-bottom: 2px solid var(--primary);
  padding-bottom: 8px;
  margin-bottom: 15px;
}

/* 同步选项描述样式 */
.sync-option .option-desc {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 20px;
  border-left: 3px solid var(--primary);
}

/* CSS文件信息样式 */
.css-file-info {
  margin-top: 10px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: var(--border-radius);
  border-left: 3px solid var(--info);
}

.info-text {
  margin: 0;
  color: var(--gray);
  font-size: 0.9rem;
}

.info-text code {
  background: rgba(0, 0, 0, 0.3);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
}

</style>
# FPSMOB - FPS游戏直播数据监控面板

FPSMOB是一个用于OBS的悬浮浏览器界面，用于显示FPS游戏（如CS:GO）的实时数据，包括选手信息卡牌、顶部回合信息卡片等。

## 功能特点

### 数据同步方式
- **被动同步**：通过本地API接收外部系统的POST请求进行数据同步
- **主动同步**：定时向设定的API发送请求获取最新数据
- **本地同步**：监视本地JSON文件的变更并自动同步数据

### 界面功能
- 选手信息卡牌显示（K/D/A、金钱、武器等）
- 顶部回合信息卡片（比分、倒计时、状态等）
- 高度自定义的UI配置（显示/隐藏元素、颜色、字体等）
- 实时预览功能
- 自定义CSS支持

## 技术栈

- **前端**：Vue 3、Vite、Vue Router、Axios
- **后端**：Python、Flask、Flask-CORS

## 安装和运行

### 前端安装

1. 安装依赖：
```bash
npm install
```

2. 开发模式运行：
```bash
npm run dev
```

3. 构建生产版本：
```bash
npm run build
```

### 快速启动（推荐）

#### 使用启动脚本（Windows）
```bash
# 双击运行或在命令行中执行
start.bat
```

#### 使用Python启动脚本（跨平台）
```bash
python start.py
```

这两个脚本会自动：
1. 检测并提示安装Node.js环境（如未安装）
2. 检测并自动安装Python依赖（如未安装）
3. 检测并自动安装前端npm依赖（如未安装）
4. 提示构建前端项目（如未构建）
5. 启动后端服务
6. 打开浏览器访问配置页面
7. 显示OBS配置说明

### 依赖检测工具

我们提供了一个依赖检测脚本，可以帮助您检查项目所需的所有依赖是否已正确安装：

```bash
python test_deps.py
```

这个脚本会检查：
- Node.js和npm环境
- Python依赖包
- 前端npm依赖
- 数据文件(api_message.json)的存在性

### 手动安装和运行

#### 后端安装

1. 安装Python依赖：
```bash
pip install -r requirements.txt
```

2. 运行后端服务：
```bash
python app.py
```

## 使用指南

### 启动应用

使用提供的启动脚本可以快速启动整个应用：

- **Windows用户**：双击运行 `start.bat` 文件
- **所有平台**：在命令行中执行 `python start.py`

启动脚本会自动完成所有必要的步骤，并在浏览器中打开配置界面。

### 配置界面
打开应用后默认进入配置界面，可以进行以下设置：

1. **同步设置**：
   - 查看被动同步的API地址
   - 配置主动同步的API地址和同步间隔
   - 本地同步会自动监视api_message.json文件

2. **界面配置**：
   - 切换UI元素的显示/隐藏
   - 自定义颜色、字体
   - 输入自定义CSS代码

3. **实时预览**：
   - 在配置界面中实时预览直播界面效果
   - 点击"打开直播界面"按钮在新窗口打开实际的直播界面

### 在OBS中使用

1. 构建前端项目：
```bash
npm run build
```

2. 运行后端服务：
```bash
python app.py
```

3. 在OBS中添加"浏览器"源，URL设置为：`http://localhost:5000/live`

## 数据格式

后端API接收和返回的数据格式遵循api_message.json的结构，主要包含：
- tabData：选手数据（K/D/A、武器、金钱等）
- 回合信息：比分、时间、状态等

## 项目结构

```
fpsmob/
├── src/                # 前端源码
│   ├── views/          # 页面视图
│   ├── components/     # 组件
│   ├── router/         # 路由配置
│   ├── assets/         # 静态资源
│   ├── main.js         # 入口文件
│   └── App.vue         # 根组件
├── app.py              # 后端API
├── requirements.txt    # Python依赖
├── package.json        # 前端依赖
├── vite.config.js      # Vite配置
├── index.html          # HTML入口
└── api_message.json    # 示例数据文件
```

## 开发说明

- 前端使用Vue 3的组合式API
- 后端使用Flask提供RESTful API
- 数据更新通过定时请求和文件监控实现
- 配置项保存在浏览器的localStorage中

## 注意事项

- 生产环境中请使用Gunicorn或uWSGI等WSGI服务器运行后端
- 确保api_message.json文件有正确的读写权限
- 在OBS中使用时，建议调整浏览器源的大小和位置以获得最佳效果

## License

MIT

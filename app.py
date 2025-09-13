from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import threading
import time
import logging
import requests
import os
import re
import matplotlib.font_manager as fm
import watchdog.observers
import watchdog.events

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# 禁用 Werkzeug 的请求日志
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__, static_folder='dist', static_url_path='/')
CORS(app)

# 应用配置
class AppConfig:
    def __init__(self):
        self.data = {}
        self.config_data = {}
        self.connections = []  # WebSocket连接（模拟）
        self.config_file_path = 'config.json'

config = AppConfig()

# 规范化URL，确保包含协议
def normalize_url(url: str) -> str:
    try:
        if not url:
            return url
        if not re.match(r'^https?://', url, flags=re.IGNORECASE):
            return f'http://{url}'
        return url
    except Exception:
        return url

# 加载初始数据和配置
def load_data():

    try:
        if os.path.exists(config.config_file_path):
            with open(config.config_file_path, 'r', encoding='utf-8') as f:
                config.config_data = json.load(f)
            logger.info(f'Loaded config from {config.config_file_path}')
    except Exception as e:
        logger.error(f'Error loading data: {e}')

# 保存配置
def save_config(data):
    try:
        with open(config.config_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        config.config_data = data
        logger.info(f'Saved config to {config.config_file_path}')
        return True
    except Exception as e:
        logger.error(f'Error saving config: {e}')
        return False

# 从命令行参数获取端口
import sys
DEFAULT_PORT = 5000
port = DEFAULT_PORT
if len(sys.argv) > 1:
    try:
        port = int(sys.argv[1])
    except ValueError:
        logger.warning(f'Invalid port number {sys.argv[1]}, using default port {DEFAULT_PORT}')

# 文件变化处理器
class FileChangeHandler(watchdog.events.FileSystemEventHandler):
    def __init__(self, sync_thread):
        super().__init__()
        self.sync_thread = sync_thread
    
    def on_modified(self, event):
        if not event.is_directory:
            # 获取当前要监视的文件路径（处理空路径情况）
            watch_file = self.sync_thread.local_file_path or 'api_message.json'
            # 规范化路径进行比较
            if os.path.normpath(event.src_path) == os.path.normpath(watch_file):
                logger.info(f'Local file modified: {event.src_path}')
                self.sync_thread.sync_from_local_file()
    
    def on_created(self, event):
        if not event.is_directory:
            # 获取当前要监视的文件路径（处理空路径情况）
            watch_file = self.sync_thread.local_file_path or 'api_message.json'
            # 规范化路径进行比较
            if os.path.normpath(event.src_path) == os.path.normpath(watch_file):
                logger.info(f'Local file created: {event.src_path}')
                self.sync_thread.sync_from_local_file()

# 定时同步数据的线程
class DataSyncThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.sync_interval = 5000  # 默认5000毫秒(5秒)同步一次
        self.api_url = None
        self.api_key = None
        self.http_method = 'GET'  # 默认GET请求
        self.request_params = {}  # 请求参数
        self.local_file_path = None
        self.sync_mode = 'active'
        self.file_observer = None
        self.file_handler = None
        
    def run(self):
        while self.running:
            # 从配置中获取最新的同步设置
            config_data = config.config_data
            if config_data and 'syncConfig' in config_data:
                sync_config = config_data['syncConfig']
                self.sync_mode = sync_config.get('syncMode', 'active')
                self.sync_interval = sync_config.get('syncInterval', 5000)  # 默认5000毫秒
                self.api_url = sync_config.get('apiUrl')
                self.api_key = sync_config.get('apiKey')
                self.http_method = sync_config.get('httpMethod', 'GET')
                self.request_params = sync_config.get('requestParams', {})
                
                # 更新本地文件路径并设置文件监视（仅在local模式）
                new_local_file_path = sync_config.get('localFilePath')
                if self.sync_mode == 'local' and new_local_file_path != self.local_file_path:
                    self.local_file_path = new_local_file_path
                    self.setup_file_watcher()
                    # 路径更新时立即同步一次
                    self.sync_from_local_file()
                # 非local模式时，确保文件监视关闭
                if self.sync_mode != 'local' and self.file_observer:
                    try:
                        self.file_observer.stop()
                        self.file_observer.join()
                    except Exception:
                        pass
                    self.file_observer = None
                    self.file_handler = None
            
            # 根据同步模式执行不同的同步逻辑
            if self.sync_mode == 'active' and self.api_url:
                self.sync_from_api()
            elif self.sync_mode == 'local':
                # 本地模式无需主动拉取，文件变更会触发同步
                pass
            elif self.sync_mode == 'passive':
                # 被动模式不应进行任何轮询
                pass
            
            time.sleep(self.sync_interval / 1000)
    
    def setup_file_watcher(self):
        # 停止现有的文件监视器
        if self.file_observer:
            try:
                self.file_observer.stop()
                self.file_observer.join()
            except Exception:
                pass
        
        # 确定要监视的文件路径
        file_path = self.local_file_path
        if not file_path:
            file_path = 'api_message.json'
        
        # 启动新的文件监视器
        try:
            # 获取文件所在目录
            watch_dir = os.path.dirname(file_path) or '.'
            
            # 检查目录是否存在
            if not os.path.exists(watch_dir):
                # 如果目录不存在，尝试创建
                os.makedirs(watch_dir, exist_ok=True)
                logger.info(f'Created directory: {watch_dir}')
            
            self.file_handler = FileChangeHandler(self)
            self.file_observer = watchdog.observers.Observer()
            self.file_observer.schedule(self.file_handler, watch_dir, recursive=False)
            self.file_observer.start()
            logger.info(f'Started file watcher for: {file_path}')
        except Exception as e:
            logger.error(f'Failed to start file watcher: {e}')
    
    def sync_from_api(self):
        """从API同步数据"""
        try:
            url = normalize_url(self.api_url)
            logger.info(f'Trying to sync data from API: {url} with method {self.http_method}')
            headers = {}
            if self.api_key:
                headers['Authorization'] = f'Bearer {self.api_key}'
            
            # 根据HTTP方法发送请求
            if self.http_method.upper() == 'GET':
                response = requests.get(url, params=self.request_params, headers=headers, timeout=10)
            elif self.http_method.upper() == 'POST':
                response = requests.post(url, json=self.request_params, headers=headers, timeout=10)
            # 仅支持 GET/POST
            else:
                logger.error(f'Unsupported HTTP method: {self.http_method}')
                return
            
            if response.status_code == 200:
                config.data = response.json()
                logger.info('Data synced successfully from API')
            else:
                logger.error(f'API request failed with status code: {response.status_code}')
        except Exception as e:
            logger.error(f'Error syncing data from API: {e}')
    
    def sync_from_local_file(self):
        """从本地文件同步数据"""
        try:
            # 如果本地文件路径为空，默认使用 api_message.json
            file_path = self.local_file_path
            if not file_path:
                file_path = 'api_message.json'
            
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                config.data = file_data
                logger.info(f'Data synced successfully from local file: {file_path}')
            else:
                logger.warning(f'Local file not found: {file_path}')
        except Exception as e:
            logger.error(f'Error syncing data from local file: {e}')
    
    def stop(self):
        self.running = False
        # 停止文件监视
        if self.file_observer:
            try:
                self.file_observer.stop()
                self.file_observer.join()
            except Exception:
                pass
            self.file_observer = None
            self.file_handler = None

# 全局同步线程（按需启动）
sync_thread = None

def control_sync_thread():
    """根据配置中的 syncMode 控制同步线程的启停"""
    global sync_thread
    mode = 'active'
    if config.config_data and 'syncConfig' in config.config_data:
        mode = config.config_data['syncConfig'].get('syncMode', 'active')
    
    if mode in ['active', 'local']:
        # 确保线程在运行
        if sync_thread is None or not sync_thread.is_alive():
            sync_thread = DataSyncThread()
            sync_thread.start()
            logger.info(f'Started sync thread for mode: {mode}')
    else:
        # 被动模式，停止线程
        if sync_thread is not None and sync_thread.is_alive():
            logger.info('Stopping sync thread (passive mode)')
            sync_thread.stop()
            # 等待最多1秒结束
            sync_thread.join(timeout=1.0)
            if sync_thread.is_alive():
                logger.warning('Sync thread did not stop within timeout')
            sync_thread = None

# API路由 - 获取当前游戏数据
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(config.data)

# API路由 - 保存配置
@app.route('/api/config', methods=['POST'])
def save_config_api():
    try:
        data = request.json
        
        # 合并配置而不是覆盖
        current_config = config.config_data or {}
        merged_config = {**current_config, **data}
        
        if save_config(merged_config):
            # 保存后根据新配置控制线程
            control_sync_thread()
            return jsonify({'status': 'success', 'message': 'Config saved successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save config'}), 500
    except Exception as e:
        logger.error(f'Error saving config: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 400

# API路由 - 获取配置
@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify(config.config_data)

# API路由 - 被动同步数据接收端点
@app.route('/api/data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        # 检查当前是否处于被动同步模式
        config_data = config.config_data
        sync_mode = 'active'
        if config_data and 'syncConfig' in config_data:
            sync_mode = config_data['syncConfig'].get('syncMode', 'active')
        
        if sync_mode != 'passive':
            return jsonify({'status': 'error', 'message': 'Server is not in passive sync mode'}), 400
        
        # 更新数据
        config.data = data
        logger.info('Data received successfully via passive sync')
        return jsonify({'status': 'success', 'message': 'Data received successfully'})
    except Exception as e:
        logger.error(f'Error receiving data: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 400

# API路由 - 测试API连接
@app.route('/api/config/test-connection', methods=['POST'])
def test_connection():
    try:
        data = request.json
        api_url = normalize_url(data.get('apiUrl'))
        api_key = data.get('apiKey')
        
        if not api_url:
            return jsonify({'status': 'error', 'message': 'API URL is required'}), 400
        
        headers = {}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        response = requests.get(api_url, headers=headers, timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'success', 'message': 'API connection successful'})
        else:
            return jsonify({'status': 'error', 'message': f'API request failed with status code: {response.status_code}'}), 400
    except Exception as e:
        logger.error(f'Error testing connection: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 400

# API路由 - 获取系统字体列表
@app.route('/api/fonts', methods=['GET'])
def get_fonts():
    try:
        # 使用matplotlib获取系统字体列表
        font_names = []
        font_paths = fm.findSystemFonts()
        
        # 提取字体名称并去重
        seen_fonts = set()
        fonts = []
        
        for font_path in font_paths:
            try:
                # 获取字体属性
                font_prop = fm.FontProperties(fname=font_path)
                font_name = font_prop.get_name()
                
                # 去重处理
                if font_name and font_name not in seen_fonts:
                    seen_fonts.add(font_name)
                    
                    # 清理字体名称，移除乱码和特殊字符
                    cleaned_font_name = font_name
                    # 移除常见的乱码字符和不可打印字符
                    cleaned_font_name = re.sub(r'[\x00-\x1f\x7f-\xff]', '', cleaned_font_name)
                    # 移除多余的空格
                    cleaned_font_name = re.sub(r'\s+', ' ', cleaned_font_name).strip()
                    
                    # 如果清理后名称为空，使用原始名称
                    if not cleaned_font_name:
                        cleaned_font_name = font_name
                    
                    # 将常见英文字体名称映射为中文名称
                    chinese_font_names = {
                        'Arial': 'Arial',
                        'Times New Roman': 'Times New Roman',
                        'Courier New': 'Courier New',
                        'Georgia': 'Georgia',
                        'Verdana': 'Verdana',
                        'Tahoma': 'Tahoma',
                        'Trebuchet MS': 'Trebuchet MS',
                        'Impact': 'Impact',
                        'Comic Sans MS': 'Comic Sans MS',
                        'Microsoft YaHei': '微软雅黑',
                        'SimSun': '宋体',
                        'SimHei': '黑体',
                        'KaiTi': '楷体',
                        'FangSong': '仿宋',
                        'LiSu': '隶书',
                        'YouYuan': '幼圆',
                        'NSimSun': '新宋体',
                        'Microsoft JhengHei': '微软正黑体',
                        'PMingLiU': '细明体',
                        'MingLiU': '明体',
                        'DFKai-SB': '标楷体'
                    }
                    
                    # 如果字体名称在映射表中，使用中文名称
                    if cleaned_font_name in chinese_font_names:
                        cleaned_font_name = chinese_font_names[cleaned_font_name]
                    
                    # 根据字体名称生成CSS值
                    css_value = f'"{cleaned_font_name}", '
                    
                    # 根据字体类型添加后备字体
                    if 'sans' in cleaned_font_name.lower() or '黑体' in cleaned_font_name or '雅黑' in cleaned_font_name:
                        css_value += 'sans-serif'
                    elif 'serif' in cleaned_font_name.lower() or '宋体' in cleaned_font_name or '楷体' in cleaned_font_name:
                        css_value += 'serif'
                    elif 'mono' in cleaned_font_name.lower() or '等宽' in cleaned_font_name:
                        css_value += 'monospace'
                    elif 'cursive' in cleaned_font_name.lower() or '手写' in cleaned_font_name:
                        css_value += 'cursive'
                    else:
                        css_value += 'sans-serif'
                    
                    # 生成预览描述
                    preview = '系统字体'
                    
                    fonts.append({
                        'name': cleaned_font_name,
                        'value': css_value,
                        'preview': preview
                    })
            except Exception as e:
                continue
        
        # 按字体名称排序
        fonts.sort(key=lambda x: x['name'])
        
        return jsonify(fonts)
    except Exception as e:
        logger.error(f'Error getting system fonts: {e}')
        # 出错时返回默认字体列表作为后备
        default_fonts = [
            { 'name': 'Arial', 'value': 'Arial, sans-serif', 'preview': '系统字体' },
            { 'name': 'Microsoft YaHei', 'value': '"Microsoft YaHei", "微软雅黑", sans-serif', 'preview': '系统字体' },
            { 'name': 'SimSun', 'value': 'SimSun, "宋体", serif', 'preview': '系统字体' }
        ]
        return jsonify(default_fonts)

# 服务CSS文件
@app.route('/css/<path:filename>')
def serve_css(filename):
    css_dir = os.path.join(os.path.dirname(__file__), 'css')
    return send_from_directory(css_dir, filename)

# 服务静态文件
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

# 初始化函数
def init_app():
    load_data()
    # 根据配置启动或停止同步线程
    control_sync_thread()

# 应用启动时初始化
init_app()

if __name__ == '__main__':
    # 生产环境请使用Gunicorn或uWSGI等WSGI服务器
    try:
        # 使用127.0.0.1代替0.0.0.0，避免某些网络配置问题
        app.run(host='127.0.0.1', port=port, debug=True)
        logger.info(f'Flask server started on http://127.0.0.1:{port}')
    except KeyboardInterrupt:
        print("\nFlask服务器已被用户中断")
    except Exception as e:
        print(f"启动Flask服务器时发生错误: {str(e)}")
        print("请检查端口5000是否被其他程序占用")
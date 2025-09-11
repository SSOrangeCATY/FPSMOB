from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import threading
import time
import logging
import requests

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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

# 加载初始数据和配置
def load_data():
    # 不再加载api_message.json，只加载配置文件
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

# 定时同步数据的线程
class DataSyncThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.running = True
        self.sync_interval = 5  # 默认5秒同步一次
        self.api_url = None
        self.api_key = None
        
    def run(self):
        while self.running:
            # 从配置中获取最新的API设置
            config_data = config.config_data
            if config_data and 'apiConfig' in config_data:
                self.api_url = config_data['apiConfig'].get('apiUrl')
                self.api_key = config_data['apiConfig'].get('apiKey')
                self.sync_interval = config_data['apiConfig'].get('refreshInterval', 5)
                
            if self.api_url:
                try:
                    logger.info(f'Trying to sync data from {self.api_url}')
                    headers = {}
                    if self.api_key:
                        headers['Authorization'] = f'Bearer {self.api_key}'
                    
                    response = requests.get(self.api_url, headers=headers)
                    if response.status_code == 200:
                        # 直接更新配置中的数据，不再保存到api_message.json
                        config.data = response.json()
                        logger.info('Data synced successfully')
                    else:
                        logger.error(f'API request failed with status code: {response.status_code}')
                except Exception as e:
                    logger.error(f'Error syncing data: {e}')
            time.sleep(self.sync_interval)
    
    def stop(self):
        self.running = False

# 创建同步线程
sync_thread = DataSyncThread()

# API路由 - 获取当前游戏数据
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(config.data)

# API路由 - 保存配置
@app.route('/api/config', methods=['POST'])
def save_config_api():
    try:
        data = request.json
        if save_config(data):
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

# API路由 - 测试API连接
@app.route('/api/config/test-connection', methods=['POST'])
def test_connection():
    try:
        data = request.json
        api_url = data.get('apiUrl')
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
    sync_thread.start()

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
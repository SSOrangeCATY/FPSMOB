import os
import subprocess
import sys
import importlib.util
from sys import platform

# 项目根目录
project_dir = os.path.dirname(os.path.abspath(__file__))

# 根据操作系统设置命令
if platform == "win32":
    python_cmd = "python"
    npm_cmd = "npm"
    which_cmd = "where"
else:
    python_cmd = "python3"
    npm_cmd = "npm"
    which_cmd = "which"

print("==== FPSMOB 依赖检测测试 ====")

# 函数：检查命令是否存在
def check_command_exists(command):
    try:
        if platform == "win32":
            result = subprocess.run([which_cmd, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            result = subprocess.run([which_cmd, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except:
        return False

# 函数：检查Python包是否已安装
def check_python_package(package_name):
    try:
        spec = importlib.util.find_spec(package_name)
        return spec is not None
    except:
        return False

# 测试Node.js和npm\print("\n[测试1] 检查Node.js和npm环境:")
node_installed = check_command_exists("node")
npm_installed = check_command_exists("npm")
print(f"- Node.js已安装: {node_installed}")
print(f"- npm已安装: {npm_installed}")

# 测试Python依赖
print("\n[测试2] 检查Python依赖:")
requirements_file = os.path.join(project_dir, "requirements.txt")
if os.path.exists(requirements_file):
    with open(requirements_file, 'r') as f:
        dependencies = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    
    print(f"从requirements.txt找到 {len(dependencies)} 个依赖项")
    
    for dep in dependencies:
        package_name = dep.split('==')[0].split('>=')[0].split('<=')[0].strip()
        if package_name == 'flask-cors':
            installed = check_python_package('flask_cors')
        elif package_name == 'python-dotenv':
            installed = check_python_package('dotenv')
        else:
            installed = check_python_package(package_name)
        print(f"- {dep}: {'✓ 已安装' if installed else '✗ 未安装'}")
else:
    print("未找到requirements.txt文件")

# 测试前端依赖
print("\n[测试3] 检查前端npm依赖:")
npm_lock_file = os.path.join(project_dir, "package-lock.json")
npm_modules_dir = os.path.join(project_dir, "node_modules")
dist_dir = os.path.join(project_dir, "dist")
print(f"- package-lock.json存在: {os.path.exists(npm_lock_file)}")
print(f"- node_modules目录存在: {os.path.exists(npm_modules_dir)}")
print(f"- dist目录存在(前端构建文件): {os.path.exists(dist_dir)}")

# 测试api_message.json文件
print("\n[测试4] 检查数据文件:")
api_message_file = os.path.join(project_dir, "api_message.json")
print(f"- api_message.json存在: {os.path.exists(api_message_file)}")

print("\n==== 测试完成 ====")
input("按Enter键退出...")
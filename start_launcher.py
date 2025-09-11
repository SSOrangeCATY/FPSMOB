import os
import subprocess
import sys
import time
import socket

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 检查端口是否被占用
def check_port(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
        return False
    except OSError:
        return True

# 启动后端服务
try:
    # 检查端口5000是否被占用，如果被占用则尝试使用5001
    port = 5000
    if check_port(port):
        print("端口5000已被占用，尝试使用端口5001...")
        port = 5001
        if check_port(port):
            print("错误: 端口5001也被占用，请关闭占用端口的程序后重试。")
            sys.exit(1)
        
    print(f"正在启动后端服务... (端口: {port})")
    # 使用Python启动app.py，移除CREATE_NEW_CONSOLE标志，使后端在同控制台运行
    backend_process = subprocess.Popen([sys.executable, os.path.join(script_dir, "app.py"), str(port)], 
                                    shell=True)
    
    # 等待2秒，确保后端服务有足够的启动时间
    print("等待后端服务启动...")
    time.sleep(2)
    
    # 检查后端进程是否仍在运行
    if backend_process.poll() is not None:
        print("错误: 后端服务启动失败，可能是由于内部错误。")
        sys.exit(1)
        
    # 打开浏览器访问配置页面
    print(f"正在打开浏览器访问配置页面... (端口: {port})")
    subprocess.Popen(["start", f"http://localhost:{port}"], shell=True)
    
    # 输出提示信息
    print("\nFPSMOB服务已启动成功！")
    print("=====================================")
    print(f"配置界面已在浏览器中打开：http://localhost:{port}")
    print(f"在OBS中添加浏览器源，URL设置为：http://localhost:{port}/live")
    print("=====================================")
    print("\n使用指南：")
    print("1. 在浏览器配置界面设置所需的显示选项")
    print("2. 在OBS中添加浏览器源并输入直播视图URL")
    print("3. 后端服务与当前控制台绑定运行")
    print("\n注意事项：")
    print("- 关闭控制台窗口即可停止FPSMOB服务")
    print("- 按Ctrl+C可以优雅地停止服务")
    print("- 如果浏览器没有自动打开，请手动访问上述URL")
    
    # 等待后端进程结束，使控制台退出时后端也退出
    backend_process.wait()
    
except KeyboardInterrupt:
    print("\nFPSMOB服务正在停止...")
    # 尝试优雅地终止后端进程
    try:
        if 'backend_process' in locals() and backend_process.poll() is None:
            backend_process.terminate()
            # 等待进程终止，最多等待5秒
            backend_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        # 如果超时，强制终止
        print("强制终止后端进程...")
        backend_process.kill()
    print("FPSMOB服务已停止。")
except Exception as e:
    print(f"启动过程中发生错误: {str(e)}")
    print("请检查Python环境和相关依赖是否正确安装。")
    # 如果后端进程已启动，尝试终止它
    if 'backend_process' in locals() and backend_process.poll() is None:
        try:
            backend_process.terminate()
        except:
            pass
    # 不使用input，程序会自动退出
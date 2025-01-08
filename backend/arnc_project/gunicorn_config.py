import os
import time
import pynvml

# 初始化 NVML
try:
    pynvml.nvmlInit()
    gpuDeviceCount = pynvml.nvmlDeviceGetCount()
except:
    gpuDeviceCount = 1

gpuDevicePool = []

def pre_fork(server, worker):
    try:
        gid = gpuDevicePool.pop(0)
    except IndexError:
        gid = (worker.age - 1) % gpuDeviceCount
    worker.gid = gid
 
def post_fork(server, worker):
    time.sleep(worker.age % server.cfg.workers)
    os.environ['CUDA_VISIBLE_DEVICES'] = str(worker.gid)
    server.log.info(f'worker(age:{worker.age}, pid:{worker.pid}, cuda:{worker.gid})')
    
def child_exit(server, worker):
    gpuDevicePool.append(worker.gid)

# 配置参数
workers = 4                     # 工作进程数
bind = 'localhost:6006'         # 绑定的IP和端口
timeout = 1200                  # 超时时间（秒）
worker_class = 'gthread'        # 使用线程而非默认的异步workers

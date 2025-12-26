import random
from math import sin, cos, pi, log
from tkinter import *

# 画布配置
CANVAS_WIDTH = 840
CANVAS_HEIGHT = 680
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11  # 图像放大倍数
HEART_COLOR = "pink"  # 心形颜色设置为粉红色

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """生成心形曲线上的点（基于参数方程）"""
    x = 17 * (sin(t) ** 3)
    y = -(16 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))  # 修正原方程重复项
    # 缩放并平移到画布中心
    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)

def scatter_inside(x, y, beta=0.15):
    """在原始点周围生成扩散点（内部填充用）"""
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def shrink(x, y, ratio):
    """收缩点坐标（用于光晕效果）"""
    force = -1 / (((x - CANVAS_CENTER_X) **2 + (y - CANVAS_CENTER_Y)** 2) **0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def curve(p):
    """动画曲线函数，控制心形收缩扩张节奏"""
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    """心形动画核心类，管理点集和帧数据"""
    def __init__(self, generate_frame=20):
        self._points = set()  # 原始心形点
        self._edge_diffusion_points = set()  # 边缘扩散点
        self._center_diffusion_points = set()  # 中心扩散点
        self.all_points = {}  # 每帧的点数据
        self.build(1000)  # 构建基础点集（优化：减少点数量）
        self.generate_frame = generate_frame  # 动画总帧数
        # 预计算所有帧的点数据
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        """构建基础点集（原始点+扩散点）"""
        # 生成原始心形点
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        
        # 生成边缘扩散点
        for _x, _y in list(self._points):
            for _ in range(3):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        
        # 生成中心扩散点（优化：减少点数量）
        point_list = list(self._points)
        for _ in range(5000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.27)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        """计算动态点位置（带随机扰动）"""
        force = 1 / (((x - CANVAS_CENTER_X)** 2 + (y - CANVAS_CENTER_Y) **2)** 0.420)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        """计算指定帧的所有点数据（包括光晕）"""
        ratio = 15 * curve(generate_frame / 10 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        # 优化：减少光晕点数量
        halo_number = int(1000 + 2000 * abs(curve(generate_frame / 10 * pi)** 2))
        all_points = []

        # 生成光晕点
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=-15)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-60, 60)
                y += random.randint(-60, 60)
                size = random.choice((1, 1, 2))
                # 添加光晕点及其偏移点
                all_points.extend([
                    (x, y, size),
                    (x + 20, y + 20, size),
                    (x - 20, y - 20, size),
                    (x + 20, y - 20, size),
                    (x - 20, y + 20, size)
                ])
        
        # 添加原始点
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        
        # 添加边缘扩散点
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        
        # 添加中心扩散点
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        
        self.all_points[generate_frame] = all_points

    def render(self, render_canvas, render_frame):
        """渲染指定帧的所有点"""
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_rectangle(
                x, y, x + size, y + size,
                width=0, fill=HEART_COLOR
            )

def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    """动画绘制循环"""
    render_canvas.delete('all')  # 清空画布
    render_heart.render(render_canvas, render_frame)  # 渲染当前帧
    # 控制帧率（优化：16ms/帧 ~60帧/秒）
    main.after(16, draw, main, render_canvas, render_heart, render_frame + 1)

if __name__ == '__main__':
    # 初始化窗口和画布
    root = Tk()
    root.title("动态心形")  # 添加窗口标题
    canvas = Canvas(root, bg='black', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
    canvas.pack()
    
    # 启动动画
    heart = Heart()
    draw(root, canvas, heart)
    root.mainloop()
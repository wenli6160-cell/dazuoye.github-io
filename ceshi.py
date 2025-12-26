import pygame
import random
from math import sin, cos, pi, log
from random import randint, uniform, choice
import tkinter as tk

# ==================== 初始化配置 ====================
pygame.init()
info = pygame.display.Info()
DISPLAY_WIDTH = info.current_w
DISPLAY_HEIGHT = info.current_h
screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("全屏特效合集")
clock = pygame.time.Clock()

# tkinter配置（删除不支持的-dontgrab属性）
tk_main = tk.Tk()
tk_main.withdraw()

# ==================== 核心配置 ====================
# 心形配置
CANVAS_CENTER_X = DISPLAY_WIDTH / 2
CANVAS_CENTER_Y = DISPLAY_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = (255, 105, 180)
HEART_FRAME_SKIP = 3

# 烟花配置
vector = pygame.math.Vector2
gravity = vector(0, 0.3)
trail_colours = [(45, 45, 45), (60, 60, 60), (75, 75, 75),
                 (125, 125, 125), (150, 150, 150)]
dynamic_offset = 1
static_offset = 5
display_mode = 3

# 弹窗配置
tips = [
    '多喝水哦~', '保持微笑呀', '每天都要元气满满',
    '记得吃水果', '保持好心情', '好好爱自己',
    '梦想成真', '期待下一次见面', '顺顺利利', '早点休息',
    '愿所有烦恼都消失', '别熬夜', '今天过得开心嘛', '天冷了，多穿衣服'
]
bg_colors = [
    'lightpink', 'skyblue', 'lightgreen', 'lavender',
    'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine',
    'mistyrose', 'honeydew', 'lavenderblush', 'oldlace'
]
windows_list = []
final_window_created = [False]
current_window_count = [0]
max_total_windows = 30
max_simultaneous_windows = 8
tip_create_interval = 200
last_tip_create_time = 0

# ==================== 心形相关 ====================
def heart_function(t, shrink_ratio=IMAGE_ENLARGE):
    x = 17 * (sin(t) ** 3)
    y = -(16 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))
    x *= shrink_ratio
    y *= shrink_ratio
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y
    return int(x), int(y)

def scatter_inside(x, y, beta=0.15):
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())
    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) **2 + (y - CANVAS_CENTER_Y)** 2) **0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy

def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    def __init__(self, generate_frame=30):
        self._points = set()
        self._edge_diffusion_points = set()
        self._center_diffusion_points = set()
        self.all_points = {}
        self.build(800)
        self.generate_frame = generate_frame
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        for _ in range(number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))
        for _x, _y in list(self._points):
            for _ in range(2):
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))
        point_list = list(self._points)
        for _ in range(3000):
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.27)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X)** 2 + (y - CANVAS_CENTER_Y) **2)** 0.420)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 15 * pi)
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 15 * pi)))
        halo_number = int(800 + 1500 * abs(curve(generate_frame / 15 * pi)** 2))
        all_points = []

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
                all_points.extend([
                    (x, y, size),
                    (x + 20, y + 20, size),
                    (x - 20, y - 20, size),
                    (x + 20, y - 20, size),
                    (x - 20, y + 20, size)
                ])
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))
        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))
        self.all_points[generate_frame] = all_points

    def render(self, frame):
        for x, y, size in self.all_points[frame % self.generate_frame]:
            pygame.draw.rect(screen, HEART_COLOR, (x, y, size, size))

# ==================== 烟花相关 ====================
class Firework:
    def __init__(self):
        self.colour = (randint(0, 255), randint(0, 255), randint(0, 255))
        self.colours = (
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255)),
            (randint(0, 255), randint(0, 255), randint(0, 255))
        )
        self.firework = Particle(randint(0, DISPLAY_WIDTH), DISPLAY_HEIGHT, True, self.colour)
        self.exploded = False
        self.particles = []
        self.min_max_particles = (150, 300)

    def update(self):
        if not self.exploded:
            self.firework.apply_force(gravity)
            self.firework.move()
            for tf in self.firework.trails:
                tf.show()
            self.show()
            if self.firework.vel.y >= 0:
                self.exploded = True
                self.explode()
        else:
            for particle in self.particles[:]:
                particle.apply_force(
                    vector(gravity.x + uniform(-1, 1) / 20, gravity.y / 2 + (randint(1, 8) / 100))
                )
                particle.move()
                for t in particle.trails:
                    t.show()
                particle.show()

    def explode(self):
        amount = randint(self.min_max_particles[0], self.min_max_particles[1])
        for _ in range(amount):
            self.particles.append(Particle(self.firework.pos.x, self.firework.pos.y, False, self.colours))

    def show(self):
        pygame.draw.circle(screen, self.colour, 
                          (int(self.firework.pos.x), int(self.firework.pos.y)), 
                          self.firework.size)

    def remove(self):
        if self.exploded:
            for p in self.particles[:]:
                if p.remove:
                    self.particles.remove(p)
            return len(self.particles) == 0
        return False

class Particle:
    def __init__(self, x, y, firework, colour):
        self.firework = firework
        self.pos = vector(x, y)
        self.origin = vector(x, y)
        self.radius = 20
        self.remove = False
        self.explosion_radius = randint(8, 22)
        self.life = 0
        self.acc = vector(0, 0)
        self.trails = []
        self.prev_posx = [-10] * 10
        self.prev_posy = [-10] * 10

        if self.firework:
            self.vel = vector(0, -randint(15, 22))
            self.size = 6
            self.colour = colour
            for i in range(5):
                self.trails.append(Trail(i, self.size, True))
        else:
            self.vel = vector(uniform(-1, 1), uniform(-1, 1))
            self.vel.x *= randint(8, self.explosion_radius + 2)
            self.vel.y *= randint(8, self.explosion_radius + 2)
            self.size = randint(3, 5)
            self.colour = choice(colour)
            for i in range(5):
                self.trails.append(Trail(i, self.size, False))

    def apply_force(self, force):
        self.acc += force

    def move(self):
        if not self.firework:
            self.vel.x *= 0.8
            self.vel.y *= 0.8
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        if self.life == 0 and not self.firework:
            distance = ((self.pos.x - self.origin.x)**2 + (self.pos.y - self.origin.y)** 2)**0.5
            if distance > self.explosion_radius:
                self.remove = True

        self.decay()
        self.trail_update()
        self.life += 1

    def show(self):
        pygame.draw.circle(screen, self.colour, 
                          (int(self.pos.x), int(self.pos.y)), 
                          self.size)

    def decay(self):
        if 50 > self.life > 10:
            ran = randint(0, 30)
            if ran == 0:
                self.remove = True
        elif self.life > 50:
            ran = randint(0, 5)
            if ran == 0:
                self.remove = True

    def trail_update(self):
        self.prev_posx.pop()
        self.prev_posx.insert(0, int(self.pos.x))
        self.prev_posy.pop()
        self.prev_posy.insert(0, int(self.pos.y))

        for n, t in enumerate(self.trails):
            if t.dynamic:
                t.get_pos(self.prev_posx[n + dynamic_offset], self.prev_posy[n + dynamic_offset])
            else:
                t.get_pos(self.prev_posx[n + static_offset], self.prev_posy[n + static_offset])

class Trail:
    def __init__(self, n, size, dynamic):
        self.pos_in_line = n
        self.pos = vector(-10, -10)
        self.dynamic = dynamic

        if self.dynamic:
            self.colour = trail_colours[n]
            self.size = int(size - n / 2)
        else:
            self.colour = (255, 255, 200)
            self.size = size - 2
            if self.size < 0:
                self.size = 0

    def get_pos(self, x, y):
        self.pos = vector(x, y)

    def show(self):
        pygame.draw.circle(screen, self.colour, 
                          (int(self.pos.x), int(self.pos.y)), 
                          self.size)

# ==================== 弹窗相关 ====================
def create_tip_window():
    if (final_window_created[0] 
        or current_window_count[0] >= max_total_windows 
        or len(windows_list) >= max_simultaneous_windows):
        return
    
    window_width = 300
    window_height = 90
    x = random.randint(20, DISPLAY_WIDTH - window_width - 20)
    y = random.randint(20, DISPLAY_HEIGHT - window_height - 20)

    try:
        window = tk.Toplevel(tk_main)
        window.title('温馨提示')
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        window.attributes('-topmost', True)
        window.attributes('-alpha', 0.9)

        tip = random.choice(tips)
        bg = random.choice(bg_colors)

        tk.Label(
            window,
            text=tip,
            bg=bg,
            font=('微软雅黑', 16),
            width=30,
            height=3,
        ).pack()

        windows_list.append(window)
        current_window_count[0] += 1

        close_delay = random.randint(1000, 3000)
        def close_window():
            if window.winfo_exists():
                window.destroy()
            if window in windows_list:
                windows_list.remove(window)
            
            if not windows_list and not final_window_created[0]:
                final_window_created[0] = True
                create_final_window()
        
        window.after(close_delay, close_window)
    except Exception as e:
        print(f"弹窗创建失败: {e}")

def create_final_window():
    final_width = 300
    final_height = 90
    x = (DISPLAY_WIDTH - final_width) // 2
    y = (DISPLAY_HEIGHT - final_height) // 2

    final_window = tk.Toplevel(tk_main)
    final_window.title('温馨提示')
    final_window.geometry(f"{final_width}x{final_height}+{x}+{y}")
    final_window.attributes('-topmost', True)

    tk.Label(
        final_window,
        text='我想你了',
        bg='lightpink',
        font=('微软雅黑', 18, 'bold'),
        width=30,
        height=3
    ).pack()

# ==================== 主函数 ====================
def main():
    heart = Heart()
    fireworks = [Firework() for _ in range(5)]
    frame_count = 0
    heart_update_counter = 0
    running = True
    global last_tip_create_time

    while running:
        current_time = pygame.time.get_ticks()
        screen.fill((0, 0, 20))

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 创建弹窗（控制频率）
        if current_time - last_tip_create_time > tip_create_interval:
            create_tip_window()
            last_tip_create_time = current_time

        # 心形渲染
        if display_mode in (1, 3):
            heart_update_counter += 1
            if heart_update_counter >= HEART_FRAME_SKIP:
                frame_count += 1
                heart_update_counter = 0
            heart.render(frame_count)

        # 烟花渲染
        if display_mode in (2, 3):
            if randint(0, 10) == 1:
                fireworks.append(Firework())
            for fw in fireworks[:]:
                fw.update()
                if fw.remove():
                    fireworks.remove(fw)

        # 更新tkinter事件
        tk_main.update_idletasks()
        tk_main.update()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    tk_main.destroy()

if __name__ == "__main__":
    main()
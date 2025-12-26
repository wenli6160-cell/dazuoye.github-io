import tkinter as tk  # 导入tkinter库，用于创建GUI界面
import random         # 导入random库，用于随机选择提示语和颜色
import time           # 导入time库，用于控制窗口创建的间隔时间

def create_tip_window(main_window, tips, bg_colors, windows_list, final_window_created):
    """
    创建一个提示窗口，并设置自动关闭
    :param main_window: 主窗口对象
    :param tips: 提示语列表
    :param bg_colors: 背景颜色列表
    :param windows_list: 存储所有窗口的列表
    :param final_window_created: 标记最终窗口是否已创建
    """
    # 如果已经创建了最终窗口，则不再创建新窗口
    if final_window_created[0]:
        return
    
    # 设置窗口的宽和高
    window_width = 300
    window_height = 90
    
    # 随机生成窗口在屏幕上的位置（x, y坐标）
    x = random.randint(-30, 1500)
    y = random.randint(-20, 900)

    # 创建顶级窗口（Toplevel）
    window = tk.Toplevel(main_window)
    window.title('温馨提示')  # 设置窗口标题
    # 设置窗口大小和位置
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # 确保窗口始终显示在最上层
    window.attributes('-topmost', True)

    # 从提示语列表中随机选择一条提示语
    tip = random.choice(tips)
    # 从颜色列表中随机选择一种背景色
    bg = random.choice(bg_colors)

    # 创建标签组件，用于显示提示语
    tk.Label(
        window,               # 父窗口
        text=tip,             # 显示的文本内容
        bg=bg,                # 背景颜色
        font=('微软雅黑', 16), # 字体设置
        width=30,             # 宽度
        height=3              # 高度
    ).pack()  # 将标签添加到窗口中

    # 将窗口添加到列表
    windows_list.append(window)
    
    # 设置窗口在随机时间后自动关闭（1-3秒）
    close_delay = random.randint(1000, 3000)
    def close_window():
        if window.winfo_exists():
            window.destroy()
        # 从列表中移除已关闭的窗口
        if window in windows_list:
            windows_list.remove(window)
            
        # 当所有窗口都关闭且未创建最终窗口时，创建最终窗口
        if not windows.winfo_exists() and not windows_list and not final_window_created[0]:
            final_window_created[0] = True
            create_final_window(main_window)
    
    window.after(close_delay, close_window)
    return window

def create_final_window(main_window):
    """创建最终的提示窗口，显示"我想你了"""
    # 设置最终窗口的宽和高
    final_width = 300
    final_height = 90
    
    # 获取屏幕的宽和高
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    
    # 计算窗口居中显示时的x, y坐标
    x = (screen_width - final_width) // 2
    y = (screen_height - final_height) // 2

    # 创建最终的顶级窗口
    final_window = tk.Toplevel(main_window)
    final_window.title('温馨提示')
    final_window.geometry(f"{final_width}x{final_height}+{x}+{y}")
    final_window.attributes('-topmost', True)

    # 创建标签组件
    tk.Label(
        final_window,
        text='我想你了',
        bg='lightpink',
        font=('微软雅黑', 18, 'bold'),
        width=30,
        height=3
    ).pack()

def main():
    """主函数，程序的入口点"""
    # 创建主窗口
    main_window = tk.Tk()
    # 隐藏主窗口
    main_window.withdraw()

    # 定义提示语列表
    tips = [
        '多喝水哦~', '保持微笑呀', '每天都要元气满满',
        '记得吃水果', '保持好心情', '好好爱自己', '我想你了',
        '梦想成真', '期待下一次见面', '顺顺利利', '早点休息',
        '愿所有烦恼都消失', '别熬夜', '今天过得开心嘛', '天冷了，多穿衣服'
    ]
    
    # 定义背景颜色列表
    bg_colors = [
        'lightpink', 'skyblue', 'lightgreen', 'lavender',
        'lightyellow', 'plum', 'coral', 'bisque', 'aquamarine',
        'mistyrose', 'honeydew', 'lavenderblush', 'oldlace'
    ]

    # 存储所有创建的提示窗口
    windows_list = []
    # 标记最终窗口是否已创建（使用列表是为了在嵌套函数中修改）
    final_window_created = [False]
    # 控制创建窗口的数量
    max_windows = 50
    current_window_count = [0]  # 使用列表是为了在嵌套函数中修改
    
    # 循环创建窗口的函数
    def create_windows():
        if current_window_count[0] < max_windows and not final_window_created[0]:
            create_tip_window(main_window, tips, bg_colors, windows_list, final_window_created)
            current_window_count[0] += 1
            # 每0.01秒创建一个新窗口
            main_window.after(10, create_windows)
    
    # 开始创建窗口
    create_windows()
    
    # 进入主事件循环
    main_window.mainloop()

if __name__ == "__main__":
    main()

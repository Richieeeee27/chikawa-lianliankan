import pygame
import random
import numpy as np
from typing import List, Tuple, Optional
import os
import time
import sys

# 初始化Pygame
pygame.init()
# 初始化显示模块
pygame.display.init()

# 设置游戏图标
icon = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "卖萌小八.png"))
pygame.display.set_icon(icon)

# 游戏常量
WINDOW_SIZE = 800  # 增加窗口大小
TOP_MARGIN = 60   # 增加顶部空间
BOTTOM_MARGIN = 60  # 增加底部空间
WINDOW_HEIGHT = WINDOW_SIZE + TOP_MARGIN + BOTTOM_MARGIN  # 窗口总高度
GRID_SIZE = 6     # 网格大小保持不变
CELL_SIZE = 100    # 增加格子大小
MARGIN = (WINDOW_SIZE - GRID_SIZE * CELL_SIZE) // 2  # 自动计算边距

# 加载背景图片
def load_background():
    """加载背景图片"""
    try:
        # 使用绝对路径
        bg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "background")
        
        # 如果背景图片文件夹不存在，创建它
        if not os.path.exists(bg_dir):
            os.makedirs(bg_dir)
            print(f"请在 {bg_dir} 文件夹中放入背景图片文件")
            return None
            
        # 查找背景图片
        bg_files = [f for f in os.listdir(bg_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        if not bg_files:
            print("未找到背景图片")
            return None
            
        # 加载第一张找到的图片作为背景
        bg_path = os.path.join(bg_dir, bg_files[0])
        original_bg = pygame.image.load(bg_path)
        # 调整背景图片大小以适应窗口
        scaled_bg = pygame.transform.scale(original_bg, (WINDOW_SIZE, WINDOW_HEIGHT))
        return scaled_bg
        
    except Exception as e:
        print(f"加载背景图片时出错: {str(e)}")
        return None

# 加载图片
def load_images():
    """加载所有图标图片"""
    images = []
    # 使用绝对路径
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
    
    # 如果图标文件夹不存在，创建它
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        print(f"请在 {image_dir} 文件夹中放入图标图片文件")
        return []
    
    try:
        # 创建一个临时surface来初始化视频模式
        temp_surface = pygame.display.set_mode((1, 1))
        
        # 获取所有图片文件
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        print(f"找到以下图片文件：{image_files}")  # 调试信息
        
        for image_file in image_files:
            try:
                # 加载图片并缩放到合适大小
                image_path = os.path.join(image_dir, image_file)
                print(f"正在加载图片：{image_path}")  # 调试信息
                
                # 使用pygame.image.load()加载图片
                original_image = pygame.image.load(image_path)
                # 转换图片格式以优化性能
                converted_image = original_image.convert_alpha()
                # 缩放图片 - 减小边距使图片更大
                scaled_image = pygame.transform.scale(converted_image, (CELL_SIZE - 2, CELL_SIZE - 2))
                images.append(scaled_image)
                print(f"成功加载图片：{image_file}")
            except Exception as e:
                print(f"无法加载图片 {image_file}: {str(e)}")
        
        # 关闭临时surface
        pygame.display.quit()
        
    except Exception as e:
        print(f"初始化显示模式时出错: {str(e)}")
        return []
    
    if not images:
        print("没有找到任何图片，将使用颜色块替代")
    else:
        print(f"成功加载了 {len(images)} 个图片")
    
    return images

# 加载图片
IMAGES = load_images()
if not IMAGES:
    # 如果没有找到图片，使用颜色块作为后备
    COLORS = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 0, 255), (0, 255, 255),
        (128, 0, 0), (0, 128, 0), (0, 0, 128),
    ]

# 按钮常量
BUTTON_WIDTH = 120  # 增加按钮宽度
BUTTON_HEIGHT = 40  # 按钮高度
BUTTON_MARGIN = 20
BUTTON_COLOR = (70, 70, 70)
BUTTON_HOVER_COLOR = (100, 100, 100)
TEXT_COLOR = (255, 255, 255)

def get_font():
    """获取系统支持的中文字体"""
    system_fonts = [
        "SimHei",  # Windows 黑体
        "Microsoft YaHei",  # Windows 微软雅黑
        "SimSun",  # Windows 宋体
        "NSimSun",  # Windows 新宋体
        "FangSong",  # Windows 仿宋
        "KaiTi"  # Windows 楷体
    ]
    for font_name in system_fonts:
        try:
            return pygame.font.SysFont(font_name, 24)  # 减小字体大小
        except:
            continue
    return pygame.font.Font(None, 28)  # 减小默认字体大小

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        self.font = get_font()

    def draw(self, screen, font):
        # 绘制按钮背景
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect)
        
        # 绘制按钮文字
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class LianLianKan:
    def __init__(self):
        # 设置窗口位置居中
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # 重新初始化显示模式
        pygame.display.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
        
        # 设置游戏图标
        try:
            icon = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "卖萌小八.png"))
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"加载图标时出错: {str(e)}")
            
        pygame.display.set_caption("Chiikawa连连看")
        self.clock = pygame.time.Clock()
        
        # 加载背景图片
        self.background = load_background()
        
        # 游戏状态
        self.current_level = 1  # 当前关卡
        self.score = 0
        self.is_paused = False
        self.game_completed = False  # 是否通关
        
        # 计时相关
        self.level_start_time = 0  # 当前关卡开始时间
        self.level_times = []      # 每关耗时记录
        self.current_time = 0      # 当前关卡已用时间
        
        # 创建按钮 - 调整按钮位置
        button_y = WINDOW_SIZE + TOP_MARGIN + (BOTTOM_MARGIN - BUTTON_HEIGHT) // 2  # 调整按钮垂直位置
        self.quit_button = Button(WINDOW_SIZE - BUTTON_WIDTH - 20, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "结束游戏")
        self.pause_button = Button(20, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "暂停")
        
        # 初始化游戏
        self.init_level()

    def init_level(self):
        """初始化当前关卡"""
        self.selected = None
        self.font = get_font()
        self.board = self.create_board()
        self.level_start_time = time.time()  # 记录关卡开始时间
        self.current_time = 0

    def create_board(self) -> np.ndarray:
        """创建游戏板，确保生成的棋盘一定可以完全通关"""
        max_attempts = 100  # 最大尝试次数
        
        for attempt in range(max_attempts):
            # 创建一个全是-1的棋盘（表示空格子）
            board = np.full((GRID_SIZE, GRID_SIZE), -1)
            
            # 获取可用的图片数量
            available_images = len(IMAGES) if IMAGES else len(COLORS)
            
            # 确保每个图片都被使用两次
            icon_indices = []
            used_images = min(available_images, 10)  # 最多使用10种不同的图片
            
            # 创建配对列表
            for i in range(used_images):
                icon_indices.extend([i, i])  # 每个图片添加两次，确保配对
            
            # 如果配对数量不够填满所需的格子，重复使用图片
            while len(icon_indices) < GRID_SIZE * GRID_SIZE:
                i = random.randint(0, used_images - 1)
                icon_indices.extend([i, i])
            
            # 打乱图片索引的顺序
            random.shuffle(icon_indices)
            
            # 创建所有可能的位置
            positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE)]
            random.shuffle(positions)
            
            # 放置图片
            for pos, icon_index in zip(positions, icon_indices):
                board[pos[0]][pos[1]] = icon_index
            
            # 检查棋盘是否有解
            if self.has_solution(board):
                print(f"找到可解的棋盘，尝试次数：{attempt + 1}")
                return board
        
        # 如果多次尝试都失败，生成一个简单的可解棋盘
        print("使用简单布局作为后备方案")
        board = np.full((GRID_SIZE, GRID_SIZE), -1)
        icon_indices = [i for i in range(used_images) for _ in range(2)]
        while len(icon_indices) < GRID_SIZE * GRID_SIZE:
            i = random.randint(0, used_images - 1)
            icon_indices.extend([i, i])
        
        # 按顺序放置图片，确保相邻的都是成对的
        for i in range(0, len(icon_indices), 2):
            row = (i // 2) // GRID_SIZE
            col = (i // 2) % GRID_SIZE
            if row < GRID_SIZE and col < GRID_SIZE:
                board[row][col] = icon_indices[i]
                board[row][col+1 if col+1 < GRID_SIZE else col-1] = icon_indices[i]
        
        return board

    def has_solution(self, board: np.ndarray) -> bool:
        """检查棋盘是否有解"""
        # 创建一个副本用于模拟消除过程
        temp_board = board.copy()
        
        while True:
            found_pair = False
            # 遍历所有格子
            for i1 in range(GRID_SIZE):
                for j1 in range(GRID_SIZE):
                    if temp_board[i1][j1] == -1:
                        continue
                    # 对于每个格子，寻找相同图案的其他格子
                    for i2 in range(GRID_SIZE):
                        for j2 in range(GRID_SIZE):
                            if (i1, j1) != (i2, j2) and temp_board[i2][j2] == temp_board[i1][j1]:
                                # 检查这两个格子是否可以连接
                                if self.can_connect_static(temp_board, (i1, j1), (i2, j2)):
                                    # 模拟消除这对图案
                                    temp_board[i1][j1] = -1
                                    temp_board[i2][j2] = -1
                                    found_pair = True
                                    break
                        if found_pair:
                            break
                    if found_pair:
                        break
            
            # 如果没有找到可以消除的对子，检查是否所有图案都已消除
            if not found_pair:
                # 如果所有格子都是-1，说明可以完全消除
                return np.all(temp_board == -1)
            
        return False

    def can_connect_static(self, board: np.ndarray, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """静态检查两个点是否可以连接（用于检查棋盘是否有解）"""
        if start == end or board[start[0]][start[1]] != board[end[0]][end[1]]:
            return False
            
        # 直线连接
        if start[0] == end[0]:  # 水平
            min_col = min(start[1], end[1])
            max_col = max(start[1], end[1])
            if all(board[start[0]][col] == -1 or col in [start[1], end[1]] 
                  for col in range(min_col, max_col + 1)):
                return True
        elif start[1] == end[1]:  # 垂直
            min_row = min(start[0], end[0])
            max_row = max(start[0], end[0])
            if all(board[row][start[1]] == -1 or row in [start[0], end[0]]
                  for row in range(min_row, max_row + 1)):
                return True

        # 一个拐角连接
        corners = [
            (start[0], end[1]),  # 水平-垂直
            (end[0], start[1])   # 垂直-水平
        ]
        
        for corner in corners:
            if board[corner[0]][corner[1]] == -1:  # 拐角处无图案
                # 检查两段路径
                path1_clear = True
                path2_clear = True
                
                # 检查第一段路径
                if corner[1] == start[1]:  # 垂直路径
                    min_row = min(start[0], corner[0])
                    max_row = max(start[0], corner[0])
                    for row in range(min_row, max_row + 1):
                        if row not in [start[0], corner[0]] and board[row][start[1]] != -1:
                            path1_clear = False
                            break
                else:  # 水平路径
                    min_col = min(start[1], corner[1])
                    max_col = max(start[1], corner[1])
                    for col in range(min_col, max_col + 1):
                        if col not in [start[1], corner[1]] and board[start[0]][col] != -1:
                            path1_clear = False
                            break
                
                # 检查第二段路径
                if corner[1] == end[1]:  # 垂直路径
                    min_row = min(corner[0], end[0])
                    max_row = max(corner[0], end[0])
                    for row in range(min_row, max_row + 1):
                        if row not in [corner[0], end[0]] and board[row][end[1]] != -1:
                            path2_clear = False
                            break
                else:  # 水平路径
                    min_col = min(corner[1], end[1])
                    max_col = max(corner[1], end[1])
                    for col in range(min_col, max_col + 1):
                        if col not in [corner[1], end[1]] and board[end[0]][col] != -1:
                            path2_clear = False
                            break
                
                if path1_clear and path2_clear:
                    return True

        # 两个拐角连接
        for i in range(GRID_SIZE):
            # 水平方向
            corner1 = (start[0], i)
            corner2 = (end[0], i)
            if (i != start[1] and i != end[1] and 
                board[corner1[0]][corner1[1]] == -1 and 
                board[corner2[0]][corner2[1]] == -1):
                if (self.can_connect_static(board, start, corner1) and 
                    self.can_connect_static(board, corner1, corner2) and 
                    self.can_connect_static(board, corner2, end)):
                    return True
            
            # 垂直方向
            corner1 = (i, start[1])
            corner2 = (i, end[1])
            if (i != start[0] and i != end[0] and 
                board[corner1[0]][corner1[1]] == -1 and 
                board[corner2[0]][corner2[1]] == -1):
                if (self.can_connect_static(board, start, corner1) and 
                    self.can_connect_static(board, corner1, corner2) and 
                    self.can_connect_static(board, corner2, end)):
                    return True
        
        return False

    def draw_ui(self):
        # 绘制底部背景
        pygame.draw.rect(self.screen, (200, 200, 200), (0, WINDOW_SIZE + TOP_MARGIN, WINDOW_SIZE, WINDOW_HEIGHT - WINDOW_SIZE - TOP_MARGIN))
        
        # 绘制顶部背景
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, WINDOW_SIZE, TOP_MARGIN))
        
        # 绘制分数和关卡信息
        score_text = self.font.render(f"分数: {self.score}", True, (0, 0, 0))
        level_text = self.font.render(f"关卡: {self.current_level}", True, (0, 0, 0))
        self.screen.blit(score_text, (20, TOP_MARGIN // 2 - 12))
        self.screen.blit(level_text, (WINDOW_SIZE - 120, TOP_MARGIN // 2 - 12))
        
        # 绘制总用时
        total_time = sum(self.level_times) + self.current_time
        minutes = int(total_time) // 60
        seconds = int(total_time) % 60
        time_text = self.font.render(f"用时: {minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        time_rect = time_text.get_rect()
        self.screen.blit(time_text, (WINDOW_SIZE // 2 - time_rect.width // 2, TOP_MARGIN // 2 - 12))
        
        # 绘制按钮
        self.quit_button.draw(self.screen, self.font)
        self.pause_button.draw(self.screen, self.font)
        
        # 如果游戏暂停，显示暂停文本
        if self.is_paused:
            pause_surface = self.font.render("游戏已暂停", True, (255, 0, 0))
            pause_rect = pause_surface.get_rect(center=(WINDOW_SIZE//2, (WINDOW_SIZE + TOP_MARGIN)//2))
            self.screen.blit(pause_surface, pause_rect)

    def update_time(self):
        if not self.is_paused:
            self.current_time = time.time() - self.level_start_time

    def draw_board(self):
        """绘制游戏板"""
        # 首先填充白色背景
        self.screen.fill((255, 255, 255))
        
        # 如果有背景图片，绘制背景
        if self.background:
            self.screen.blit(self.background, (0, 0))
        
        # 绘制半透明的游戏区域背景
        game_area = pygame.Rect(MARGIN - 5, MARGIN + TOP_MARGIN - 5, 
                              GRID_SIZE * CELL_SIZE + 10, 
                              GRID_SIZE * CELL_SIZE + 10)
        
        # 创建一个半透明的surface
        bg_surface = pygame.Surface((game_area.width, game_area.height))
        bg_surface.fill((240, 240, 240))
        bg_surface.set_alpha(230)  # 设置透明度 (0-255)
        self.screen.blit(bg_surface, game_area)
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] != -1:  # -1表示已消除
                    rect = pygame.Rect(
                        MARGIN + j * CELL_SIZE + 1,
                        MARGIN + TOP_MARGIN + i * CELL_SIZE + 1,
                        CELL_SIZE - 2,
                        CELL_SIZE - 2
                    )
                    
                    # 绘制半透明的单元格背景
                    cell_bg = pygame.Surface((CELL_SIZE - 2, CELL_SIZE - 2))
                    cell_bg.fill((255, 255, 255))
                    cell_bg.set_alpha(230)
                    self.screen.blit(cell_bg, rect)
                    
                    if IMAGES:
                        # 使用图片
                        image = IMAGES[self.board[i][j]]
                        image_rect = image.get_rect(center=rect.center)
                        self.screen.blit(image, image_rect)
                    else:
                        # 使用颜色块（作为后备）
                        pygame.draw.rect(self.screen, COLORS[self.board[i][j]], rect)
                    
                    # 如果被选中，绘制边框
                    if self.selected == (i, j):
                        pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
        
        self.draw_ui()

    def get_clicked_cell(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """获取点击的格子坐标"""
        x, y = pos
        # 调整y坐标，考虑顶部边距
        y = y - TOP_MARGIN
        
        # 检查是否在游戏区域内
        if (MARGIN <= x <= WINDOW_SIZE - MARGIN and 
            MARGIN <= y <= WINDOW_SIZE - MARGIN):
            # 计算行列
            row = (y - MARGIN) // CELL_SIZE
            col = (x - MARGIN) // CELL_SIZE
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                return row, col
        return None

    def can_connect(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """检查两个点是否可以连接"""
        if start == end or self.board[start[0]][start[1]] != self.board[end[0]][end[1]]:
            return False
        if self.board[start[0]][start[1]] == -1:
            return False

        # 直线连接
        if start[0] == end[0]:  # 水平
            min_col = min(start[1], end[1])
            max_col = max(start[1], end[1])
            path_clear = True
            for col in range(min_col + 1, max_col):
                if self.board[start[0]][col] != -1:
                    path_clear = False
                    break
            if path_clear:
                return True
                
        elif start[1] == end[1]:  # 垂直
            min_row = min(start[0], end[0])
            max_row = max(start[0], end[0])
            path_clear = True
            for row in range(min_row + 1, max_row):
                if self.board[row][start[1]] != -1:
                    path_clear = False
                    break
            if path_clear:
                return True

        # 一个拐角连接
        corners = [
            (start[0], end[1]),  # 水平-垂直
            (end[0], start[1])   # 垂直-水平
        ]
        
        for corner in corners:
            if (0 <= corner[0] < GRID_SIZE and 
                0 <= corner[1] < GRID_SIZE and 
                self.board[corner[0]][corner[1]] == -1):
                if self.check_line(start, corner) and self.check_line(corner, end):
                    return True

        # 两个拐角连接
        # 水平方向
        for i in range(GRID_SIZE):
            corner1 = (start[0], i)
            corner2 = (end[0], i)
            if (i != start[1] and i != end[1] and 
                0 <= corner1[0] < GRID_SIZE and 
                0 <= corner1[1] < GRID_SIZE and 
                0 <= corner2[0] < GRID_SIZE and 
                0 <= corner2[1] < GRID_SIZE and 
                self.board[corner1[0]][corner1[1]] == -1 and 
                self.board[corner2[0]][corner2[1]] == -1):
                if (self.check_line(start, corner1) and 
                    self.check_line(corner1, corner2) and 
                    self.check_line(corner2, end)):
                    return True

        # 垂直方向
        for i in range(GRID_SIZE):
            corner1 = (i, start[1])
            corner2 = (i, end[1])
            if (i != start[0] and i != end[0] and 
                0 <= corner1[0] < GRID_SIZE and 
                0 <= corner1[1] < GRID_SIZE and 
                0 <= corner2[0] < GRID_SIZE and 
                0 <= corner2[1] < GRID_SIZE and 
                self.board[corner1[0]][corner1[1]] == -1 and 
                self.board[corner2[0]][corner2[1]] == -1):
                if (self.check_line(start, corner1) and 
                    self.check_line(corner1, corner2) and 
                    self.check_line(corner2, end)):
                    return True

        return False

    def check_line(self, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
        """检查两点之间的直线路径是否通畅"""
        if start[0] != end[0] and start[1] != end[1]:
            return False

        if start[0] == end[0]:  # 水平线
            min_col = min(start[1], end[1])
            max_col = max(start[1], end[1])
            for col in range(min_col + 1, max_col):
                if self.board[start[0]][col] != -1:
                    return False
        else:  # 垂直线
            min_row = min(start[0], end[0])
            max_row = max(start[0], end[0])
            for row in range(min_row + 1, max_row):
                if self.board[row][start[1]] != -1:
                    return False
        return True

    def handle_click(self, pos):
        """处理鼠标点击"""
        if self.is_paused:  # 如果游戏暂停，不处理点击
            return
        
        cell = self.get_clicked_cell(pos)
        if cell is None:
            return
        
        i, j = cell
        if i >= GRID_SIZE or j >= GRID_SIZE:  # 额外的边界检查
            return
        
        if self.board[i][j] == -1:  # 如果点击了空格子
            self.selected = None
            return
        
        if self.selected is None:
            self.selected = (i, j)
        else:
            if (i, j) != self.selected:  # 确保不是点击同一个格子
                if (self.board[i][j] == self.board[self.selected[0]][self.selected[1]] and 
                    self.can_connect(self.selected, (i, j))):  # 检查图案相同且可以连接
                    # 找到配对且可以连接
                    self.board[i][j] = -1
                    self.board[self.selected[0]][self.selected[1]] = -1
                    self.score += 10
                self.selected = None
            else:
                self.selected = None  # 如果点击同一个格子，取消选择

    def handle_level_complete(self):
        """处理关卡完成"""
        # 记录当前关卡耗时
        level_time = self.current_time
        self.level_times.append(level_time)
        
        # 进入下一关
        self.current_level += 1
        self.init_level()

    def show_game_over(self):
        """显示游戏结束界面"""
        # 如果有背景图片，绘制背景
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            # 如果没有背景图片，使用灰色背景
            self.screen.fill((200, 200, 200))
        
        # 创建半透明遮罩
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_HEIGHT))
        overlay.fill((255, 255, 255))
        overlay.set_alpha(200)  # 设置透明度 (0-255)
        self.screen.blit(overlay, (0, 0))
        
        # 计算总用时
        total_time = sum(self.level_times)
        minutes = int(total_time) // 60
        seconds = int(total_time) % 60
        
        # 使用黑体字体
        completion_font = pygame.font.SysFont("SimHei", 36)
        
        # 显示结束信息
        message_text = completion_font.render("别摸鱼了，快上班！", True, (0, 0, 0))
        time_text = completion_font.render(f"总用时: {minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        score_text = completion_font.render(f"总分数: {self.score}", True, (0, 0, 0))
        level_text = completion_font.render(f"共完成 {self.current_level-1} 关", True, (0, 0, 0))
        
        # 计算文本位置
        message_rect = message_text.get_rect(center=(WINDOW_SIZE//2, (WINDOW_SIZE + TOP_MARGIN)//2 - 90))
        level_rect = level_text.get_rect(center=(WINDOW_SIZE//2, (WINDOW_SIZE + TOP_MARGIN)//2 - 30))
        time_rect = time_text.get_rect(center=(WINDOW_SIZE//2, (WINDOW_SIZE + TOP_MARGIN)//2 + 30))
        score_rect = score_text.get_rect(center=(WINDOW_SIZE//2, (WINDOW_SIZE + TOP_MARGIN)//2 + 90))
        
        # 绘制文本
        self.screen.blit(message_text, message_rect)
        self.screen.blit(level_text, level_rect)
        self.screen.blit(time_text, time_rect)
        self.screen.blit(score_text, score_rect)

    def run(self):
        """运行游戏主循环"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.quit_button.rect.collidepoint(mouse_pos):
                        self.game_completed = True  # 设置游戏完成状态
                    elif self.pause_button.rect.collidepoint(mouse_pos):
                        self.is_paused = not self.is_paused
                        if self.is_paused:
                            self.pause_start_time = time.time()
                        else:
                            # 调整关卡开始时间，补偿暂停时间
                            pause_duration = time.time() - self.pause_start_time
                            self.level_start_time += pause_duration
                    else:
                        if not self.is_paused and not self.game_completed:
                            self.handle_click(mouse_pos)
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    self.quit_button.is_hovered = self.quit_button.rect.collidepoint(mouse_pos)
                    self.pause_button.is_hovered = self.pause_button.rect.collidepoint(mouse_pos)

            # 更新游戏状态
            if not self.is_paused:
                self.update_time()
                
            self.draw_board()
            
            # 检查游戏状态
            if self.game_completed:
                self.show_game_over()
            elif np.all(self.board == -1):  # 当前关卡完成
                self.handle_level_complete()
            
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = LianLianKan()
    game.run() 
# Chiikawa连连看

一个基于 Pygame 开发的可爱的 Chiikawa 主题连连看游戏。

## 游戏特色

- 可爱的 Chiikawa 角色图片
- 无限关卡模式
- 计分系统
- 计时功能
- 暂停/继续功能
- 美观的游戏界面

## 安装要求

- Python 3.x
- Pygame
- NumPy

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/你的用户名/chiikawa-lianliankan.git
cd chiikawa-lianliankan
```

2. 安装依赖：
```bash
pip install pygame numpy
```

3. 准备游戏资源：
   - 在 `icons` 文件夹中放入 Chiikawa 角色图片
   - 在 `background` 文件夹中放入背景图片（可选）

## 运行游戏

```bash
python lianliankan.py
```

## 游戏操作

- 点击两个相同的图案进行消除
- 图案必须通过不超过两个拐角的路径连接
- 点击"暂停"按钮可以暂停游戏
- 点击"结束游戏"按钮可以结束当前游戏并查看成绩

## 游戏截图

![游戏界面](https://github.com/user-attachments/assets/d8decd73-47b7-4f9e-a37a-a0528010056f)

## 文件结构

```
chiikawa-lianliankan/
│
├── lianliankan.py    # 主游戏文件
├── README.md         # 说明文档
│
├── icons/            # 游戏图标文件夹
│   ├── 小八.png
│   ├── 吉伊.png
│   └── ...
│
└── background/       # 背景图片文件夹
    └── background.png
```


## 致谢

- Chiikawa 角色版权归原作者所有
- 游戏仅用于学习和娱乐目的 

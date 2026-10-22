# iTerm2 Tab Manager

iTerm2 标签页管理工具，通过 Python 脚本扩展原生功能，支持新建标签页时智能复用或随机分配标签页颜色。

## 功能特性

- **新建标签页** — 在当前窗口快速创建新标签页
- **颜色继承** — 自动复制当前 profile 的标签页颜色到新标签页
- **智能随机色** — 随机生成标签页颜色时，自动避开窗口内已使用的颜色（包括视觉上相近的颜色）
- **RPC 常驻** — 脚本启动后常驻内存，快捷键调用无需重复启动进程，响应速度快

## 快速开始

### 1. 部署脚本

将脚本复制到 iTerm2 的 AutoLaunch 目录：

```sh
cp scripts/AutoLaunch/create_tab_rpc.py \
   "$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch/create_tab_rpc.py"
```

### 2. 配置快捷键

打开 iTerm2 设置 → Keys → Key Bindings，添加两条映射：

| 快捷键 | 动作 | 函数调用 |
|--------|------|----------|
| `Cmd+T` | Invoke Script Function... | `create_tab(session_id: id)` |
| `Cmd+Shift+T` | Invoke Script Function... | `create_tab_with_random_color(session_id: id)` |

### 3. 重启 iTerm2

退出并重新打开 iTerm2，脚本会自动加载并注册 RPC。

> **提示**：如果不知道 Scripts 目录在哪，菜单栏 `Scripts → Manage → Reveal Scripts in Finder` 可以打开。

## 使用方法

### 基础用法

- **`Cmd+T`** — 新建标签页，继承当前标签页的颜色（如果当前 profile 启用了标签页颜色）
- **`Cmd+Shift+T`** — 新建标签页，使用随机颜色（自动避开窗口内已用颜色）

### 颜色逻辑

- **继承模式**：读取当前 session 的 profile，如果 `use_tab_color` 为 true，则复制 `tab_color` 到新标签页
- **随机模式**：遍历窗口内所有标签页，收集已用颜色，生成随机颜色时确保与每个已用色的 RGB 欧氏距离 > 40（视觉上明显不同）

## 工作原理

iTerm2 启动时自动扫描 `~/Library/Application Support/iTerm2/Scripts/AutoLaunch/` 目录，找到脚本后用配置的 Python 解释器启动进程。脚本通过 `iterm2.run_forever(main)` 常驻，`main` 函数内注册两个 RPC（`create_tab` 和 `create_tab_with_random_color`）。

按下快捷键时，iTerm2 主进程通过 IPC 通道向脚本进程发送调用请求，脚本执行对应逻辑后返回。整个过程不 fork 新进程，因此响应速度快。

**为什么改完代码要重启 iTerm2？**

脚本进程常驻内存，已加载的代码不会自动刷新。覆盖文件后必须退出并重新打开 iTerm2，它才会重新读取文件、重新注册 RPC。

**为什么按键绑定不会因重新部署而失效？**

按键绑定记录的是函数名（如 `create_tab`），不是文件路径。只要函数名不变，重新部署不影响绑定。

## 项目结构

```
iterm2-tab-manager/
├── scripts/
│   └── AutoLaunch/
│       └── create_tab_rpc.py    # iTerm2 实际运行的脚本（必须自包含）
├── src/
│   └── iterm2_tab_manager/      # 包目录（预留，供未来多脚本共用逻辑）
├── pyproject.toml               # 依赖清单（iterm2 库）
└── README.md
```

**为什么脚本必须自包含？**

iTerm2 用它自己配置的脚本解释器执行 AutoLaunch 目录里的文件，不会使用本项目的 Python 环境（没有 venv，也不 import 本项目的包）。因此所有逻辑必须写在单个脚本文件里。

## 开发

### 本地开发流程

1. 编辑 `scripts/AutoLaunch/create_tab_rpc.py`
2. 复制到 iTerm2 AutoLaunch 目录（见上方「部署脚本」）
3. 退出并重新打开 iTerm2
4. 测试快捷键

### 依赖

- Python ≥ 3.10
- `iterm2` 库（iTerm2 官方 Python API）

开发环境可通过 `pip install -e .` 安装依赖，方便编辑器提供类型提示和自动补全。

### 添加新功能

当前只有一个脚本，新功能直接写在 `create_tab_rpc.py` 里。等出现第二个需要共用逻辑的脚本时，再把公共部分抽到 `src/iterm2_tab_manager/` 包里。

## 许可证

MIT

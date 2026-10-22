# iTerm2 Tab Manager

用于 iTerm2 脚本化的小工具集合。

计划的功能：

- 在当前 iTerm2 窗口新建标签页
- 可选地把当前 profile 的设置复制到新会话
- 后续扩展更多标签页/会话管理动作

## 目录结构

- `scripts/AutoLaunch/create_tab_rpc.py` - iTerm2 实际运行的唯一脚本。它必须保持自包含：iTerm2 用它自己配置的脚本解释器来执行，不会用本项目的 Python 环境
- `src/iterm2_tab_manager/` - 占用的包目录，留给以后多个脚本共用的逻辑
- `pyproject.toml` - 依赖清单，主要作用是让 `pip install -e .` 能给开发环境提供 `iterm2` 库

## 当前状态

新建标签页、并沿用当前 profile 标签页颜色的逻辑已经可用。后续新增的标签页/会话动作先继续写在 `create_tab_rpc.py` 里，等出现第二个需要共用这些逻辑的脚本时再抽到包里。

## 快捷键设置

在 iTerm2 里把 `Cmd+Shift+T` 绑定为直接调用已注册的 RPC。

推荐步骤：

1. 打开 iTerm2 设置，进入 Keys / Key Bindings（按键映射）部分。
2. 新增一条 `Cmd+Shift+T` 的映射。
3. 动作选择 `Invoke Script Function...`（调用脚本函数）。
4. 填入函数调用：`create_tab(session_id: id)`
5. 把 `scripts/AutoLaunch/create_tab_rpc.py` 复制到 iTerm2 的 AutoLaunch Scripts 目录（见下方「部署」）。
6. 重启一次 iTerm2，让常驻脚本注册这个 RPC。

如果想要随机标签页颜色，改用：

`create_tab_with_random_color(session_id: id)`

脚本会在当前窗口新建标签页；当前 profile 用了标签页颜色时，新标签页沿用同一颜色。随机颜色的版本会先收集本窗口各标签页已在用的颜色，避开重复。

不知道 iTerm2 的 Scripts 目录在哪，就用菜单栏的 `Scripts -> Manage -> Reveal Scripts in Finder`。

如果还有按键绑定指向之前那两个一次性脚本，改成指向上面的 RPC。那两个脚本每次按键都要经过 Scripts 菜单启动，比直接调用已注册的 RPC 慢，而且仓库里已经删掉了。

## 部署

iTerm2 不会读取本仓库，它运行的是自己 AutoLaunch 目录里的独立副本：

```
~/Library/Application Support/iTerm2/Scripts/AutoLaunch/create_tab_rpc.py
```

只改仓库里的文件不会生效。每次改完都要复制过去，再重启常驻脚本：

```sh
cp scripts/AutoLaunch/create_tab_rpc.py \
   "$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch/create_tab_rpc.py"
```

脚本结尾是 `iterm2.run_forever`，启动后会一直存活，并把已加载的代码留在内存里。所以光覆盖文件不够，必须退出并重新打开 iTerm2，它才会重新读取文件、重新注册 RPC。

按键是按函数名调用 RPC 的，不记录文件路径，因此重新部署不会弄坏绑定；但改函数名会——上面两个名字必须和按键设置里记录的保持一致。

# -*- coding: utf-8 -*-
"""TextMate 偏好设置面板（Preferences）正文汉化表 —— 第二批。

与菜单表（zh_menu.py）分开维护：这里全部是「偏好设置面板正文」的纯显示文案。
每条都已对照 macromates/textmate 源码用「完整字符串字面量」检索过，
确认只作为 NSTextField / NSButton / NSTableColumn 的标题（label / title）出现，
不参与 identifier、defaults key、资源名、payload 值。因此可以安全翻译。

刻意排除的条目（有非显示用途，翻了会改变行为）：
  "Anonymous"            → 同时是 defaults 默认值 + 崩溃报告 payload 里的联系人兜底值
  "Never"                → 同时是「选择语法」弹窗的按钮标题，中文语境下语义不对
  "%.0f minutes ago" 等  → 同时被 format_string.cc 用于 ${...} 时长展开，影响命令输出
  "Bundle"               → 同时是捆绑编辑器新建项的默认名称
  "Files"/"Projects"/…   → 面板 identifier + 图标资源名，见 zh_pane.py（单独实验）
"""

# ── Projects 面板 ───────────────────────────────
ZH_PROJECTS = {
    "File browser location:":        "文件浏览器位置：",
    "Folders on top":                "文件夹置顶",
    "Show links as expandable":      "将链接显示为可展开",
    "Open files on single click":    "单击打开文件",
    "Keep current document selected": "保持当前文稿选中",
    "Show file browser on:":         "文件浏览器显示于：",
    "Left side":                     "左侧",
    "Right side":                    "右侧",
    "Adjust window when toggleing display": "切换显示时调整窗口",
    "Document tabs:":                "文稿标签页：",
    "Show for single document":      "单个文稿时显示",
    "Re-order when opening a file":  "打开文件时重排序",
    "Automatically close unused tabs": "自动关闭未使用的标签页",
    "Exclude files matching:":       "排除匹配的文件：",
    "Include files matching:":       "包含匹配的文件：",
    "Non-text files:":               "非文本文件：",
    "Show command output:":          "显示命令输出：",
    "Below text view":               "文本框下方",
    "Right of text view":            "文本框右侧",
    "New window":                    "新窗口",
}

# ── Software Update 面板 ────────────────────────
ZH_SOFTWARE_UPDATE = {
    "Software update:":              "软件更新：",
    "Watch for:":                    "关注：",
    "Normal releases":               "正式版",
    "Prereleases":                   "预览版",
    "Ask before downloading updates": "下载更新前先询问",
    "Last check:":                   "上次检查：",
    "Crash reports:":                "崩溃报告：",
    "Submit to MacroMates":          "提交给 MacroMates",
    "Contact:":                      "联系人：",
    "Some time ago":                 "一段时间前",
    "Just now":                      "刚刚",
    "Checking…":                     "正在检查…",
    # 相对时间：macOS 10.15+ 走系统的 NSRelativeDateTimeFormatter（自动中文），
    # 下面几条只在旧系统上兜底，但顺手翻了。
    "Less than a minute ago":        "不到一分钟前",
    "1 minute ago":                  "1 分钟前",
    "1 hour ago":                    "1 小时前",
    "Yesterday":                     "昨天",
    "Last week":                     "上周",
    "Last month":                    "上个月",
    "Last year":                     "去年",
}

# ── Files 面板补漏 ──────────────────────────────
ZH_FILES = {
    "CR (Mac Classic)":              "CR（Mac 经典）",
    "CRLF (Windows)":                "CRLF（Windows）",
}

# ── Variables 面板 ──────────────────────────────
ZH_VARIABLES = {
    "Variable Name":                 "变量名",
    "Value":                         "值",
}

# ── Bundles 面板 ────────────────────────────────
ZH_BUNDLES = {
    "Updated":                       "更新时间",
    "Description":                   "描述",
    "Check for and install updates automatically": "自动检查并安装更新",
    "Bundle index last updated: %@": "捆绑索引最后更新：%@",
    "Installing ‘%@’ bundle…":       "正在安装捆绑“%@”…",
    "Installed ‘%@’ bundle.":        "已安装捆绑“%@”。",
    "Installed ‘%@’ bundle and one dependency.": "已安装捆绑“%@”及 1 个依赖项。",
    "Installed ‘%@’ bundle and %ld dependencies.": "已安装捆绑“%@”及 %ld 个依赖项。",
    "Uninstalled ‘%@’ bundle.":      "已卸载捆绑“%@”。",
    "Error installing ‘%@’ bundle.": "安装捆绑“%@”时出错。",
}

# ── Terminal 面板（二进制里的对话框文案；nib 两条见 NIB_TERMINAL）──
ZH_TERMINAL = {
    "Update Shell Support":          "更新 Shell 支持",
    "Would you like to update the installed version of mate to version %@?": "要把已安装的 mate 更新到 %@ 版吗？",
    "Unable to find ‘mate’":         "找不到“mate”",
    "The ‘mate’ binary is missing from the application bundle. We recommend that you re-download the application.":
        "应用程序包中缺少“mate”可执行文件，建议重新下载应用程序。",
    "File Already Exists":           "文件已存在",
    "Update":                        "更新",
}

ZH_PREF = {}
for _d in (ZH_PROJECTS, ZH_SOFTWARE_UPDATE, ZH_FILES, ZH_VARIABLES, ZH_BUNDLES, ZH_TERMINAL):
    ZH_PREF.update(_d)

# ── nib 补充（TerminalPreferences.nib 里上一轮漏掉的两条）──
# 保持 ${...} 模板语法原样，只换外面的话。
NIB_TERMINAL = {
    "Shell support ${installed:?:not }installed":
        "Shell 支持${installed:?已安装:未安装}",
    "To use TextMate as editor for subversion, git, and similar you need to install the mate shell command and add a line like the following to ~/.bashrc:\n\n\texport EDITOR=\"${mate_path/^~/\\$HOME/} -w\"\n\nFor more information use the help button down in the corner.":
        "若要把 TextMate 当作 subversion、git 等工具的编辑器，需要安装 mate 命令行工具，并在 ~/.bashrc 中加入类似下面的一行：\n\n\texport EDITOR=\"${mate_path/^~/\\$HOME/} -w\"\n\n更多信息请点角落里的帮助按钮。",
}

# ── 面板标题（identifier + 图标资源名，风险高，单独实验）──
ZH_PANE_TITLE = {
    "Files":            "文件",
    "Projects":         "项目",
    "Variables":        "变量",
    "Software Update":  "软件更新",
    "Terminal":         "终端",
}
# 面板标题翻译后，图标资源名也变了，需要补上同名的图片文件
PANE_ICONS = {
    "Projects":         "项目",
    "Variables":        "变量",
    "Software Update":  "软件更新",
    "Terminal":         "终端",
}

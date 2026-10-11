# -*- coding: utf-8 -*-
"""TextMate 菜单 / UI 汉化对照表。

容量规则（由 CFString 存储方式决定）：
  ascii 条目(flags 0x7c8) 数据按 1 字节/字符存放，改为 UTF-16 后
      可用汉字数 = 原 length // 2
  u16   条目(flags 0x7d0) 数据按 2 字节/字符存放
      可用汉字数 = 原 length
装不下的条目由 patch_binary.py 自动转入新增段，不在此处妥协译文。
"""

ZH_MENU = {
    # ── 应用程序菜单 ──────────────────────────────
    "About": "关于",
    "Changes": "更新记录",
    "Registration": "注册",
    "Legal": "法律信息",
    "Contributions": "贡献者",
    "About TextMate": "关于 TextMate",
    "Check for Update": "检查更新",
    "Check for Test Build": "检查测试版",
    "Services": "服务",
    "Hide TextMate": "隐藏 TextMate",
    "Hide Others": "隐藏其他",
    "Show All": "显示全部",
    "Quit TextMate": "退出 TextMate",
    "Preferences…": "偏好设置…",
    "Other…": "其他…",
    "TextMate Help": "TextMate 帮助",

    # ── File ────────────────────────────────────
    "File": "文件",
    "New": "新建",
    "New File Browser": "新建文件浏览器",
    "New Tab": "新建标签页",
    "Open…": "打开…",
    "Open Quickly…": "快速打开…",
    "Open Recent": "打开最近使用",
    "Clear Menu": "清除菜单",
    "Open Recent Project…": "打开最近的项目…",
    "Close": "关闭",
    "Close Window": "关闭窗口",
    "Close All Tabs": "关闭所有标签页",
    "Close Other Tabs": "关闭其他标签页",
    "Close Tabs to the Right": "关闭右侧标签页",
    "Close Tabs to the Left": "关闭左侧标签页",
    "Sticky": "固定",
    "Save": "保存",
    "Save As…": "另存为…",
    "Save All": "全部保存",
    "Revert": "还原",
    "Page Setup…": "页面设置…",
    "Print…": "打印…",

    # ── Edit ────────────────────────────────────
    "Edit": "编辑",
    "Undo": "撤销",
    "Redo": "重做",
    "Cut": "剪切",
    "Copy": "复制",
    "Paste": "粘贴",
    "Paste Without Indenting": "不缩进粘贴",
    "Paste Next": "粘贴下一项",
    "Paste Previous": "粘贴上一项",
    "Show History": "显示历史记录",
    "Delete": "删除",
    "Macros": "宏",
    "Start Recording": "开始录制",
    "Replay Macro": "回放宏",
    "Save Macro…": "保存宏…",
    "Select": "选择",
    "Word": "单词",
    "Line": "行",
    "Paragraph": "段落",
    "Current Scope": "当前作用域",
    "Enclosing Typing Pairs": "外层成对符号",
    "All": "全部",
    "Toggle Column Selection": "切换列选择",

    # ── Find ────────────────────────────────────
    "Find": "查找",
    "Find and Replace…": "查找替换…",
    "Find in Project…": "在项目中查找…",
    "Find in Folder…": "在文件夹中查找…",
    "Show Find History": "显示查找历史",
    "Incremental Search": "增量搜索",
    "Incremental Search Previous": "反向增量搜索",
    "Find Next": "查找下一个",
    "Find Previous": "查找上一个",
    "Find All": "查找全部",
    "Find Options": "查找选项",
    "Ignore Case": "忽略大小写",
    "Regular Expression": "正则表达式",
    "Ignore Whitespace": "忽略空白",
    "Wrap Around": "循环查找",
    "Replace": "替换",
    "Replace & Find": "替换并查找",
    "Replace All": "全部替换",
    "Replace All in Selection": "替换选区内全部",
    "Use Selection for Find": "用选区作为查找内容",
    "Use Selection for Replace": "用选区作为替换内容",
    "Spelling": "拼写",
    "Spelling…": "拼写…",
    "Check Document Now": "立即检查文档",
    "Check Spelling While Typing": "输入时检查拼写",

    # ── View ────────────────────────────────────
    "View": "视图",
    "Font": "字体",
    "Show Fonts": "显示字体",
    "Bigger": "放大",
    "Smaller": "缩小",
    "Default Size": "默认大小",
    "Show File Browser": "显示文件浏览器",
    "Hide File Browser": "隐藏文件浏览器",
    # 去空格以塞进 15 字节的原位（ascii 条目改 UTF-16 后只有 7 个字符的余量）
    "Show HTML Output": "显示HTML输出",
    "Hide HTML Output": "隐藏HTML输出",
    "Show Line Numbers": "显示行号",
    "Hide Line Numbers": "隐藏行号",
    "Show Invisibles": "显示不可见字符",
    # 运行时动态换标题的变体（Show↔Hide / Enable↔Disable），实测截图漏网的就是这批
    "Show Invisible Characters": "显示不可见字符",
    "Hide Invisible Characters": "隐藏不可见字符",
    "Enable Soft Wrap": "启用软换行",
    "Disable Soft Wrap": "停用软换行",
    "Show Wrap Column": "显示换行列",
    "Hide Wrap Column": "隐藏换行列",
    "Show Indent Guides": "显示缩进参考线",
    "Hide Indent Guides": "隐藏缩进参考线",
    "Wrap Column": "换行列",
    "Tab Size": "制表符宽度",
    "Theme": "主题",
    "Fold Current Block": "折叠当前块",
    "Toggle Foldings at Level": "切换层级折叠",
    "All Levels": "所有层级",
    "Toggle Scroll Past End": "切换末尾滚动",
    "Allow Scroll Past End": "允许超出末尾滚动",
    "Toggle Case of Character / Selection": "切换单词/选区大小写",
    "View Source": "查看源代码",
    "Enter Full Screen": "进入全屏",
    "Customize Touch Bar…": "自定义触控栏…",

    # ── Navigate ────────────────────────────────
    "Navigate": "导航",
    "Jump to Line…": "跳转到行…",
    "Jump to Symbol…": "跳转到符号…",
    "Jump to Selection": "跳转到选区",
    "Set Bookmark": "设置书签",
    "Jump to Next Bookmark": "跳到下一个书签",
    "Jump to Previous Bookmark": "跳到上一个书签",
    "Jump to Bookmark": "跳转到书签",
    "Jump to Next Mark": "跳到下一个标记",
    "Jump to Previous Mark": "跳到上一个标记",
    "Scroll": "滚动",
    "Line Up": "上移一行",
    "Line Down": "下移一行",
    "Column Left": "左移一列",
    "Column Right": "右移一列",
    "Go to Related File": "转到相关文件",
    "Move Focus to File Browser": "焦点移到文件浏览器",

    # ── Text ────────────────────────────────────
    "Text": "文本",
    "Transpose": "交换",
    "Move Selection": "移动选区",
    "Up": "上",
    "Down": "下",
    "Left": "左",
    "Right": "右",
    "Toggle Case of Word / Selection": "切换单词/选区大小写",
    "Uppercase Word / Selection": "单词/选区转为大写",
    "Lowercase Word / Selection": "单词/选区转为小写",
    "Titlecase Line / Selection": "行/选区转为标题式",
    "Shift Left": "左移",
    "Shift Right": "右移",
    "Indent Line / Selection": "缩进行/选区",
    "Reformat Text": "重排文本",
    "Reformat Text and Justify": "重排并对齐文本",
    "Unwrap Paragraph": "取消段落换行",
    "Filter Through Command…": "通过命令过滤…",

    # ── 文件浏览器 ──────────────────────────────
    "File Browser": "文件浏览器",
    "New File": "新建文件",
    "New Folder": "新建文件夹",
    "Back": "后退",
    "Forward": "前进",
    "Enclosing Folder": "上层文件夹",
    "Select Document": "选择文档",
    "Select None": "取消选择",
    "Project Folder": "项目文件夹",
    "SCM Status": "SCM 状态",
    "Computer": "电脑",
    "Home": "个人",
    "Desktop": "桌面",
    "Favorites": "个人收藏",
    "Go to Folder…": "前往文件夹…",
    "Reload": "重新载入",

    # ── Bundles ─────────────────────────────────
    "Bundles": "捆绑",
    "Select Bundle Item…": "选择捆绑项…",
    "Edit Bundles…": "编辑捆绑…",
    "Export Bundle…": "导出捆绑…",

    # ── Window ──────────────────────────────────
    "Window": "窗口",
    "Minimize": "最小化",
    "Zoom": "缩放",
    "Show Previous Tab": "显示上一个标签页",
    "Show Next Tab": "显示下一个标签页",
    "Show Tab": "显示标签页",
    "Move Tab to New Window": "标签页移到新窗口",
    "Merge All Windows": "合并所有窗口",
    "Bring All to Front": "全部前置",

    # ── Help ────────────────────────────────────
    "Help": "帮助",

}

# 非菜单项：对话框、按钮、偏好面板标识。
# 暂不启用 —— 这些字符串很可能同时被代码当作 key 使用（例如 General / Editor /
# Projects / Variables / Terminal 是偏好设置面板的 identifier），改掉会让查找返回
# nil 并崩溃。要启用需逐条实测。
ZH_DIALOG = {
    "Cancel": "取消",
    "OK": "好",
    "Install": "安装",
    "Relaunch": "重新启动",
    "Move to Trash": "移到废纸篓",
    "Skip Loading": "跳过加载",
    "Cannot Install Plug-in": "无法安装插件",
    "Plug-in Already Installed": "插件已安装",
    "Install Failed": "安装失败",
    "Plug-in Installed": "插件已安装",
    "Open": "打开",
    "Rename": "重命名",
    "Duplicate": "制作副本",
    "Quick Look": "快速查看",
    "Close Tab": "关闭标签页",
    "New Document": "新建文稿",
    "Remove": "移除",
    "Add": "添加",
    "Create": "创建",
    "Continue": "继续",
    "Download": "下载",
    "Later": "稍后",
    "Retry": "重试",
    "Update": "更新",
    "Overwrite": "覆盖",
    "Show in Finder": "在 Finder 中显示",
    "Bundle Editor": "捆绑编辑器",
    "Create New Item": "新建项目",
    "General": "通用",
    "Editor": "编辑器",
    "Projects": "项目",
    "Variables": "变量",
    "Search": "搜索",
    "Previous": "上一个",
    "Next": "下一个",
    "Default": "默认",
    "Remove key equivalent": "移除快捷键",
    "Key Equivalent": "快捷键",
}

# 实测结论：单词类字符串极可能被代码当 identifier / defaults key 用。
# 崩溃点 -[AppController applicationWillFinishLaunching:] 里
# std::string(char const*) 收到 nullptr —— 拿某个串去查表，查不到返回 nil，
# 再 UTF8String 就是空指针。
# General / Editor / Projects / Variables / Terminal 是偏好面板 identifier；
# Default / Search / Open / Remove / Add / Update 等单词同理危险。
# 因此这里只放行「多词短语」——按钮标题、对话框标题，几乎不可能当 key。
# ── 待排查条目 ──────────────────────────────────
# 2026-10-11 02:45 加的这批会导致偏好设置窗口打不开，暂时停用待二分定位。
# 用 patch_binary.py --with-extra 才会启用。
ZH_EXTRA = {
    "Files": "文件",
    "Terminal": "终端",
    # ── 保存确认对话框 ──
    # ── 软件更新弹窗 / 面板 ──
    # ── 偏好设置面板标签（toolbar 标题；General/Editor 已证崩，这五个待验证）──
    "Projects": "项目",
    "Variables": "变量",
    "Software Update": "软件更新",
}

ZH_DIALOG_SAFE = {
    "Cancel": "取消",
    "Move to Trash": "移到废纸篓",
    "Skip Loading": "跳过加载",
    "Cannot Install Plug-in": "无法安装插件",
    "Plug-in Already Installed": "插件已安装",
    "Install Failed": "安装失败",
    "Plug-in Installed": "插件已安装",
    "Quick Look": "快速查看",
    "Close Tab": "关闭标签页",
    "New Document": "新建文稿",
    "Show in Finder": "在 Finder 中显示",
    "Bundle Editor": "捆绑编辑器",
    "Create New Item": "新建项目",
    "Remove key equivalent": "移除快捷键",
    "Key Equivalent": "快捷键",
    # 文件浏览器右键 / 录制 / 查找窗口（同为多词短语，低风险）
    "Show Original": "显示原件",
    "Show Enclosing Folder": "显示上层文件夹",
    "Show Package Contents": "显示包内容",
    "Show Hidden Files": "显示隐藏文件",
    "Hide Invisible Files": "隐藏不可见文件",
    "Stop Recording": "停止录制",
    "Stop Search": "停止搜索",
}

# ── 批次 A：经单独验证与偏好设置窗口无关的部分 ──────────
# 2026-10-11 02:52 加入。保存确认对话框 + 软件更新弹窗。
# 面板标题（Files/Terminal/Projects/Variables/Software Update）已逐个二分确认：
#   Files 单独启用 → 偏好设置打不开；Files+Terminal → 打不开。
# 结论：标题被当作面板查找 key，翻译后窗口控制器构建失败。永久不翻。
ZH_BATCH_A = {
    "At startup:": "启动时：",
    "Open documents from last session": "打开上次会话的文稿",
    "Hold shift (⇧) to bypass": "按住 shift (⇧) 可跳过",
    "With no open documents:": "没有打开的文稿时：",
    "Create one at startup": "启动时新建一个",
    "Create one when re-activated": "重新激活时新建一个",
    "New document type:": "新建文稿类型：",
    "Unknown document type:": "未知文稿类型：",
    "Prompt for type": "询问类型",
    "Encoding:": "编码：",
    "Line endings": "换行符",
    "Line endings:": "换行符：",
    "LF (recommended)": "LF（推荐）",
    "Do you want to save the changes you made in the document “%@”?": "要保存你在文稿“%@”中所做的更改吗？",
    "Your changes will be lost if you don’t save them.": "如果不保存，你的更改将会丢失。",
    "Don’t Save": "不保存",
    "Do you want to save the changes made to the bundle named “%@”?": "要保存对捆绑“%@”所做的更改吗？",
    "Do you want to save documents with changes?": "要保存有更改的文稿吗？",
    "The document “%@” could not be saved.": "文稿“%@”无法保存。",
    "Up To Date": "已是最新版本",
    "You are running %@ which is the latest version available.": "你正在运行 %@，这已是可用的最新版本。",
    "%@ is the latest version available. You have version %@.": "%@ 是可用的最新版本，你当前是 %@。",
    "Error Checking for Update": "检查更新时出错",
    "Error Downloading Update": "下载更新时出错",
    "Failed to Install Update": "安装更新失败",
    "Check Now": "立即检查",
    "OK": "好",
}
ZH_DIALOG_SAFE.update(ZH_BATCH_A)


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查看 TextMate 汉化状态。用法: check.py [--app /Applications/TextMate.app]"""
import argparse, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "tools"))

from macho import MachO                      # noqa: E402
from zh_menu import ZH_MENU, ZH_DIALOG_SAFE  # noqa: E402
from zh_pref import ZH_PREF, ZH_PANE_TITLE   # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/Applications/TextMate.app")
    args = ap.parse_args()
    app = args.app.rstrip("/")
    bin_path = os.path.join(app, "Contents/MacOS/TextMate")
    res = os.path.join(app, "Contents/Resources")

    if not os.path.exists(bin_path):
        print(f"找不到 {bin_path}")
        return 1

    ver = subprocess.run(["/usr/libexec/PlistBuddy", "-c", "Print :CFBundleShortVersionString",
                          os.path.join(app, "Contents/Info.plist")],
                         capture_output=True, text=True).stdout.strip()
    bld = subprocess.run(["/usr/libexec/PlistBuddy", "-c", "Print :CFBundleVersion",
                          os.path.join(app, "Contents/Info.plist")],
                         capture_output=True, text=True).stdout.strip()

    print(f"目标      : {app}")
    print(f"版本      : {ver} ({bld})")

    try:
        texts = set(e["text"] for e in MachO(bin_path).cstrings() if e["text"] is not None)
    except Exception as e:
        print(f"读取二进制失败: {e}")
        return 1

    layers = [
        ("菜单栏", ZH_MENU),
        ("对话框/按钮", ZH_DIALOG_SAFE),
        ("偏好设置正文", ZH_PREF),
        ("偏好设置面板标题", ZH_PANE_TITLE),
    ]
    total_hit = total = 0
    print("")
    for name, table in layers:
        zh = set(table.values())
        hit = sum(1 for v in zh if v in texts)
        total_hit += hit
        total += len(zh)
        flag = "✅" if hit == len(zh) else ("❌" if hit == 0 else "⚠️ ")
        print(f"{flag} {name:<20} {hit:>3} / {len(zh)}")

    print("")
    print(f"二进制译文: {total_hit} / {total}")

    # 资源
    lproj = os.path.join(res, "zh-Hans.lproj")
    nibs = len([f for f in os.listdir(lproj) if f.endswith(".nib")]) if os.path.isdir(lproj) else 0
    print(f"语言包    : {'✅' if nibs else '❌'} zh-Hans.lproj（{nibs} 个 nib）")

    icons = [f for f in ("项目.png", "变量.png", "软件更新.png", "终端.png")
             if os.path.exists(os.path.join(res, f))]
    print(f"面板图标  : {'✅' if len(icons) == 4 else '⚠️ '} {len(icons)} / 4")

    about = os.path.join(res, "About/About.html")
    zh_about = False
    if os.path.exists(about):
        try:
            zh_about = "关于" in open(about, encoding="utf-8", errors="ignore").read()[:4000]
        except Exception:
            pass
    print(f"关于窗口  : {'✅ 中文' if zh_about else '❌ 英文/未知'}")

    # 签名
    sig = subprocess.run(["codesign", "-v", app], capture_output=True, text=True)
    print(f"代码签名  : {'✅ 有效' if sig.returncode == 0 else '❌ ' + sig.stderr.strip()[:60]}")

    # 面板记忆键（defaults 会把中文输出成 \uXXXX 转义）
    d = subprocess.run(["defaults", "read", "com.macromates.TextMate",
                        "MASPreferences Selected Identifier View"], capture_output=True, text=True)
    val = d.stdout.strip()
    if val.startswith('"') and val.endswith('"'):
        val = val[1:-1]

    def unescape(s):
        out, i = [], 0
        while i < len(s):
            if s[i] == "\\" and i + 5 < len(s) and s[i + 1] == "u":
                try:
                    out.append(chr(int(s[i + 2:i + 6], 16)))
                    i += 6
                    continue
                except ValueError:
                    pass
            out.append(s[i])
            i += 1
        return "".join(out)

    val = unescape(val)
    if d.returncode != 0 or not val:
        print("面板记忆  : ✅ 未设置（正常）")
    elif any('\u4e00' <= c <= '\u9fff' for c in val):
        print(f"面板记忆  : ✅ {val}")
    else:
        print(f"面板记忆  : ⚠️  残留英文值 {val!r} —— 偏好设置窗口可能打不开，"
              f"跑: defaults delete com.macromates.TextMate \"MASPreferences Selected Identifier View\"")

    # 进程
    running = subprocess.run(["pgrep", "-x", "TextMate"], capture_output=True).returncode == 0
    print(f"运行状态  : {'运行中' if running else '未运行'}")

    print("")
    if total_hit == total and nibs and len(icons) == 4:
        print("结论: 汉化完整 ✅")
    elif total_hit == 0 and not nibs:
        print("结论: 官方英文原版")
    else:
        print("结论: 部分汉化 ⚠️")
    return 0


if __name__ == "__main__":
    sys.exit(main())

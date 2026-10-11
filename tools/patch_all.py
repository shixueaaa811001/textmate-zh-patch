# -*- coding: utf-8 -*-
"""全量打补丁：从官方原版二进制一次性应用所有层。

TextMate 自动更新会整个覆盖 App，汉化会丢。更新后跑这个重建：

  python3 patch_all.py --base <官方原版二进制> --out /tmp/TextMate_new
  sudo cp /tmp/TextMate_new /Applications/TextMate.app/Contents/MacOS/TextMate
  codesign --force --sign - --timestamp=none /Applications/TextMate.app
  defaults delete com.macromates.TextMate "MASPreferences Selected Identifier View"

层：
  1. 菜单栏            zh_menu.ZH_MENU
  2. 对话框 / 按钮短语  zh_menu.ZH_DIALOG_SAFE
  3. 偏好设置面板正文   zh_pref.ZH_PREF
  4. 偏好设置面板标题   zh_pref.ZH_PANE_TITLE   ← 需要同步补 4 个中文名图标
"""
import argparse, hashlib, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patch_binary import Patcher
from macho import MachO
from zh_menu import ZH_MENU, ZH_DIALOG_SAFE
from zh_pref import ZH_PREF, ZH_PANE_TITLE


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-pane", action="store_true", help="不打面板标题（保英文标题）")
    ap.add_argument("--no-holes", action="store_true")
    args = ap.parse_args()

    table = {}
    table.update(ZH_MENU)
    table.update(ZH_DIALOG_SAFE)
    table.update(ZH_PREF)
    if not args.no_pane:
        table.update(ZH_PANE_TITLE)

    base_size = os.path.getsize(args.base)
    p = Patcher(args.base)
    ents = [e for e in p.entries if e["kind"] in ("ascii", "u16")]
    have = set(e["text"] for e in ents)
    miss = [k for k in table if k not in have]
    print(f"可改写条目 {len(ents)} / 翻译表 {len(table)} 条 / 未命中 {len(miss)}")
    if miss:
        print("  未命中:", miss[:15])

    p.apply(table, use_holes=not args.no_holes)
    p.save(args.out)

    print(f"原地替换 {p.inplace} / 空洞装箱 {p.newseg} / 跳过 {len(p.skipped)}")
    for en, zh, why in p.skipped:
        print(f"  skip {en!r} ({why})")

    out_size = os.path.getsize(args.out)
    print(f"字节数 {base_size} -> {out_size} {'一致 ✅' if base_size == out_size else '不一致 ❌'}")

    texts = set(e["text"] for e in MachO(args.out).cstrings() if e["text"])
    zh = set(table.values())
    hit = sum(1 for v in zh if v in texts)
    print(f"回读 {hit}/{len(zh)} 条译文在位")
    # 给安装脚本读的机器可解析行，别改格式
    print(f"SUMMARY miss={len(miss)} skip={len(p.skipped)} size_ok={int(base_size == out_size)}")
    print("md5:", hashlib.md5(open(args.out, "rb").read()).hexdigest())


if __name__ == "__main__":
    main()

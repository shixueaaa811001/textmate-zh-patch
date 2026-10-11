# -*- coding: utf-8 -*-
"""把英文 nib 按译文表就地翻译成中文 nib。

运行时从用户已装的 English.lproj 读取官方英文源，套上 zh_nib.ZH_NIB_BY_NIB
里的对照，写出到 zh-Hans.lproj。不打包任何成品 nib，也不含 TextMate 的 UI 结构——
仓库里只有「英文→中文」这张表。

用法:
  python3 nib_patch.py --src English.lproj/MainMenu.nib \
                       --out zh-Hans.lproj/MainMenu.nib --nib MainMenu
"""
import argparse, os, plistlib, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zh_nib import ZH_NIB_BY_NIB


def patch(src, out, nib_name, table=None):
    d = plistlib.load(open(src, "rb"))
    objs = d["$objects"]
    table = table if table is not None else ZH_NIB_BY_NIB.get(nib_name, {})
    hits = 0
    for i, o in enumerate(objs):
        if isinstance(o, str) and o in table:
            objs[i] = table[o]
            hits += 1
    plistlib.dump(d, open(out, "wb"), fmt=plistlib.FMT_BINARY)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--nib", required=True, help="nib 名（对应 ZH_NIB_BY_NIB 的键）")
    args = ap.parse_args()
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    n = patch(args.src, args.out, args.nib)
    print(f"{args.nib}: 应用 {n} 条")


if __name__ == "__main__":
    main()

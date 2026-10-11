#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Patch TextMate's __cfstring table in place.

Two write strategies, chosen per entry by how much room the original has:

  IN-PLACE  the entry's own bytes are reused.
            ascii entry (flags 0x7c8, 1 byte/char): flip flags to 0x7d0 so the
            runtime reads it as UTF-16; the N original bytes then hold N/2 UTF-16
            code units. e.g. "File" (4 bytes) -> "文件" (2 units).
            u16 entry (flags 0x7d0): overwrite with new UTF-16, len must not grow.

  HOLE PACK  for entries too small to hold the translation. Every in-place entry
            leaves a tail hole (its own bytes, no longer read). Those holes are
            collected and the too-long translations are packed into them.

            This keeps the Mach-O structurally identical — no new load command,
            no segment growth. That matters: inserting an LC shifts every section
            offset, and growing __LINKEDIT past EOF collides with where codesign
            puts its signature (both were tried; both broke the signature).

Run with --no-holes to disable the second strategy (such entries stay English).
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from macho import MachO

FLAG_ASCII = 0x7C8
FLAG_U16 = 0x7D0
LC_SEGMENT_64 = 0x19
PAGE = 0x1000


def u16_len(s):
    return len(s.encode("utf-16-le")) // 2


class Patcher:
    def __init__(self, path):
        self.path = path
        self.buf = bytearray(open(path, "rb").read())
        self.m = MachO(path)
        self.entries = self.m.cstrings()
        self.inplace = 0
        self.newseg = 0
        self.skipped = []

    def capacity(self, e):
        """Max UTF-16 code units the entry can hold without moving."""
        return e["length"] // 2 if e["kind"] == "ascii" else e["length"]

    def apply(self, table, use_holes=True):
        by_text = {}
        for e in self.entries:
            if e["text"] is not None:
                by_text.setdefault(e["text"], []).append(e)

        holes = []
        overflow = []
        for en, zh in table.items():
            for e in by_text.get(en, []):
                n = u16_len(zh)
                if e["kind"] not in ("ascii", "u16"):
                    self.skipped.append((en, zh, "外部数据"))
                    continue
                if n > self.capacity(e):
                    overflow.append((e, zh))
                    continue
                free = self._write_inplace(e, zh)
                self.inplace += 1
                if free >= 4:
                    holes.append([e["data_off"] + n * 2, free])

        if overflow and use_holes:
            self._pack_into_holes(overflow, holes)
        elif overflow:
            for e, zh in overflow:
                self.skipped.append((e["text"], zh,
                                     f"容量 {self.capacity(e)} < 需要 {u16_len(zh)}"))
        return self

    def _write_inplace(self, e, zh):
        """Overwrite the entry's own bytes; returns bytes left over at its tail."""
        raw = zh.encode("utf-16-le")
        off = e["data_off"]
        old = e["length"] if e["kind"] == "ascii" else e["length"] * 2
        self.buf[off: off + len(raw)] = raw
        for i in range(off + len(raw), off + old):
            self.buf[i] = 0
        ent = e["off"]
        if e["kind"] == "ascii":
            struct.pack_into("<Q", self.buf, ent + 8, FLAG_U16)
        struct.pack_into("<Q", self.buf, ent + 24, u16_len(zh))
        return old - len(raw)

    def _pack_into_holes(self, overflow, holes):
        """Best-fit pack the too-long translations into the tails freed above."""
        need_total = sum(u16_len(zh) * 2 for _, zh in overflow)
        free_total = sum(h[1] for h in holes)
        print(f"    空洞: {len(holes)} 处共 {free_total} 字节 / 需求 {need_total} 字节")

        # largest first, so the awkward ones get placed while holes are big
        for e, zh in sorted(overflow, key=lambda x: -u16_len(x[1])):
            size = u16_len(zh) * 2
            best = None
            for h in holes:
                start = h[0] if h[0] % 2 == 0 else h[0] + 1   # keep UTF-16 aligned
                avail = h[1] - (start - h[0])
                if avail >= size and (best is None or avail < best[1]):
                    best = (start, avail)
            if best is None:
                self.skipped.append((e["text"], zh, f"无 {size} 字节空洞"))
                continue
            start = best[0]
            h = next(h for h in holes if h[0] <= start < h[0] + h[1])
            raw = zh.encode("utf-16-le")
            self.buf[start: start + len(raw)] = raw
            ent = e["off"]
            struct.pack_into("<Q", self.buf, ent + 8, FLAG_U16)
            struct.pack_into("<Q", self.buf, ent + 16, self.m.addr_by_off(start))
            struct.pack_into("<Q", self.buf, ent + 24, u16_len(zh))
            used = (start - h[0]) + len(raw)
            h[0] += used
            h[1] -= used
            self.newseg += 1

    def _append_to_linkedit(self, overflow):
        """Grow __LINKEDIT to host the strings that had no room in place.

        Only __LINKEDIT's filesize (and vmsize if needed) is rewritten. Because
        every other byte in the file stays put, no other offset needs adjusting.
        """
        m = self.m
        le = next(s for s in m.segments if s["name"] == "__LINKEDIT")

        payload = bytearray()
        plan = []
        for e, zh in overflow:
            plan.append((e, zh, len(payload)))
            payload += zh.encode("utf-16-le") + b"\x00\x00"
        while len(payload) % 2:
            payload += b"\x00"

        fileoff = len(self.buf)
        delta = fileoff - le["fileoff"]           # same delta for vm and file
        vmaddr = le["vmaddr"] + delta
        need_file = delta + len(payload)
        need_vm = (need_file + PAGE - 1) & ~(PAGE - 1)

        self.buf += payload
        # pad vm tail so the segment stays page-sized
        if le["vmsize"] < need_vm:
            self.buf += b"\x00" * (need_vm - max(le["vmsize"], delta + len(payload)))

        # segment_command_64: +32 = vmsize, +48 = filesize.
        # fileoff is deliberately left alone — it is slice-relative, and writing
        # the normalised (absolute) value back would shift it by slice_off.
        struct.pack_into("<Q", self.buf, le["cmdoff"] + 48, need_file)
        struct.pack_into("<Q", self.buf, le["cmdoff"] + 32, max(le["vmsize"], need_vm))

        for e, zh, rel in plan:
            ent = e["off"]
            struct.pack_into("<Q", self.buf, ent + 8, FLAG_U16)
            struct.pack_into("<Q", self.buf, ent + 16, vmaddr + rel)
            struct.pack_into("<Q", self.buf, ent + 24, u16_len(zh))
            self.newseg += 1

        print(f"    __LINKEDIT 扩展: filesize 0x{le['filesize']:x} -> 0x{need_file:x}, "
              f"新数据 vm=0x{vmaddr:x}  装载 {len(plan)} 条")

    def save(self, out):
        open(out, "wb").write(bytes(self.buf))
        return out


def check(path):
    """只回读不修改：统计译文在位条数，判断该二进制是否已汉化。"""
    from zh_menu import ZH_MENU, ZH_DIALOG_SAFE
    table = dict(ZH_MENU)
    table.update(ZH_DIALOG_SAFE)
    texts = [e["text"] for e in MachO(path).cstrings() if e["text"]]
    zh = set(table.values())
    hit = sum(1 for v in zh if v in set(texts))
    total = len(zh)
    ratio = hit / total
    if ratio >= 0.9:
        print(f"状态: 已汉化")
    elif hit == 0:
        print(f"状态: 未汉化（官方原版）")
    else:
        print(f"状态: 部分汉化")
    print(f"译文在位: {hit} / {total}")
    print(f"二进制: {path}")
    return hit, total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", default="/Applications/TextMate.app/Contents/MacOS/TextMate")
    ap.add_argument("--out")
    ap.add_argument("--no-holes", action="store_true")
    ap.add_argument("--with-dialog", action="store_true",
                    help="额外应用 ZH_DIALOG_SAFE（对话框/按钮，剔除面板 identifier）")
    ap.add_argument("--check-only", action="store_true",
                    help="只回读校验，不写文件")
    args = ap.parse_args()

    if args.check_only:
        check(args.app)
        return
    if not args.out:
        ap.error("缺少 --out（或用 --check-only 只做校验）")

    from zh_menu import ZH_MENU, ZH_DIALOG_SAFE
    table = dict(ZH_MENU)
    if args.with_dialog:
        table.update(ZH_DIALOG_SAFE)
    p = Patcher(args.app)
    ents = [e for e in p.entries if e["kind"] in ("ascii", "u16")]
    print(f"可改写 CFString 条目: {len(ents)}")

    miss = [k for k in table if k not in {e["text"] for e in ents}]
    if miss:
        print(f"翻译表中未命中 {len(miss)} 条: {miss[:12]}")

    p.apply(table, use_holes=not args.no_holes)
    p.save(args.out)
    print(f"\n原地替换: {p.inplace} 条")
    print(f"新段装载: {p.newseg} 条")
    print(f"跳过    : {len(p.skipped)} 条")
    for en, zh, why in p.skipped[:15]:
        print(f"   {en:<30} -> {zh:<14} ({why})")
    print(f"\n输出: {args.out}")


if __name__ == "__main__":
    main()

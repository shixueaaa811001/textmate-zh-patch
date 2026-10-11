"""Minimal Mach-O reader for TextMate arm64.
Locates __cfstring entries and resolves each one's backing bytes by address range
(more reliable than guessing CF flags semantics).
"""
import struct

FAT_MAGIC = 0xCAFEBABE
FAT_MAGIC_64 = 0xCAFEBABF
MH_MAGIC_64 = 0xFEEDFACF
LC_SEGMENT_64 = 0x19


class MachO:
    def __init__(self, path):
        self.data = open(path, "rb").read()
        d = self.data
        (magic,) = struct.unpack_from(">I", d, 0)

        if magic in (FAT_MAGIC, FAT_MAGIC_64):
            (narch,) = struct.unpack_from(">I", d, 4)
            for i in range(narch):
                if magic == FAT_MAGIC_64:
                    ct, cs, off, size, align = struct.unpack_from(">iiQQI", d, 8 + i * 32)
                else:
                    ct, cs, off, size, align = struct.unpack_from(">iiIII", d, 8 + i * 20)
                if ct == 0x0100000C:  # CPU_TYPE_ARM64
                    self.slice_off = off
                    break
            else:
                raise ValueError("no arm64 slice")
        else:
            self.slice_off = 0

        base = self.slice_off
        (m,) = struct.unpack_from("<I", d, base)
        assert m == MH_MAGIC_64, f"not MH_MAGIC_64: {hex(m)}"
        self.ncmds, self.sizeofcmds = struct.unpack_from("<II", d, base + 16)
        self.hdrsize = 32

        # walk load commands
        self.segments = []
        p = base + self.hdrsize
        for _ in range(self.ncmds):
            cmd, cmdsize = struct.unpack_from("<II", d, p)
            if cmd == LC_SEGMENT_64:
                name = d[p + 8: p + 24].rstrip(b"\x00").decode()
                vmaddr, vmsize, fileoff, filesize = struct.unpack_from("<QQQQ", d, p + 24)
                nsects, = struct.unpack_from("<I", d, p + 64)
                sects = []
                sp = p + 72
                for _ in range(nsects):
                    sname = d[sp: sp + 16].rstrip(b"\x00").decode()
                    segname = d[sp + 16: sp + 32].rstrip(b"\x00").decode()
                    saddr, ssize = struct.unpack_from("<QQ", d, sp + 32)
                    soff, = struct.unpack_from("<I", d, sp + 48)
                    sects.append(dict(name=sname, seg=segname, addr=saddr,
                                      size=ssize, offset=soff))
                    sp += 80
                self.segments.append(dict(name=name, vmaddr=vmaddr, vmsize=vmsize,
                                          fileoff=fileoff, filesize=filesize,
                                          sects=sects, cmdoff=p, cmdsize=cmdsize))
            p += cmdsize

        # normalise: make every file offset absolute within the fat file
        for s in self.segments:
            s["fileoff"] += self.slice_off
            for x in s["sects"]:
                x["offset"] += self.slice_off

    def sect(self, seg, name):
        for s in self.segments:
            if s["name"] == seg:
                for x in s["sects"]:
                    if x["name"] == name:
                        return x
        raise KeyError(f"{seg},{name}")

    def addr2off(self, addr):
        for s in self.segments:
            if s["filesize"] == 0:
                continue
            if s["vmaddr"] <= addr < s["vmaddr"] + s["filesize"]:
                return s["fileoff"] + (addr - s["vmaddr"])
        raise ValueError(f"addr {hex(addr)} not mapped")

    def addr_by_off(self, off):
        for s in self.segments:
            if s["filesize"] == 0:
                continue
            if s["fileoff"] <= off < s["fileoff"] + s["filesize"]:
                return s["vmaddr"] + (off - s["fileoff"])
        raise ValueError(f"offset {hex(off)} not mapped")

    def owner_seg(self, addr):
        for s in self.segments:
            if s["vmaddr"] <= addr < s["vmaddr"] + s["vmsize"]:
                return s
        return None

    def cstrings(self):
        """Yield (index, file_offset, length, text) for every __cfstring entry."""
        sect = self.sect("__DATA", "__cfstring")
        ustr = self.sect("__TEXT", "__ustring")
        cstr = self.sect("__TEXT", "__cstring")
        base = sect["offset"]
        n = sect["size"] // 32
        out = []
        for i in range(n):
            o = base + i * 32
            isa, flags, data_ptr, length = struct.unpack_from("<QQQQ", self.data, o)
            kind = None
            off = None
            # bit4 of flags selects UTF-16 storage; this is authoritative, since a
            # patched entry keeps its old (ascii-segment) address but new encoding.
            is_u16 = bool(flags & 0x10)
            try:
                off = self.addr2off(data_ptr)
                if is_u16:
                    kind = "u16"
                    raw = self.data[off: off + length * 2]
                    text = raw.decode("utf-16-le", "replace")
                else:
                    kind = "ascii"
                    raw = self.data[off: off + length]
                    text = raw.decode("utf-8", "replace")
            except Exception:
                kind, off, text = "err", None, None
            out.append(dict(idx=i, off=o, data_ptr=data_ptr, length=length,
                            kind=kind, data_off=off, text=text, flags=flags))
        return out

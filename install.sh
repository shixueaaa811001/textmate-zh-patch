#!/bin/bash
# TextMate 汉化补丁（零资源版）—— 安装
# 全部资源在运行时从你已装的 TextMate 自己生成：
#   · 菜单/对话框/偏好设置正文/面板标题 → 改二进制 CFString 表
#   · 13 个 nib → 用译文表套在官方英文 nib 上现场生成
#   · 面板图标 → 从 Projects.png 等复制重命名
# 本仓库不含任何 TextMate 的二进制/资源文件。
#
# 用法: install.sh [--app /Applications/TextMate.app] [--yes]
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="/Applications/TextMate.app"
ASSUME_YES=0
while [ $# -gt 0 ]; do
	case "$1" in
		--app) APP="$2"; shift 2 ;;
		--yes|-y) ASSUME_YES=1; shift ;;
		*) echo "未知参数: $1"; exit 2 ;;
	esac
done

BIN="$APP/Contents/MacOS/TextMate"
RES="$APP/Contents/Resources"
EXPECT_VER="2.0.23"
EXPECT_BUILD="9800"
MAX_MISS=5

# 13 个需要本地化的 nib（与 tools/zh_nib.py 的键一致）
NIBS=(BundleProperties CommandProperties CustomizeEncodings FileDropProperties
      GrammarProperties MacroProperties MainMenu "Pasteboard Selector"
      SharedProperties SnippetProperties TabSizeSetting TerminalPreferences ThemeProperties)
# 面板图标：英文源名 -> 中文目标名
ICONS=(Projects:项目 Variables:变量 "Software Update:软件更新" Terminal:终端)

say()  { printf '%s\n' "$*"; }
die()  { printf '❌ %s\n' "$*" >&2; exit 1; }
ok()   { printf '✅ %s\n' "$*"; }

# ---------- 0. 找 python3 ----------
PY=""
for c in /usr/bin/python3 "$(command -v python3 2>/dev/null)" \
         "$HOME/.workbuddy-ai/binaries/python/versions/3.13.12/bin/python3"; do
	[ -n "$c" ] && [ -x "$c" ] || continue
	"$c" -c 'import sys,plistlib; sys.exit(0 if sys.version_info>=(3,6) else 1)' 2>/dev/null || continue
	PY="$c"; break
done
[ -n "$PY" ] || die "找不到可用的 python3（需要 3.6+）。装一下 Xcode 命令行工具: xcode-select --install"
say "python3: $PY ($("$PY" -V 2>&1))"

# ---------- 1. 环境检查 ----------
say ""
say "=============== TextMate 汉化补丁（零资源版） ==============="
[ -d "$APP" ] || die "找不到 $APP"
[ -f "$BIN" ] || die "找不到可执行文件 $BIN"
[ -d "$RES/English.lproj" ] || die "找不到 $RES/English.lproj（无法在现场生成中文 nib）"

ver=$(/usr/libexec/PlistBuddy -c "Print :CFBundleShortVersionString" "$APP/Contents/Info.plist" 2>/dev/null)
bld=$(/usr/libexec/PlistBuddy -c "Print :CFBundleVersion" "$APP/Contents/Info.plist" 2>/dev/null)
say "目标: $APP"
say "版本: $ver ($bld)"

if [ "$ver" != "$EXPECT_VER" ] || [ "$bld" != "$EXPECT_BUILD" ]; then
	say ""
	say "⚠️  这个补丁是给 TextMate $EXPECT_VER ($EXPECT_BUILD) 做的，你的是 $ver ($bld)。"
	say "    译文按精确字符串匹配，对不上的会被跳过（不改错东西）。"
	say "    未命中超过 $MAX_MISS 条则中止。"
	if [ "$ASSUME_YES" != "1" ]; then
		read -r -p "    继续？(y/N) " a
		[ "$a" = "y" ] || [ "$a" = "Y" ] || exit 1
	fi
fi

if [ -d "$RES/zh-Hans.lproj" ]; then
	say ""
	say "⚠️  检测到已经汉化过（$RES/zh-Hans.lproj 已存在）。"
	say "    请先跑「还原官方英文版.command」/ uninstall.sh，再重新安装。"
	exit 1
fi

# ---------- 2. 可写性 ----------
SUDO=""
if [ ! -w "$BIN" ] || [ ! -w "$RES" ]; then
	say "→ 目标目录不可写，需要管理员密码"
	SUDO="sudo"
	$SUDO -v || die "获取管理员权限失败"
fi
run() { if [ -n "$SUDO" ]; then $SUDO "$@"; else "$@"; fi; }

# ---------- 3. 备份（只备份会被改的二进制）----------
STAMP="$(date +%Y%m%d-%H%M%S)"
BAK="$HOME/Library/Application Support/TextMate-汉化/backup/$STAMP"
mkdir -p "$BAK"
cp "$BIN" "$BAK/TextMate.bin"
say "→ 备份二进制到 $BAK"

# ---------- 4. 退出 TextMate ----------
say "→ 退出正在运行的 TextMate"
pkill -x TextMate 2>/dev/null && sleep 2
pgrep -x TextMate >/dev/null && { pkill -9 -x TextMate; sleep 1; }

# ---------- 5. 打二进制补丁 ----------
say "→ 打二进制补丁（菜单 + 对话框 + 偏好设置正文 + 面板标题）"
OUT="$(mktemp -t tm_zh)"
"$PY" "$HERE/tools/patch_all.py" --base "$BIN" --out "$OUT" > "$BAK/patch.log" 2>&1
sed 's/^/    /' "$BAK/patch.log"
miss=$(sed -n 's/^SUMMARY miss=\([0-9]*\).*/\1/p' "$BAK/patch.log" | tail -1)
skip=$(sed -n 's/^SUMMARY .*skip=\([0-9]*\).*/\1/p' "$BAK/patch.log" | tail -1)
sizeok=$(sed -n 's/^SUMMARY .*size_ok=\([0-9]*\).*/\1/p' "$BAK/patch.log" | tail -1)
miss=${miss:-999}; skip=${skip:-999}; sizeok=${sizeok:-0}
if [ "$miss" -gt "$MAX_MISS" ] || [ "$skip" -gt "$MAX_MISS" ]; then
	rm -f "$OUT"
	die "未命中 $miss 条 / 跳过 $skip 条，超过阈值 $MAX_MISS —— 判定版本不匹配，已中止，未改动程序"
fi
if [ "$sizeok" != "1" ]; then
	rm -f "$OUT"
	die "补丁后字节数与原版不一致 —— Mach-O 结构被破坏，已中止，未改动程序"
fi
run cp "$OUT" "$BIN"
run chmod 755 "$BIN"
rm -f "$OUT"

# ---------- 6. 现场生成 zh-Hans.lproj（从官方英文 nib 套译文表）----------
say "→ 现场生成中文语言包（13 个 nib，从 English.lproj 套表）"
run mkdir -p "$RES/zh-Hans.lproj"
for n in "${NIBS[@]}"; do
	src="$RES/English.lproj/$n.nib"
	[ -f "$src" ] || { say "    ⚠️  跳过缺失源 nib: $n"; continue; }
	"$PY" "$HERE/tools/nib_patch.py" --src "$src" --out "$RES/zh-Hans.lproj/$n.nib" --nib "$n" | sed 's/^/    /'
done

# ---------- 7. 面板图标（从 Projects.png 等复制重命名）----------
say "→ 生成中文名面板图标"
for pair in "${ICONS[@]}"; do
	en="${pair%%:*}"; zh="${pair##*:}"
	[ -f "$RES/$en.png" ] && run cp "$RES/$en.png" "$RES/$zh.png"
	[ -f "$RES/$en@2x.png" ] && run cp "$RES/$en@2x.png" "$RES/$zh@2x.png"
done

# ---------- 8. 清掉记忆的面板标识 ----------
say "→ 清除记忆的偏好面板标识（否则偏好设置窗口会塌成 1×80 打不开）"
defaults delete com.macromates.TextMate "MASPreferences Selected Identifier View" 2>/dev/null && \
	say "  已清除" || say "  （本来就没有，跳过）"

# ---------- 9. 重签名 ----------
say "→ 重新签名（ad-hoc）"
run codesign --force --sign - --timestamp=none "$APP" >/dev/null 2>&1
if ! codesign -v "$APP" 2>/dev/null; then
	die "签名校验失败，已中止。请用「还原官方英文版.command」恢复。"
fi
ok "签名有效"
run xattr -dr com.apple.quarantine "$APP" 2>/dev/null || true

# ---------- 10. 启动验证 ----------
say "→ 启动验证（8 秒）"
BEFORE=$(ls ~/Library/Logs/DiagnosticReports 2>/dev/null | grep -c '^TextMate-' || true)
open "$APP"
sleep 8
ALIVE=0
pgrep -x TextMate >/dev/null && ALIVE=1
AFTER=$(ls ~/Library/Logs/DiagnosticReports 2>/dev/null | grep -c '^TextMate-' || true)
if [ "$ALIVE" != "1" ] || [ "$AFTER" -gt "$BEFORE" ]; then
	say ""
	say "❌ 启动验证失败（存活=$ALIVE，新崩溃报告 $((AFTER-BEFORE)) 份）—— 自动回滚"
	pkill -x TextMate 2>/dev/null
	run cp "$BAK/TextMate.bin" "$BIN"
	run rm -rf "$RES/zh-Hans.lproj"
	for pair in "${ICONS[@]}"; do
		zh="${pair##*:}"
		run rm -f "$RES/$zh.png" "$RES/$zh@2x.png"
	done
	run codesign --force --sign - --timestamp=none "$APP" >/dev/null 2>&1
	die "已回滚到安装前状态。日志: $BAK/patch.log"
fi
ok "启动正常，无新崩溃报告"

# ---------- 11. 回读校验 ----------
say "→ 回读校验"
"$PY" "$HERE/check.py" --app "$APP" | sed 's/^/    /'

say ""
say "============================================================"
ok "汉化完成"
say "  备份: $BAK"
say "  还原: 双击「还原官方英文版.command」，或跑 ./uninstall.sh"
say "  现在打开 TextMate，菜单栏和偏好设置应该都是中文了。"

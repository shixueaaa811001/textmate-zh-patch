#!/bin/bash
# TextMate 汉化补丁（零资源版）—— 还原官方英文版
# 用法: uninstall.sh [--app /Applications/TextMate.app] [--from <备份目录>]
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP="/Applications/TextMate.app"
FROM=""
while [ $# -gt 0 ]; do
	case "$1" in
		--app) APP="$2"; shift 2 ;;
		--from) FROM="$2"; shift 2 ;;
		*) echo "未知参数: $1"; exit 2 ;;
	esac
done

BIN="$APP/Contents/MacOS/TextMate"
RES="$APP/Contents/Resources"
ROOT="$HOME/Library/Application Support/TextMate-汉化/backup"
ICONS=(项目 变量 软件更新 终端)

say() { printf '%s\n' "$*"; }
die() { printf '❌ %s\n' "$*" >&2; exit 1; }

[ -d "$APP" ] || die "找不到 $APP"

if [ -z "$FROM" ]; then
	FROM=$(ls -1d "$ROOT"/*/ 2>/dev/null | sort | tail -1)
	FROM="${FROM%/}"
fi

if [ -z "$FROM" ] || [ ! -f "$FROM/TextMate.bin" ]; then
	say "❌ 找不到可用备份（$ROOT）。"
	say "   没有备份时无法自动还原二进制 —— 请去 https://macromates.com 重新下载"
	say "   TextMate $ver 覆盖安装，然后手动删掉:"
	say "     $RES/zh-Hans.lproj"
	say "     $RES/{项目,变量,软件更新,终端}.png 及各自的 @2x"
	exit 1
fi
say "→ 备份来源: $FROM"

SUDO=""
if [ ! -w "$BIN" ] || [ ! -w "$RES" ]; then
	SUDO="sudo"; sudo -v || die "获取管理员权限失败"
fi
run() { if [ -n "$SUDO" ]; then $SUDO "$@"; else "$@"; fi; }

say "→ 退出 TextMate"
pkill -x TextMate 2>/dev/null && sleep 2
pgrep -x TextMate >/dev/null && { pkill -9 -x TextMate; sleep 1; }

say "→ 还原二进制"
run cp "$FROM/TextMate.bin" "$BIN"
run chmod 755 "$BIN"

say "→ 移除中文语言包与面板图标"
run rm -rf "$RES/zh-Hans.lproj"
for f in "${ICONS[@]}"; do
	run rm -f "$RES/$f.png" "$RES/$f@2x.png"
done

say "→ 清除面板记忆键"
defaults delete com.macromates.TextMate "MASPreferences Selected Identifier View" 2>/dev/null || true

say "→ 重新签名"
run codesign --force --sign - --timestamp=none "$APP" >/dev/null 2>&1
codesign -v "$APP" 2>/dev/null && say "✅ 签名有效" || die "签名校验失败"

say ""
say "✅ 已还原为官方英文版。"

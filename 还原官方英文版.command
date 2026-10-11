#!/bin/bash
cd "$(dirname "$0")"
clear
echo "══════════════════════════════════════════════"
echo "  TextMate 汉化补丁（零资源版）— 还原"
echo "  把 TextMate 恢复为官方英文原版"
echo "══════════════════════════════════════════════"
echo
echo "正在还原，请稍候……（期间会自动退出 TextMate）"
echo
./uninstall.sh
echo
read -p "还原结束，按回车关闭此窗口…"

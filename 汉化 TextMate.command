#!/bin/bash
cd "$(dirname "$0")"
clear
echo "══════════════════════════════════════════════"
echo "  TextMate 汉化补丁（零资源版）"
echo "  把菜单 / 对话框 / 偏好设置汉化为中文"
echo "══════════════════════════════════════════════"
echo
echo "正在安装，请稍候……（约 10 秒，期间会自动退出 TextMate）"
echo
./install.sh --yes
echo
read -p "安装结束，按回车关闭此窗口…"

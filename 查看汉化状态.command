#!/bin/bash
cd "$(dirname "$0")"
clear
echo "══════════════════════════════════════════════"
echo "  TextMate 汉化补丁（零资源版）— 状态"
echo "  查看当前汉化情况"
echo "══════════════════════════════════════════════"
echo
python3 check.py
echo
read -p "按回车关闭此窗口…"

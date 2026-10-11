#!/bin/bash
cd "$(dirname "$0")"
python3 check.py
echo
read -p "按回车关闭窗口…"

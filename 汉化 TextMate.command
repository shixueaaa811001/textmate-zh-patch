#!/bin/bash
cd "$(dirname "$0")"
./install.sh --yes
echo
read -p "按回车关闭窗口…"

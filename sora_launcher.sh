#!/bin/bash

# Sora批量出图工具 - macOS启动脚本
echo "========================================"
echo "    Sora批量出图工具 - 优化版界面"
echo "========================================"
echo ""
echo "✨ 特性："
echo "• 统一设置管理中心"
echo "• 简洁主界面设计"
echo "• 三合一弹窗管理（配置+风格库+参考图）"
echo ""
echo "正在启动优化版界面..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3，请先安装 Python"
    echo "建议使用 Homebrew 安装：brew install python"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "📦 安装依赖包..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    # 激活虚拟环境
    source venv/bin/activate
fi

# 启动应用
python main.py
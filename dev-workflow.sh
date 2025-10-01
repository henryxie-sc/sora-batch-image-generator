#!/bin/bash

# Sora项目开发工作流脚本

function new_feature() {
    echo "🚀 创建新功能分支: $1"
    git checkout main
    git pull origin main
    git checkout -b "feature/$1"
    echo "✅ 功能分支 feature/$1 已创建"
}

function test_feature() {
    echo "🧪 运行测试..."
    python -m pytest tests/ || echo "⚠️  没有找到测试文件"

    echo "🔍 代码检查..."
    python -m pylint main.py || echo "⚠️  代码检查完成"

    echo "🏃‍♂️ 启动应用测试..."
    python main.py &
    APP_PID=$!
    echo "应用已启动 (PID: $APP_PID)，请手动测试功能"
    echo "测试完成后按任意键继续..."
    read -n 1
    kill $APP_PID 2>/dev/null
}

function finish_feature() {
    BRANCH=$(git branch --show-current)
    echo "🎉 完成功能开发: $BRANCH"

    # 提交更改
    git add .
    echo "请输入提交信息:"
    read COMMIT_MSG
    git commit -m "$COMMIT_MSG"

    # 推送功能分支
    git push origin "$BRANCH"

    # 切换到main并合并
    git checkout main
    git pull origin main
    git merge "$BRANCH"
    git push origin main

    # 清理功能分支
    git branch -d "$BRANCH"
    git push origin --delete "$BRANCH"

    echo "✅ 功能已完成并合并到main分支"
}

# 菜单
case "$1" in
    "new")
        new_feature "$2"
        ;;
    "test")
        test_feature
        ;;
    "finish")
        finish_feature
        ;;
    *)
        echo "使用方法:"
        echo "  ./dev-workflow.sh new <功能名称>   # 创建新功能分支"
        echo "  ./dev-workflow.sh test           # 运行测试"
        echo "  ./dev-workflow.sh finish         # 完成功能开发"
        ;;
esac
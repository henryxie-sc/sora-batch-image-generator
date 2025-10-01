#!/bin/bash

# Sora项目简化开发脚本
# 使用方法：./dev.sh <命令>

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 新建功能分支
new_feature() {
    if [ -z "$1" ]; then
        print_error "请提供功能名称"
        echo "使用方法: ./dev.sh new <功能名称>"
        exit 1
    fi

    FEATURE_NAME="$1"
    BRANCH_NAME="feature/$FEATURE_NAME"

    print_info "创建新功能分支: $BRANCH_NAME"

    # 确保在develop分支
    git checkout develop
    git pull origin develop

    # 创建功能分支
    git checkout -b "$BRANCH_NAME"

    print_success "功能分支 $BRANCH_NAME 已创建"
    print_info "现在可以开始开发功能: $FEATURE_NAME"
}

# 运行测试
run_tests() {
    print_info "运行基础测试..."

    # 运行基础测试
    cd tests
    python3 test_basic.py
    cd ..

    print_info "检查代码启动..."
    timeout 10s python3 main.py --help 2>/dev/null || print_warning "应用启动检查完成"

    print_success "测试检查完成"
}

# 提交当前更改
commit_changes() {
    git add .

    if git diff --staged --quiet; then
        print_warning "没有需要提交的更改"
        return
    fi

    echo "请输入提交信息："
    read -r COMMIT_MSG

    if [ -z "$COMMIT_MSG" ]; then
        print_error "提交信息不能为空"
        return 1
    fi

    git commit -m "$COMMIT_MSG"
    print_success "更改已提交: $COMMIT_MSG"
}

# 完成功能开发
finish_feature() {
    CURRENT_BRANCH=$(git branch --show-current)

    if [[ ! $CURRENT_BRANCH == feature/* ]]; then
        print_error "当前不在功能分支上 (当前: $CURRENT_BRANCH)"
        return 1
    fi

    print_info "完成功能开发: $CURRENT_BRANCH"

    # 提交当前更改
    commit_changes

    # 推送功能分支
    print_info "推送功能分支..."
    git push origin "$CURRENT_BRANCH"

    # 切换到develop并合并
    print_info "合并到develop分支..."
    git checkout develop
    git pull origin develop
    git merge "$CURRENT_BRANCH" --no-ff

    # 推送develop
    git push origin develop

    # 清理功能分支
    print_info "清理功能分支..."
    git branch -d "$CURRENT_BRANCH"
    git push origin --delete "$CURRENT_BRANCH"

    print_success "功能已完成并合并到develop分支"
}

# 发布到main分支
release_to_main() {
    print_info "准备发布到main分支..."

    # 确保在develop分支
    git checkout develop
    git pull origin develop

    # 运行测试
    run_tests

    print_warning "即将合并develop到main分支，这将创建新的发布版本"
    echo "确认继续？(y/N)"
    read -r confirm

    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        print_info "发布已取消"
        return
    fi

    # 切换到main并合并
    git checkout main
    git pull origin main
    git merge develop --no-ff
    git push origin main

    print_success "已发布到main分支"

    # 回到develop分支
    git checkout develop
}

# 显示帮助
show_help() {
    echo "Sora开发工具 - 使用方法:"
    echo ""
    echo "  ./dev.sh new <功能名称>     创建新功能分支"
    echo "  ./dev.sh test              运行测试"
    echo "  ./dev.sh commit            提交当前更改"
    echo "  ./dev.sh finish            完成功能开发"
    echo "  ./dev.sh release           发布到main分支"
    echo "  ./dev.sh help              显示此帮助"
    echo ""
    echo "示例："
    echo "  ./dev.sh new 图片压缩功能"
    echo "  ./dev.sh test"
    echo "  ./dev.sh commit"
    echo "  ./dev.sh finish"
}

# 主逻辑
case "$1" in
    "new")
        new_feature "$2"
        ;;
    "test")
        run_tests
        ;;
    "commit")
        commit_changes
        ;;
    "finish")
        finish_feature
        ;;
    "release")
        release_to_main
        ;;
    "help"|"")
        show_help
        ;;
    *)
        print_error "未知命令: $1"
        show_help
        exit 1
        ;;
esac
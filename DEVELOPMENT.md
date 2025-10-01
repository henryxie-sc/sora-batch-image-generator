# 🚀 Sora项目开发指南

## 📋 开发流程

### 🌟 新功能开发流程

```bash
# 1. 创建新功能分支
./dev.sh new "功能名称"

# 2. 开发过程中提交更改
git add .
git commit -m "feat: 添加xxx功能"

# 3. 测试功能
./dev.sh test

# 4. 完成功能开发
./dev.sh finish
```

### 🔧 快速命令

| 命令 | 说明 |
|------|------|
| `./dev.sh new <功能名称>` | 创建新功能分支 |
| `./dev.sh test` | 运行测试检查 |
| `./dev.sh commit` | 交互式提交更改 |
| `./dev.sh finish` | 完成功能开发并合并 |
| `./dev.sh release` | 发布到main分支 |

### 📁 分支说明

- **main** - 稳定发布版本
- **develop** - 开发主分支
- **feature/功能名** - 功能开发分支

### 💡 提交信息规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构代码
test: 测试相关
chore: 构建/工具相关
```

### 🧪 测试说明

运行 `./dev.sh test` 会检查：
- 模块导入是否正常
- 基础功能是否可用
- 应用启动是否正常

## 🔄 完整开发示例

```bash
# 开始新功能
./dev.sh new "图片压缩"

# 开发中...
git add .
git commit -m "feat: 添加图片压缩基础功能"

# 继续开发...
git add .
git commit -m "feat: 完善图片压缩界面"

# 测试功能
./dev.sh test

# 完成开发
./dev.sh finish

# 发布到生产环境
./dev.sh release
```

## 🛠️ 开发环境设置

### 安装开发依赖
```bash
pip install -r requirements-dev.txt
```

### 代码格式化
```bash
black main.py services/
```

### 代码质量检查
```bash
pylint main.py services/
```

## 📞 问题反馈

如果遇到问题：
1. 检查当前分支：`git branch`
2. 查看状态：`git status`
3. 运行测试：`./dev.sh test`
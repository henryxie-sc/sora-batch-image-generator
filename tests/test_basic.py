"""
Sora批量出图工具 - 基础测试
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import_main():
    """测试主模块能否正常导入"""
    try:
        import main
        assert True
    except ImportError as e:
        assert False, f"主模块导入失败: {e}"

def test_services_import():
    """测试服务模块能否正常导入"""
    try:
        from services import pathing, images, history
        assert True
    except ImportError as e:
        assert False, f"服务模块导入失败: {e}"

def test_app_path_exists():
    """测试应用路径是否存在"""
    from services.pathing import APP_PATH
    assert APP_PATH.exists(), "应用路径不存在"

if __name__ == "__main__":
    test_import_main()
    test_services_import()
    test_app_path_exists()
    print("✅ 所有基础测试通过")
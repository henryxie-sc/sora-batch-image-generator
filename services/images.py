import base64
import logging
import shutil
from pathlib import Path

from .pathing import IMAGES_PATH


def ensure_images_directory() -> None:
    if not IMAGES_PATH.exists():
        IMAGES_PATH.mkdir(parents=True, exist_ok=True)
        logging.info(f"创建图片目录: {IMAGES_PATH}")


def create_category_directory(category_name: str) -> Path:
    ensure_images_directory()
    category_path = IMAGES_PATH / category_name
    if not category_path.exists():
        category_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"创建分类目录: {category_path}")
    return category_path


def rename_category_directory(old_name: str, new_name: str) -> None:
    ensure_images_directory()
    old_path = IMAGES_PATH / old_name
    new_path = IMAGES_PATH / new_name
    if old_path.exists() and not new_path.exists():
        old_path.rename(new_path)
        logging.info(f"重命名分类目录: {old_path} -> {new_path}")
    elif not old_path.exists():
        create_category_directory(new_name)


def delete_category_directory(category_name: str) -> None:
    ensure_images_directory()
    category_path = IMAGES_PATH / category_name
    if category_path.exists():
        shutil.rmtree(category_path)
        logging.info(f"删除分类目录: {category_path}")


def copy_image_to_category(source_path: str | Path, category_name: str, image_name: str) -> str:
    category_path = create_category_directory(category_name)

    source_path = Path(source_path)
    source_ext = source_path.suffix or ".png"

    target_filename = f"{image_name}{source_ext}"
    target_path = category_path / target_filename

    shutil.copy2(source_path, target_path)
    logging.info(f"复制图片: {source_path} -> {target_path}")

    return f"images/{category_name}/{target_filename}"


def image_to_base64(image_path: str | Path) -> str | None:
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode("utf-8")
            ext = Path(image_path).suffix.lower()
            if ext in [".jpg", ".jpeg"]:
                mime_type = "image/jpeg"
            elif ext == ".png":
                mime_type = "image/png"
            elif ext == ".gif":
                mime_type = "image/gif"
            elif ext == ".webp":
                mime_type = "image/webp"
            else:
                mime_type = "image/png"
            return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        logging.error(f"转换图片为base64失败: {e}")
        return None


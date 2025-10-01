import json
import logging
import time
from pathlib import Path


def ensure_history_directory(app_path: Path) -> Path:
    history_path = app_path / "history"
    if not history_path.exists():
        history_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"创建历史记录目录: {history_path}")
    return history_path


def save_history_record(prompt_data, config_data: dict, app_path: Path, filename: str | None = None) -> str | None:
    import hashlib
    import glob

    try:
        history_path = ensure_history_directory(app_path)

        history_record = {
            "version": "3.4",
            "created_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_prompts": len(prompt_data),
            "success_count": len([p for p in prompt_data if p.get("status") == "成功"]),
            "failed_count": len([p for p in prompt_data if p.get("status") == "失败"]),
            "config": {
                "api_platform": config_data.get("api_platform", ""),
                "model_type": config_data.get("model_type", ""),
                "thread_count": config_data.get("thread_count", 5),
                "retry_count": config_data.get("retry_count", 3),
                "image_ratio": config_data.get("image_ratio", "3:2"),
                "current_style": config_data.get("current_style", ""),
                "custom_style_content": config_data.get("custom_style_content", ""),
            },
            "prompts": prompt_data,
        }

        content_for_hash = {
            "config": history_record["config"],
            "prompts": [{"prompt": p.get("prompt", "")} for p in prompt_data],
        }
        content_str = json.dumps(content_for_hash, sort_keys=True, ensure_ascii=False)
        content_hash = hashlib.md5(content_str.encode("utf-8")).hexdigest()

        existing_files = glob.glob(str(history_path / "sora_history_*.json"))
        duplicate_file = None

        for existing_file in existing_files:
            try:
                with open(existing_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                existing_content = {
                    "config": existing_data.get("config", {}),
                    "prompts": [
                        {"prompt": p.get("prompt", "")} for p in existing_data.get("prompts", [])
                    ],
                }
                existing_str = json.dumps(existing_content, sort_keys=True, ensure_ascii=False)
                existing_hash = hashlib.md5(existing_str.encode("utf-8")).hexdigest()
                if existing_hash == content_hash:
                    duplicate_file = existing_file
                    break
            except (json.JSONDecodeError, IOError, KeyError):
                continue

        if duplicate_file:
            logging.info(f"发现重复内容，更新现有文件: {duplicate_file}")
            try:
                with open(duplicate_file, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                existing_data["created_time"] = history_record["created_time"]
                existing_data["total_prompts"] = history_record["total_prompts"]
                existing_data["success_count"] = history_record["success_count"]
                existing_data["failed_count"] = history_record["failed_count"]
                existing_data["prompts"] = prompt_data
                with open(duplicate_file, "w", encoding="utf-8") as f:
                    json.dump(existing_data, f, indent=2, ensure_ascii=False)
                logging.info(f"历史记录已更新: {duplicate_file}")
                return str(duplicate_file)
            except Exception as e:
                logging.error(f"更新重复文件失败: {e}")

        if not filename:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"sora_history_{timestamp}.json"
        if not filename.endswith(".json"):
            filename += ".json"

        file_path = history_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history_record, f, indent=2, ensure_ascii=False)
        logging.info(f"历史记录已保存: {file_path}")
        return str(file_path)
    except Exception as e:
        logging.error(f"保存历史记录失败: {e}")
        return None


def load_history_record(file_path: str | Path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            history_record = json.load(f)
        logging.info(f"历史记录已加载: {file_path}")
        return history_record
    except Exception as e:
        logging.error(f"加载历史记录失败: {e}")
        return None


def get_history_files(app_path: Path):
    try:
        history_path = ensure_history_directory(app_path)
        history_files = []
        for file_path in history_path.glob("*.json"):
            try:
                stat = file_path.stat()
                file_info = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": stat.st_size,
                    "modified_time": time.strftime(
                        "%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime)
                    ),
                }
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    file_info.update(
                        {
                            "created_time": data.get("created_time", file_info["modified_time"]),
                            "version": data.get("version", "未知"),
                            "total_prompts": data.get("total_prompts", 0),
                            "success_count": data.get("success_count", 0),
                            "failed_count": data.get("failed_count", 0),
                        }
                    )
                history_files.append(file_info)
            except Exception as e:
                logging.warning(f"读取历史文件失败: {file_path}, 错误: {e}")
                continue
        history_files.sort(key=lambda x: x["modified_time"], reverse=True)
        return history_files
    except Exception as e:
        logging.error(f"获取历史文件列表失败: {e}")
        return []


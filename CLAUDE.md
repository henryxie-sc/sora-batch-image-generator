# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Chinese GUI application built with PyQt6 for batch AI image generation using various API platforms (云雾AI, API易, apicore). The tool allows users to generate multiple AI images from text prompts with reference images and style templates.

## Key Components

### Main Architecture
- `main.py`: Single-file PyQt6 application containing all GUI components and core logic
- `config.json`: Stores all configuration including API keys, settings, styles, and reference images
- `images/`: Directory for storing reference images organized by categories
- `requirements.txt`: Python dependencies
- Virtual environment setup with activation scripts

### Core Classes (main.py)
- `AsyncWorker`: Handles async API calls to different platforms
- `SettingsDialog`: Centralized settings management (API keys, styles, reference images)
- `MainWindow`: Primary GUI with prompt table and generation controls
- `WorkerSignals`: Qt signal system for async operations
- Supporting dialogs: `KeyEditDialog`, `PromptEditDialog`, `ImageViewDialog`

## Development Commands

### Running the Application

**macOS/Linux:**
```bash
./sora_launcher.sh
```

**Windows:**
```bash
sora批量出图启动.bat
```

**Manual Python:**
```bash
# Create virtual environment if it doesn't exist
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Dependencies Management
The application requires these key packages:
- PyQt6: GUI framework
- aiohttp: Async HTTP requests to API platforms
- pandas: CSV file handling for batch imports
- requests, aiofiles: Additional HTTP and file operations

### Configuration System
- All settings persist in `config.json`
- Reference images stored in `images/[category]/` structure
- Style templates and API keys managed through GUI
- Window geometry and user preferences auto-saved

## API Integration Architecture

### Supported Platforms
The app integrates with three AI image generation APIs:
1. **云雾 (Yunwu)**: Primary platform with specific endpoint format
2. **API易 (APIYi)**: Alternative platform with different request structure
3. **apicore**: Third platform option

### Async Request Handling
- Uses `AsyncWorker` class with aiohttp for concurrent API requests
- Semaphore-controlled concurrency (configurable thread count)
- Automatic retry mechanism for failed requests
- SSL context configuration for different platforms

### Image Processing Flow
1. Prompt preparation with style templates and reference image injection
2. Base64 encoding of reference images for API submission
3. Concurrent API requests with status tracking
4. Image download and local file management
5. Automatic file naming with conflict resolution

## Reference Image System

### File Organization
- Images stored in `images/[category_name]/[image_name].[ext]`
- Category management through GUI with automatic directory creation
- Global unique naming enforced across all categories

### Auto-matching Logic
- Prompt text is scanned for image names mentioned
- Matching reference images automatically attached to API requests
- Supports multiple reference images per prompt

## Code Patterns

### Configuration Management
```python
# Configuration is loaded/saved through MainWindow methods
self.load_config()  # Reads config.json
self.save_config()  # Writes config.json with current state
```

### Async Operations
```python
# All API calls use AsyncWorker with signal system
worker = AsyncWorker(prompt, api_key, image_data, platform, retry_count)
await worker.run()
```

### GUI State Management
- Table widget for prompt management with custom delegates
- Real-time status updates through Qt signals
- Settings persist across application restarts

## File Structure Conventions
- Single main.py file contains entire application
- Configuration stored as JSON with nested structure for different data types
- Images organized by user-defined categories
- Log files generated in application directory
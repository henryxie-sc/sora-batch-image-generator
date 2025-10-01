-- Placeholder schema for future local SQLite metadata (no code uses it yet)

-- Images table: store generated image metadata
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    prompt TEXT NOT NULL,
    status TEXT NOT NULL,
    filename TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Prompts table: store prompts and config snapshot
CREATE TABLE IF NOT EXISTS prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    prompt TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for quick search
CREATE INDEX IF NOT EXISTS idx_images_number ON images(number);
CREATE INDEX IF NOT EXISTS idx_prompts_number ON prompts(number);


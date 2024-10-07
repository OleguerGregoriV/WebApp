CREATE TABLE IF NOT EXISTS tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    is_deleted INTEGER DEFAULT 0,
    is_archived INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

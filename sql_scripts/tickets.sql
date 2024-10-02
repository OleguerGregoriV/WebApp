CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    description TEXT NOT NULL, 
    due_date DATE NOT NULL,
    is_deleted INTEGER DEFAULT 0, 
    FOREIGN KEY(user_id) REFERENCES users(id)
);

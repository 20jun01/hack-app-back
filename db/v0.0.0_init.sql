-- Description: Initial database schema
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL, -- パスワードはハッシュ化して保存
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notes (
    note_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    title VARCHAR(200) NOT NULL,
    image_id TEXT,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS note_tags (
    note_id UUID REFERENCES notes(note_id),
    tag_id UUID REFERENCES tags(tag_id),
    PRIMARY KEY (note_id, tag_id)
);

CREATE TABLE IF NOT EXISTS comments (
    comment_id UUID PRIMARY KEY,
    note_id UUID REFERENCES notes(note_id),
    user_id UUID REFERENCES users(user_id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    category_id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS note_categories (
    note_id UUID REFERENCES notes(note_id),
    category_id UUID REFERENCES categories(category_id),
    PRIMARY KEY (note_id, category_id)
);

CREATE TABLE IF NOT EXISTS sub_categories (
    sub_category_id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS category_sub_categories (
    category_id UUID REFERENCES categories(category_id),
    sub_category_id UUID REFERENCES sub_categories(sub_category_id),
    PRIMARY KEY (category_id, sub_category_id)
);

CREATE TABLE IF NOT EXISTS notes_sub_categories (
    note_id UUID REFERENCES notes(note_id),
    sub_category_id UUID REFERENCES sub_categories(sub_category_id),
    PRIMARY KEY (note_id, sub_category_id)
);

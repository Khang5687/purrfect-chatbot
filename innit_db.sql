-- PostgreSQL
-- Create the "user" table
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_interaction_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
);

-- Create the "openai_settings" table
CREATE TABLE "openai_settings" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    api_key VARCHAR(255),
    model VARCHAT(25) DEFAULT "gpt-3.5-turbo",
    temperature FLOAT DEFAULT 0.7,
    maximum_length INTEGER DEFAULT 1024,
    top_p FLOAT DEFAULT 1,
    penalty_freq FLOAT DEFAULT 0,
    penalty_pre FLOAT DEFAULT 0
);

-- Create the "chats" table
CREATE TABLE "chats" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL
);

-- Create the "chat_logs" table
CREATE TABLE "chat_logs" (
    id SERIAL PRIMARY KEY,
    chat_id INTEGER REFERENCES "chats"(id) ON DELETE CASCADE,
    log TEXT
);
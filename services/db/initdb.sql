CREATE TABLE IF NOT EXISTS user_user (
    id serial PRIMARY KEY,
    email VARCHAR(320) UNIQUE NOT NULL,
    password BYTEA NOT NULL,
    created_on TIMESTAMP DEFAULT NOW()
)
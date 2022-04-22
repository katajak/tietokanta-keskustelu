SET TIMEZONE="Europe/Helsinki";

DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS areas CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS likes CASCADE;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    title TEXT,
    visible BOOLEAN
);

CREATE TABLE threads (
    id SERIAL PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES users,
    area_id INTEGER REFERENCES areas,
    sent_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    content TEXT,
    user_id INTEGER REFERENCES users,
    area_id INTEGER REFERENCES areas,
    thread_id INTEGER REFERENCES threads,
    sent_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    message_id INTEGER REFERENCES messages,
    liked BOOLEAN
);

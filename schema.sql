CREATE TABLE IF NOT EXISTS "user"(
    "UID" STRING UNIQUE,
    "userName" STRING UNIQUE,
    "password" STRING
);
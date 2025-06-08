CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* 기본 구조만 형성 */
CREATE TABLE "Restaurant" (
    manage_id VARCHAR PRIMARY KEY,
    permission_date DATE,
    store_name VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    legacy_address VARCHAR
);

CREATE TABLE "UserEvaluation" (
    evaluation_id SERIAL PRIMARY KEY,
    store_id VARCHAR NOT NULL,
    user_id INTEGER NOT NULL,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    photo_url VARCHAR,
    eval_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR,
    FOREIGN KEY (user_id) REFERENCES "User"(user_id),
    FOREIGN KEY (store_id) REFERENCES "Restaurant"(manage_id)
);

/* 기본 구조만 형성 */
CREATE TABLE "Action" (
    action_id BIGSERIAL PRIMARY KEY,
    disposal_date DATE,
    store_id VARCHAR NOT NULL,
    guide_date DATE,
    disposal_name VARCHAR,
    legal_reason VARCHAR,
    violation TEXT,
    FOREIGN KEY (store_id) REFERENCES "Restaurant"(manage_id)
);
-- upgrade --
CREATE TABLE IF NOT EXISTS "auth.namespace" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "auth.token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" VARCHAR(64) NOT NULL,
    "valid" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth.token_auth.namespace" (
    "auth.token_id" INT NOT NULL REFERENCES "auth.token" ("id") ON DELETE CASCADE,
    "namespace_id" INT NOT NULL REFERENCES "auth.namespace" ("id") ON DELETE CASCADE
);

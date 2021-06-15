-- upgrade --
CREATE TABLE IF NOT EXISTS "namespace.namespace" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "namespace.token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" VARCHAR(64) NOT NULL,
    "valid" BOOL NOT NULL  DEFAULT True,
    "namespace_id" INT NOT NULL REFERENCES "namespace.namespace" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);

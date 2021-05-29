-- upgrade --
CREATE TABLE IF NOT EXISTS "cronjobmodel" (
    "id" VARCHAR(48) NOT NULL  PRIMARY KEY,
    "enable" INT NOT NULL  DEFAULT 1,
    "technology" VARCHAR(64) NOT NULL,
    "mode" VARCHAR(32) NOT NULL,
    "host" VARCHAR(128) NOT NULL,
    "port" INT NOT NULL  DEFAULT 80,
    "minute" VARCHAR(16) NOT NULL  DEFAULT '*',
    "hour" VARCHAR(16) NOT NULL  DEFAULT '*',
    "day_of_month" VARCHAR(16) NOT NULL  DEFAULT '*',
    "month" VARCHAR(16) NOT NULL  DEFAULT '*',
    "day_of_week" VARCHAR(16) NOT NULL  DEFAULT '*',
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "label" VARCHAR(128),
    "full_command" VARCHAR(512)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);

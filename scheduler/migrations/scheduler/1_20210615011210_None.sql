-- upgrade --
CREATE TABLE IF NOT EXISTS "scheduler.cronjob" (
    "id" VARCHAR(48) NOT NULL  PRIMARY KEY,
    "enable" BOOL NOT NULL  DEFAULT True,
    "technology" VARCHAR(64) NOT NULL,
    "mode" VARCHAR(32) NOT NULL,
    "host" VARCHAR(128) NOT NULL,
    "port" INT NOT NULL  DEFAULT 80,
    "minute" VARCHAR(16) NOT NULL  DEFAULT '*',
    "hour" VARCHAR(16) NOT NULL  DEFAULT '*',
    "day_of_month" VARCHAR(16) NOT NULL  DEFAULT '*',
    "month" VARCHAR(16) NOT NULL  DEFAULT '*',
    "day_of_week" VARCHAR(16) NOT NULL  DEFAULT '*',
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "namespace" VARCHAR(128),
    "full_command" VARCHAR(512)
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);

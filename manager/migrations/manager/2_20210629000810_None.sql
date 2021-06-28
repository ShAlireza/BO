-- upgrade --
CREATE TABLE IF NOT EXISTS "manager.module" (
    "id" VARCHAR(48) NOT NULL  PRIMARY KEY,
    "name" VARCHAR(128) NOT NULL UNIQUE,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "valid_credential_names" TEXT NOT NULL
);
COMMENT ON COLUMN "manager.module"."valid_credential_names" IS 'a comma separated set of values that are valid for this service credentials names';
CREATE TABLE IF NOT EXISTS "manager.moduleinstance" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "host" VARCHAR(256) NOT NULL,
    "port" INT NOT NULL,
    "state" VARCHAR(64) NOT NULL  DEFAULT 'down',
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "module_id" VARCHAR(48) NOT NULL REFERENCES "manager.module" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "manager.secretkey" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "secret_key" VARCHAR(128) NOT NULL UNIQUE,
    "valid" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "manager.serviceinstancedata" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "host" VARCHAR(256) NOT NULL,
    "port" INT NOT NULL,
    "namespace" VARCHAR(256) NOT NULL,
    "module_id" VARCHAR(48) NOT NULL REFERENCES "manager.module" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "manager.serviceinstancecredential" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(256) NOT NULL,
    "value" VARCHAR(512) NOT NULL,
    "service_instance_id" INT NOT NULL REFERENCES "manager.serviceinstancedata" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "manager.token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "key" VARCHAR(64) NOT NULL UNIQUE,
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "expired" BOOL NOT NULL  DEFAULT False,
    "instance_id" INT NOT NULL REFERENCES "manager.moduleinstance" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);

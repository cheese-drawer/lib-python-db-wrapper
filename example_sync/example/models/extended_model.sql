CREATE EXTENSION hstore;

CREATE TABLE IF NOT EXISTS "extended_model" (
    "id" uuid PRIMARY KEY,
    "string" varchar(255),
    "integer" smallint,
    "data" jsonb
);

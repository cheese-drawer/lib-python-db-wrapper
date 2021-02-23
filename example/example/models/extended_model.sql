CREATE EXTENSION hstore;

CREATE TABLE IF NOT EXISTS "extended_model" (
    "_id" uuid PRIMARY KEY,
    "string" varchar(255),
    "integer" smallint,
    "json" jsonb
);

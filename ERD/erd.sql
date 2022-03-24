CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "email" varchar,
  "created_at" timestamp
);

CREATE TABLE "questions" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar,
  "description" varchar,
  "location" varchar,
  "open_at" timestamp,
  "close_at" timestamp,
  "user" int
);

CREATE TABLE "choices" (
  "id" SERIAL PRIMARY KEY,
  "text" varchar,
  "question" int
);

CREATE TABLE "votes" (
  "id" SERIAL PRIMARY KEY,
  "timestamp" varchar,
  "choice" int,
  "name" varchar,
  "user" int
);

ALTER TABLE "choices" ADD FOREIGN KEY ("question") REFERENCES "questions" ("id");

ALTER TABLE "questions" ADD FOREIGN KEY ("user") REFERENCES "users" ("id");

ALTER TABLE "votes" ADD FOREIGN KEY ("user") REFERENCES "users" ("id");

ALTER TABLE "votes" ADD FOREIGN KEY ("choice") REFERENCES "choices" ("id");

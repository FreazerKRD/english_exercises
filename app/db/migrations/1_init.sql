CREATE TABLE "users" (
	"telegram_id" bigint NOT NULL UNIQUE,
	"username" varchar,
	"current_book" integer NOT NULL,
	"exercises" TEXT NOT NULL,
	CONSTRAINT "users_pk" PRIMARY KEY ("telegram_id")
);

CREATE TABLE "user_books" (
	"book_id" integer NOT NULL,
	"user_id" bigint NOT NULL,
	"progress" integer
);

CREATE TABLE "books" (
	"id" serial NOT NULL UNIQUE,
	"file_name" TEXT NOT NULL UNIQUE,
	CONSTRAINT "books_pk" PRIMARY KEY ("id")
);

ALTER TABLE "user_books" ADD CONSTRAINT "user_books_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");
ALTER TABLE "user_books" ADD CONSTRAINT "user_books_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("telegram_id");
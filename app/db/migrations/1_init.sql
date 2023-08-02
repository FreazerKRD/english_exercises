CREATE TABLE "users" (
	"telegram_id" bigint NOT NULL UNIQUE,
	"current_book" integer NOT NULL DEFAULT 1,
	"exercise_adjective_form" BOOLEAN DEFAULT TRUE,
	"exercise_verb_form" BOOLEAN DEFAULT TRUE,
	"exercise_sentence_gen" BOOLEAN DEFAULT TRUE,
	CONSTRAINT "users_pk" PRIMARY KEY ("telegram_id")
);

CREATE TABLE "user_books" (
	"book_id" integer NOT NULL,
	"user_id" bigint NOT NULL,
	"progress" integer NOT NULL DEFAULT 0
);

CREATE TABLE "books" (
	"id" serial NOT NULL UNIQUE,
	"file_name" TEXT NOT NULL UNIQUE,
	CONSTRAINT "books_pk" PRIMARY KEY ("id")
);

ALTER TABLE "user_books" ADD CONSTRAINT "user_books_fk0" FOREIGN KEY ("book_id") REFERENCES "books"("id");
ALTER TABLE "user_books" ADD CONSTRAINT "user_books_fk1" FOREIGN KEY ("user_id") REFERENCES "users"("telegram_id");

INSERT INTO books (file_name) VALUES ('Little_Red_Cap_ Jacob_and_Wilhelm_Grimm.json'), ('Little_Red_Riding_Hood_Charles_Perrault.json') 
	ON CONFLICT (file_name) DO NOTHING;
-- initial table creeation
-- depends:

CREATE TABLE "people" (
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "birth_date" VARCHAR(255),
    "birth_year" INTEGER,
    "birth_place" VARCHAR(255),
    "death_date" VARCHAR(255),
    "death_place" VARCHAR(255),
    "fathers_name" VARCHAR(255),
    "mothers_name" VARCHAR(255),
    "father_id" INTEGER,
    "mother_id" INTEGER,
    "family_id" INTEGER,
    "sex" VARCHAR(255)
);

CREATE TABLE "families" (
    "id" SERIAL PRIMARY KEY,
    "husband_id" INTEGER,
    "wife_id" INTEGER,
    FOREIGN KEY ("husband_id") REFERENCES "people"("id"),
    FOREIGN KEY ("wife_id") REFERENCES "people"("id"),
    "marriage_date" VARCHAR(255),
    "marriage_place" VARCHAR(255)
);

ALTER TABLE "people" ADD FOREIGN KEY ("father_id") REFERENCES "people"("id");
ALTER TABLE "people" ADD FOREIGN KEY ("mother_id") REFERENCES "people"("id");
ALTER TABLE "people" ADD FOREIGN KEY ("family_id") REFERENCES "families"("id");


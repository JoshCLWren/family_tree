-- initial table creeation
-- depends:

CREATE TABLE "people" (
    "id" VARCHAR PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "birth_date" VARCHAR(255),
    "birth_year" INTEGER,
    "birth_place" VARCHAR(255),
    "death_date" VARCHAR(255),
    "death_place" VARCHAR(255),
    "death_year" INTEGER,
    "father" VARCHAR(255),
    "mother" VARCHAR(255),
    "father_id" VARCHAR,
    "mother_id" VARCHAR,
    "sex" VARCHAR(255),
    "tree_level" INTEGER NOT NULL,
    "is_alive" BOOLEAN,
    "FAMC_ID" VARCHAR,
    "FAMS_IDs" VARCHAR[],
    "is_immigrant" BOOLEAN,
    "children" VARCHAR[]
);



CREATE TABLE "traditional_marriages" (
    "id" VARCHAR PRIMARY KEY,
    "husband_id" VARCHAR,
    "marriage_date" VARCHAR(255),
    "marriage_place" VARCHAR(255),
    "marriage_year" INTEGER,
    "wife_id" VARCHAR,
    "tree_level" INTEGER,
    "is_divorced" BOOLEAN,
    "divorce_date" VARCHAR(255)
);



ALTER TABLE "people" ADD FOREIGN KEY ("father_id") REFERENCES "people"("id");
ALTER TABLE "people" ADD FOREIGN KEY ("mother_id") REFERENCES "people"("id");
ALTER TABLE "traditional_marriages" ADD FOREIGN KEY ("husband_id") REFERENCES "people"("id");
ALTER TABLE "traditional_marriages" ADD FOREIGN KEY ("wife_id") REFERENCES "people"("id");



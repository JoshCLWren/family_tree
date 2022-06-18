-- Add countries to people
-- depends: wren_tree20220603_01_ngfis-initial-table-creeation

ALTER TABLE people ADD COLUMN birth_country VARCHAR;
ALTER TABLE people ADD COLUMN death_country VARCHAR;

-- USE customs_db

--=== CAUTION
--DROP TABLE IF EXISTS customs_log;



--=====================================
--=====================================
--============================= STAGING
--=== Create staging table
CREATE TABLE customs_log(
	month VARCHAR(10),
	country VARCHAR(50),
	direction VARCHAR(10),
	code VARCHAR(20),
	category TEXT,
	measure VARCHAR(20),
	value BIGINT,
	netto BIGINT,
	quantity BIGINT,
	region INTEGER,
	district INTEGER,
	meta_year INTEGER,
	meta_month INTEGER
);

-- i did it with 26mil rows and 10 gigs of all data on a laptop, am i brain damaged?
-- P.S.
/*
COPY 26392290

Query returned successfully in 2 min 32 secs.
*/
--=== Copy data
COPY customs_log(month, country, direction, code, category, measure,
	value, netto, quantity, region, district, meta_year, meta_month)
FROM '/data_share/04_pg/original/part-00000-87f41f2b-2742-43d4-a126-705175f01c78-c000.csv'
WITH (
	FORMAT CSV,
	DELIMITER E'\t',
	HEADER true
);

--=== Check data
-- SELECT * FROM customs_log LIMIT 20;
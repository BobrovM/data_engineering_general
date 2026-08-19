--===
-- This script is used to create DB inside Clickhouse client terminal.
--===
-- Script is just copypasted, even that there is an option to 
-- ||clickhouse-client -m < script.sql||

CREATE DATABASE customs;

USE customs;

-- bridge table for batch mirror
CREATE TABLE MIG_pg_customs_log(
	month String,
	country String,
	direction String,
	code String,
	category String,
	measure String,
	value Int64,
	netto Int64,
	quantity Int64,
	region Int32,
	district Int32,
	meta_year Int32,
	meta_month Int32
) ENGINE = PostgreSQL('db-postgres:5432', 'customs_db', 'customs_log', 'officeguy', 'Test4321');

-- test
-- SELECT * FROM MIG_pg_customs_log LIMIT 10;

-- target table to store data in
CREATE TABLE customs_log(
	month String,
	country String,
	direction String,
	code String,
	category String,
	measure String,
	value Int64,
	netto Int64,
	quantity Int64,
	region Int32,
	district Int32,
	meta_year Int32,
	meta_month Int32
) ENGINE = MergeTree()
ORDER BY (meta_year, meta_month, code);

-- test (on a new empty table)
-- SELECT * FROM customs_log LIMIT 10;

INSERT INTO customs_log
SELECT * FROM MIG_pg_customs_log;

--26392290 rows in set. Elapsed: 38.277 sec. Processed 26.39 million rows, 11.66 GB (689.50 thousand rows/s., 304.56 MB/s.)
--Peak memory usage: 924.68 MiB.
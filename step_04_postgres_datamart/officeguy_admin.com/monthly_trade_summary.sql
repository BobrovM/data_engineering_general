-- USE customs_db

--==================================
--==================================
--============================= VIEW
--=== Create view
CREATE VIEW monthly_trade_summary AS
WITH import_val_monthly AS(
	SELECT
		month,
		SUM(value) AS total_import_value
	FROM customs_log 
	WHERE direction = 'ИМ'
	GROUP BY month
),
export_val_monthly AS(
	SELECT
		month,
		SUM(value) AS total_export_value
	FROM customs_log 
	WHERE direction = 'ЭК'
	GROUP BY month
),
redefined_month AS(
	SELECT
		month,
		CONCAT(SUBSTRING(month FROM 4 FOR 4), '/', SUBSTRING(month FROM 1 FOR 2)) AS re_month
	FROM customs_log
	GROUP BY month
),
top_import_category AS(
	SELECT DISTINCT ON (month) -- Postgres ONLY
		month,
		category,
		COUNT(*) AS entries
	FROM customs_log
	WHERE direction = 'ИМ' AND TRIM(category) != 'ПРОЧЕЕ'
	GROUP BY month, category
	ORDER BY month, COUNT(*) DESC
),
top_export_category AS(
	SELECT DISTINCT ON (month) -- Postgres ONLY
		month,
		category,
		COUNT(*) AS entries
	FROM customs_log
	WHERE direction = 'ЭК' AND TRIM(category) != 'ПРОЧЕЕ'
	GROUP BY month, category
	ORDER BY month, COUNT(*) DESC
),
major_import_partner AS(
	SELECT DISTINCT ON (month) -- Postgres ONLY
		month,
		country,
		COUNT(*) AS entries
	FROM customs_log
	WHERE direction = 'ИМ'
	GROUP BY month, country
	ORDER BY month, COUNT(*) DESC
),
major_export_partner AS(
	SELECT DISTINCT ON (month) -- Postgres ONLY
		month,
		country,
		COUNT(*) AS entries
	FROM customs_log
	WHERE direction = 'ЭК'
	GROUP BY month, country
	ORDER BY month, COUNT(*) DESC
),
total_transactions AS(
	SELECT
		month,
		COUNT(*) AS transactions
	FROM customs_log
	GROUP BY month
)
SELECT
	rm.re_month AS month,
	ivl.total_import_value AS total_import_value,
	evl.total_export_value AS total_export_value,
	evl.total_export_value - ivl.total_import_value AS trade_balance,
	tic.category AS "top_import_category",
	tec.category AS "top_export_category",
	mip.country AS "major_import_partner",
	mep.country AS "major_export_partner",
	tt.transactions AS "total_transactions"
FROM redefined_month AS rm
LEFT JOIN import_val_monthly AS ivl ON rm.month = ivl.month
LEFT JOIN export_val_monthly AS evl ON rm.month = evl.month
LEFT JOIN top_import_category AS tic ON rm.month = tic.month
LEFT JOIN top_export_category AS tec ON rm.month = tec.month
LEFT JOIN major_import_partner AS mip ON rm.month = mip.month
LEFT JOIN major_export_partner AS mep ON rm.month = mep.month
LEFT JOIN total_transactions AS tt ON rm.month = tt.month
ORDER BY rm.re_month;


--=== Test VIEW
SELECT
	*
FROM monthly_trade_summary
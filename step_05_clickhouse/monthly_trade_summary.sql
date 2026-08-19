--===
-- This script is used to create DB inside Clickhouse client terminal.
--===
-- Script is just copypasted, even that there is an option to 
-- ||clickhouse-client -m < script.sql||

USE customs;

-- redesigned view from postgres
CREATE VIEW monthly_trade_summary AS
WITH agg_simple AS(
    SELECT
        month,
        sumIf(value, direction = 'ИМ') AS total_import_value,
        sumIf(value, direction = 'ЭК') AS total_export_value,
        count(*) AS total_transactions
    FROM customs_log
    GROUP BY month
),
agg_top_import_category AS(
    SELECT
        month,
        category
    FROM
        (
            SELECT
                month, 
                category,
                row_number() OVER(PARTITION BY month ORDER BY count(*) DESC) AS rn
            FROM customs_log
            WHERE direction = 'ИМ' AND category != 'ПРОЧЕЕ'
            GROUP BY month, category
        )
    WHERE rn = 1
),
agg_top_export_category AS(
    SELECT
        month,
        category
    FROM
        (
            SELECT
                month, 
                category,
                row_number() OVER(PARTITION BY month ORDER BY count(*) DESC) AS rn
            FROM customs_log
            WHERE direction = 'ЭК' AND category != 'ПРОЧЕЕ'
            GROUP BY month, category
        )
    WHERE rn = 1
),
agg_top_import_partner AS(
    SELECT
        month,
        country
    FROM
        (
            SELECT
                month, 
                country,
                row_number() OVER(PARTITION BY month ORDER BY count(*) DESC) AS rn
            FROM customs_log
            WHERE direction = 'ИМ'
            GROUP BY month, country
        )
    WHERE rn = 1
),
agg_top_export_partner AS(
    SELECT
        month,
        country
    FROM
        (
            SELECT
                month, 
                country,
                row_number() OVER(PARTITION BY month ORDER BY count(*) DESC) AS rn
            FROM customs_log
            WHERE direction = 'ЭК'
            GROUP BY month, country
        )
    WHERE rn = 1
),
agg_complex AS(
    SELECT
        atic.month AS month,
        atic.category AS top_import_category,
        atec.category AS top_export_category,
        atip.country AS major_import_partner,
        atep.country AS major_export_partner
    FROM agg_top_import_category AS atic
    LEFT JOIN agg_top_export_category AS atec ON atic.month = atec.month
    LEFT JOIN agg_top_import_partner AS atip ON atic.month = atip.month
    LEFT JOIN agg_top_export_partner AS atep ON atic.month = atep.month
),
redefined_month AS(
	SELECT DISTINCT
		month,
		concat(substring(month, 4, 4), '/', substring(month, 1, 2)) AS re_month
	FROM customs_log
)
SELECT
    rm.re_month AS month,
    agsim.total_import_value,
    agsim.total_export_value,
    agsim.total_export_value - agsim.total_import_value AS trade_balance,
    agcom.top_import_category,
    agcom.top_export_category,
    agcom.major_import_partner,
    agcom.major_export_partner,
    agsim.total_transactions
FROM redefined_month AS rm
LEFT JOIN agg_simple AS agsim ON rm.month = agsim.month
LEFT JOIN agg_complex AS agcom ON rm.month = agcom.month
ORDER BY rm.re_month;
--LIMIT 10;

SELECT
    *
FROM monthly_trade_summary;
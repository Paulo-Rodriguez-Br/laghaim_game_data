query_daily_mean = """
WITH cte_log AS (
    SELECT DISTINCT
        CI AS character_id,
        CL AS lvl,
        TimeInterval AS time_interval,
        Map AS maps,
        date
    FROM table_master
),
table_filtered AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        MAX(lvl) AS max_lvl,
        MIN(lvl) AS min_lvl,
        MAX(lvl) - MIN(lvl) AS lvls_up
    FROM cte_log
    GROUP BY character_id, time_interval, date, maps
),
table_filtered_2 AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        max_lvl,
        min_lvl,
        lvls_up,
        LAG(maps) OVER (
            PARTITION BY character_id, date
            ORDER BY time_interval
        ) AS lag_map,
        LAG(max_lvl) OVER (
            PARTITION BY character_id, date
            ORDER BY time_interval
        ) AS lag_max_lvl
    FROM table_filtered
),
final_work_table AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        max_lvl,
        min_lvl,
        lvls_up,
        CASE 
            WHEN lag_map IS NULL THEN 0
            WHEN maps = lag_map THEN 
                CASE 
                    WHEN (min_lvl - lag_max_lvl) > 0 THEN (min_lvl - lag_max_lvl)
                    ELSE 0
                END
            ELSE 1
        END AS lvls_up_between_time,
        lvls_up + 
        CASE 
            WHEN lag_map IS NULL THEN 0
            WHEN maps = lag_map THEN 
                CASE 
                    WHEN (min_lvl - lag_max_lvl) > 0 THEN (min_lvl - lag_max_lvl)
                    ELSE 0
                END
            ELSE 1
        END AS total_lvls_up
    FROM table_filtered_2
)
SELECT
    maps,
    "date",
    time_interval,
    AVG(total_lvls_up) AS avg_total_lvls_up
FROM
    final_work_table
WHERE
    total_lvls_up <> 0
GROUP BY
    maps,
    "date",
    time_interval;
"""

query_interval_mean = """
WITH cte_log AS (
    SELECT DISTINCT
        CI AS character_id,
        CL AS lvl,
        TimeInterval AS time_interval,
        Map AS maps,
        date
    FROM table_master
),
table_filtered AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        MAX(lvl) AS max_lvl,
        MIN(lvl) AS min_lvl,
        MAX(lvl) - MIN(lvl) AS lvls_up
    FROM cte_log
    GROUP BY character_id, time_interval, date, maps
),
table_filtered_2 AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        max_lvl,
        min_lvl,
        lvls_up,
        LAG(maps) OVER (
            PARTITION BY character_id, date
            ORDER BY time_interval
        ) AS lag_map,
        LAG(max_lvl) OVER (
            PARTITION BY character_id, date
            ORDER BY time_interval
        ) AS lag_max_lvl
    FROM table_filtered
),
final_work_table AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        max_lvl,
        min_lvl,
        lvls_up,
        CASE 
            WHEN lag_map IS NULL THEN 0
            WHEN maps = lag_map THEN 
                CASE 
                    WHEN (min_lvl - lag_max_lvl) > 0 THEN (min_lvl - lag_max_lvl)
                    ELSE 0
                END
            ELSE 1
        END AS lvls_up_between_time,
        lvls_up + 
        CASE 
            WHEN lag_map IS NULL THEN 0
            WHEN maps = lag_map THEN 
                CASE 
                    WHEN (min_lvl - lag_max_lvl) > 0 THEN (min_lvl - lag_max_lvl)
                    ELSE 0
                END
            ELSE 1
        END AS total_lvls_up
    FROM table_filtered_2
)
SELECT
    maps,
    time_interval,
    AVG(total_lvls_up) AS avg_total_lvls_up
FROM
    final_work_table
WHERE
    total_lvls_up <> 0
GROUP BY
    maps,
    time_interval;
"""

query_amount_players_per_date = """
WITH cte_log AS (
    SELECT DISTINCT
        CI AS character_id,
        CL AS lvl,
        TimeInterval AS time_interval,
        Map AS maps,
        date
    FROM table_master
),
table_filtered AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        MAX(lvl) AS max_lvl,
        MIN(lvl) AS min_lvl,
        MAX(lvl) - MIN(lvl) AS lvls_up
    FROM cte_log
    GROUP BY character_id, time_interval, date, maps
),
table_filtered_2 AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        max_lvl,
        min_lvl,
        lvls_up,
        LAG(maps) OVER (
            PARTITION BY character_id, date
            ORDER BY time_interval
        ) AS lag_map,
        LAG(max_lvl) OVER (
            PARTITION BY character_id, date
            ORDER BY time_interval
        ) AS lag_max_lvl
    FROM table_filtered
),
final_work_table AS (
    SELECT
        character_id,
        time_interval,
        maps,
        date,
        max_lvl,
        min_lvl,
        lvls_up,
        CASE 
            WHEN lag_map IS NULL THEN 0
            WHEN maps = lag_map THEN 
                CASE 
                    WHEN (min_lvl - lag_max_lvl) > 0 THEN (min_lvl - lag_max_lvl)
                    ELSE 0
                END
            ELSE 1
        END AS lvls_up_between_time,
        lvls_up + 
        CASE 
            WHEN lag_map IS NULL THEN 0
            WHEN maps = lag_map THEN 
                CASE 
                    WHEN (min_lvl - lag_max_lvl) > 0 THEN (min_lvl - lag_max_lvl)
                    ELSE 0
                END
            ELSE 1
        END AS total_lvls_up
    FROM table_filtered_2
)
SELECT
    "date",
    maps,
    COUNT(character_id) AS amount_players
FROM
    (
        SELECT DISTINCT
            "date",
            character_id,
            maps
        FROM
            final_work_table
        WHERE
            total_lvls_up <> 0
    )
GROUP BY
    "date",
    maps;
"""
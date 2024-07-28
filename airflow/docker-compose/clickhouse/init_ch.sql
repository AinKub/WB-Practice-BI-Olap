create database if not exists report;


create table if not exists penalties
(
    shk_id                UInt64,
    creation_date         DateTime,
    type                  LowCardinality(String),
    penalties             String,
    warehouse_updated_dt  DateTime
)
engine ReplacingMergeTree
partition by toYYYYMM(warehouse_updated_dt)
order by (shk_id, type)
SETTINGS index_granularity = 8192;


create table if not exists report.wh_penalty
(
    dt_date         Date,
    wh_id           UInt16,
    sum_penalty     Decimal(15, 2),
    sum_return      Decimal(15, 2),
    dt_load         DateTime MATERIALIZED now()
)
engine ReplacingMergeTree
order by (dt_date, wh_id)
SETTINGS index_granularity = 8192;
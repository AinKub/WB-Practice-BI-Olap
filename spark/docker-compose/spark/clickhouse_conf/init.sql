CREATE USER IF NOT EXISTS spark IDENTIFIED WITH sha256_password BY 'spark7';

create database if not exists stage;

create database if not exists tmp;

create database if not exists datamart;

create table if not exists stage.raw_shkCreate_edu_7
(
    shk_id          UInt64,
    barcode         String,
    chrt_id         UInt64,
    nm_id           UInt64,
    dt              DateTime,
    employee_id     UInt64,
    place_id        UInt64,
    state_id        LowCardinality(String),
    gi_id           UInt64,
    supplier_id     UInt32,
    invdet_id       UInt64,
    expire_dt       DateTime,
    has_excise      UInt8,
    supplier_box_id Int64,
    is_surplus      UInt8,
    ext_ids         String,
    volume_sm       UInt64,
    entry           LowCardinality(String),
    dt_load         DateTime DEFAULT now()
)
engine MergeTree
order by shk_id
TTL dt_load + toIntervalDay(7)
SETTINGS index_granularity = 8192;


create table if not exists datamart.volume_by_nm
(
    `nm_id` UInt64,
    `vol` UInt64,
    `size_a_sm` UInt32,
    `size_b_sm` UInt32,
    `size_c_sm` UInt32,
    `dt_size_load` DateTime,
    `src_table` LowCardinality(String),
    `src_metric` UInt8
)
engine = ReplacingMergeTree()
order by nm_id
SETTINGS index_granularity = 8192;


grant insert, select on stage.* TO spark;

grant all on tmp.* to spark;

grant select on datamart.* to spark;
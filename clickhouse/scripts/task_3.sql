create database stg;

create database history;

create database current;

create database direct_log;


create table if not exists stg.rating_wh_by_suppliers
(
    wh_id         UInt16    comment 'Блок, которому поставщик поставил оценку'
    , supplier_id UInt32    comment 'ID поставщика'
    , rating      UInt8     comment 'Оценка от 1 до 5'
    , comment     String    comment 'Комментарий, оставленный поставщиком'
    , dt_date     Date      comment 'Дата, когда была поставлена оценка'
    , dt_load     MATERIALIZED now()
)
engine MergeTree
order by (dt_date, wh_id, supplier_id)
partition by toYYYYMM(dt_date)
TTL dt_date + interval 1 year
SETTINGS ttl_only_drop_parts = 1, index_granularity = 8192, merge_with_ttl_timeout = 36000
COMMENT 'Таблица с оценками блоков поставщиками. Staging слой';


create table if not exists history.rating_wh_by_suppliers
(
    wh_id         UInt16    comment 'Блок, которому поставщик поставил оценку'
    , supplier_id UInt32    comment 'ID поставщика'
    , rating      UInt8     comment 'Оценка от 1 до 5'
    , comment     String    comment 'Комментарий, оставленный поставщиком'
    , dt_date     Date      comment 'Дата, когда была поставлена оценка'
    , dt_load     MATERIALIZED now()
)
engine MergeTree
order by (dt_date, wh_id, supplier_id)
partition by toYYYYMM(dt_date)
TTL dt_date + interval 60 day
SETTINGS ttl_only_drop_parts = 1, index_granularity = 8192, merge_with_ttl_timeout = 36000
COMMENT 'Таблица с оценками блоков поставщиками. History слой';


create table if not exists current.rating_wh_by_suppliers
(
    wh_id         UInt16    comment 'Блок, которому поставщик поставил оценку'
    , supplier_id UInt32    comment 'ID поставщика, чья оценка была крайняя'
    , rating      UInt8     comment 'Крайняя оценка от 1 до 5'
    , comment     String    comment 'Крайний комментарий, оставленный поставщиком'
    , dt_date     Date      comment 'Крайняя дата, когда была поставлена оценка'
    , dt_load     MATERIALIZED now()
)
engine ReplacingMergeTree()
order by wh_id
SETTINGS index_granularity = 8192
COMMENT 'Таблица с оценками блоков поставщиками. Слой с текущими данными';


create table if not exists direct_log.rating_wh_by_suppliers
(
    wh_id         UInt16    comment 'Блок, которому поставщик поставил оценку'
    , supplier_id UInt32    comment 'ID поставщика'
    , rating      UInt8     comment 'Оценка от 1 до 5'
    , comment     String    comment 'Комментарий, оставленный поставщиком'
    , dt_date     Date      comment 'Дата, когда была поставлена оценка'
)
engine = Buffer('stg', 'rating_wh_by_suppliers', 16, 10, 100, 10000, 1000000, 10000000, 100000000)
COMMENT 'Буферная таблица с оценками блоков поставщиками';



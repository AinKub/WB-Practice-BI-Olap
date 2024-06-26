create materialized view stg.history_rating_wh_by_suppliers to history.rating_wh_by_suppliers as
select wh_id
    , supplier_id
    , rating
    , comment
    , dt_date 
from stg.rating_wh_by_suppliers;


create materialized view stg.current_rating_wh_by_suppliers to current.rating_wh_by_suppliers as
select wh_id
    , supplier_id
    , rating
    , comment
    , dt_date 
from stg.rating_wh_by_suppliers;

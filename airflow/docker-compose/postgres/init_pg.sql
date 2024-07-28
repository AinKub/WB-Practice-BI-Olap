CREATE SCHEMA IF NOT EXISTS report;

CREATE SCHEMA IF NOT EXISTS sync;

CREATE TABLE IF NOT EXISTS report.wh_penalty
(
    dt_date     Date           NOT NULL,
    wh_id       Smallint       NOT NULL,
    sum_penalty Numeric(15, 2) NOT NULL,
    sum_return  Numeric(15, 2) NOT NULL,
    
    PRIMARY KEY (dt_date, wh_id)
);

CREATE OR REPLACE PROCEDURE sync.wh_penalty_import(_src JSON)
    SECURITY DEFINER
    LANGUAGE plpgsql
AS
$$
BEGIN
    INSERT INTO report.wh_penalty AS penalty(dt_date,
                                             wh_id,
                                             sum_penalty,
                                             sum_return)
    SELECT s.dt_date,
           s.wh_id,
           s.sum_penalty,
           s.sum_return
    FROM JSON_TO_RECORDSET(_src) AS s(dt_date     Date,
                                      wh_id       Smallint,
                                      sum_penalty Numeric(15, 2),
                                      sum_return  Numeric(15, 2))
    ON CONFLICT (dt_date, wh_id) DO UPDATE
    SET sum_penalty = EXCLUDED.sum_penalty,
        sum_return  = EXCLUDED.sum_return;
END;
$$;

-- Пользователь с правами только на чтение

create role readonly;

grant show tables, select on *.* to readonly;

CREATE USER readonly IDENTIFIED WITH SHA256_password BY 'qwerty' DEFAULT ROLE readonly;


-- Пользователь с возможностью создавать и заполнять данные в БД стейджинга(stg) 

create role stg_writer;

grant create table, insert on stg.* to stg_writer;

CREATE USER stg_writer IDENTIFIED WITH SHA256_password BY 'stg_qwerty' DEFAULT ROLE stg_writer;

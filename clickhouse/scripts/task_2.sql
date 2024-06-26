CREATE USER clickhouse_admin IDENTIFIED WITH sha256_password BY 'qwerty1234567';

GRANT ALL ON *.* TO clickhouse_admin WITH GRANT OPTION;

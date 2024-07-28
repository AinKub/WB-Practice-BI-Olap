from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

default_args = {
    "owner": "Andreev",
    "start_date": datetime(2024, 7, 28),
    "retries": 1,
    "retry_delay": timedelta(seconds=60),
}

dag = DAG(
    dag_id="report_wh_penalties",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    max_active_runs=1
)


def main():
    import json
    import psycopg2
    from clickhouse_driver import Client

    days_ago = 0
    
    with open('/opt/airflow/dags/keys/connect.json') as json_file:
        param_сonnect = json.load(json_file)

    client_CH = Client(
        param_сonnect['clickhouse'][0]['host'],
        user=param_сonnect['clickhouse'][0]['user'],
        password=param_сonnect['clickhouse'][0]['password'],
        port=param_сonnect['clickhouse'][0]['port'],
        verify=False,
        compression=True
    )

    client_PG = psycopg2.connect(
        host=param_сonnect['postgres'][0]['host'],
        user=param_сonnect['postgres'][0]['user'],
        password=param_сonnect['postgres'][0]['password'],
        port=param_сonnect['postgres'][0]['port'],
        database=param_сonnect['postgres'][0]['database']
    )

    client_CH.execute(f"""
        INSERT INTO report.wh_penalty
        select fine_state_date                                        dt_date
            , wh_id
            , sumIf(money_income, fine_type = 'penalty') / 100        sum_penalty
            , (sumIf(money_income, fine_type = 'return') * -1) / 100  sum_return
        from
        (
            select JSONExtract(arr, 'wh_id', 'UInt16')                                      wh_id
                , JSONExtract(arr, 'employee_id', 'UInt32')                                 employee_id
                , JSONExtract(arr, 'money_income', 'Decimal(15,2)')                         money_income
                , toDate(
                    parseDateTimeBestEffortOrZero(
                        substring(JSONExtract(arr, 'fine_state_date', 'String'), 1, 10)
                    )
                )                                                                           fine_state_date
                , JSONExtract(arr, 'fine_type', 'String')                                   fine_type
                , JSONExtract(arr, 'fine_state_id', 'UInt16')                               fine_state_id
                , arrayJoin(JSONExtractArrayRaw(penalties, 'warehouse'))                    arr
            from penalties final
            prewhere warehouse_updated_dt >= today() - interval {days_ago} day 
                and warehouse_updated_dt < today() - interval {days_ago} day + interval 1 day
            where 1
                and fine_state_date = today() - interval {days_ago} day 
                and type = 'defective'
                and fine_state_id = 6  -- штраф/возврат подтвержден (выполнен)
        )
        group by dt_date, wh_id
    """)
    print('Вставка в витрину report.wh_penalty в кликхаусе прошла успешно')

    df = client_CH.query_dataframe(f"""
        select dt_date
            , wh_id
            , sum_penalty
            , sum_return
        from report.wh_penalty final
        where dt_date >= today() - interval {days_ago} day
            and dt_date < today() - interval {days_ago} day + interval 1 day
    """)

    df = df.to_json(orient='records', date_format='iso')

    cursor = client_PG.cursor()
    cursor.execute(f"CALL sync.wh_penalty_import(_src := '{df}')")
    client_PG.commit()

    print('Вставка в витрину report.wh_penalty в постгресе прошла успешно')

    cursor.close()
    client_PG.close()

    client_CH.disconnect()


task1 = PythonOperator(
    task_id="report_wh_penalties",
    python_callable=main,
    dag=dag
)
from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from clickhouse_driver import Client

import os
import pandas as pd
import json
from datetime import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Нужно указать, чтобы spark подгрузил lib для kafka.
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars org.apache.spark:spark-sql-kafka-0-10_2.12-3.5.0 --packages org.apache.spark:spark-sql-kafka-0-10_2.12-3.5.0 pyspark-shell'

# Загружаем конекты. Не выкладываем в гит файл с конектами.
with open('/opt/spark/Streams/credentials.json') as json_file:
    сonnect_settings = json.load(json_file)

ch_db_name = "stage"  # Схема на локальном клике
ch_dst_table = "raw_shkCreate_edu_7"

client = Client(сonnect_settings['ch'][0]['host'],
                user=сonnect_settings['ch'][0]['user'],
                password=сonnect_settings['ch'][0]['password'],
                verify=False,
                database=ch_db_name,
                settings={"numpy_columns": True, 'use_numpy': True},
                compression=True)

client_local = Client(сonnect_settings['ch_local'][0]['host'],
                      user=сonnect_settings['ch_local'][0]['user'],
                      password=сonnect_settings['ch_local'][0]['password'],
                      verify=False,
                      database=ch_db_name,
                      settings={"numpy_columns": True, 'use_numpy': True},
                      compression=True)

# Разные переменные, задаются в params.json
spark_app_name = "shkCreate_edu_7"
spark_ui_port = "8081"

kafka_host = сonnect_settings['kafka'][0]['host']
kafka_port = сonnect_settings['kafka'][0]['port']
kafka_user = сonnect_settings['kafka'][0]['user']
kafka_password = сonnect_settings['kafka'][0]['password']
kafka_topic = "shkCreate"
kafka_batch_size = 5000
processing_time = "5 second"

checkpoint_path = f'/opt/kafka_checkpoint_dir/{spark_app_name}/{kafka_topic}/v1'

# Создание сессии спарк.
spark = SparkSession \
    .builder \
    .appName(spark_app_name) \
    .config('spark.ui.port', spark_ui_port)\
    .config("spark.dynamicAllocation.enabled", "false") \
    .config("spark.executor.cores", "1") \
    .config("spark.task.cpus", "1") \
    .config("spark.num.executors", "1") \
    .config("spark.executor.instances", "1") \
    .config("spark.default.parallelism", "1") \
    .config("spark.cores.max", "1") \
    .config('spark.ui.port', spark_ui_port)\
    .getOrCreate()

# убираем разные Warning.
spark.sparkContext.setLogLevel("WARN")
spark.conf.set("spark.sql.adaptive.enabled", "false")
spark.conf.set("spark.sql.debug.maxToStringFields", 500)

# Описание как создается процесс spark structured streaming.
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", f"{kafka_host}:{kafka_port}") \
    .option("subscribe", kafka_topic) \
    .option("maxOffsetsPerTrigger", kafka_batch_size) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .option("kafka.sasl.jaas.config", f'org.apache.kafka.common.security.plain.PlainLoginModule required username="{kafka_user}" password="{kafka_password}";') \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.security.protocol", "SASL_PLAINTEXT") \
    .load()

# Колонки, которые писать в ClickHouse. В kafka много колонок, не все нужны. Этот tuple нужен перед записью в ClickHouse.
columns_to_ch = ("shk_id", "barcode", "chrt_id", "nm_id", "dt", "employee_id",
                 "place_cod", "state_id", "gi_id", "supplier_id", "invdet_id", 
                 "expire_dt", "has_excise", "supplier_box_id", "is_surplus", "ext_ids")


# Схема сообщений в топике kafka. Используется при формировании batch.
schema = StructType([
    StructField("shk_id", LongType(), False),
    StructField("barcode", StringType(), True),
    StructField("chrt_id", LongType(), True),
    StructField("nm_id", LongType(), True),
    StructField("create_dt", StringType(), False),
    StructField("dt", StringType(), False),
    StructField("employee_id", LongType(), True),
    StructField("place_cod", LongType(), True),
    StructField("state_id", StringType(), True),
    StructField("gi_id", LongType(), True),
    StructField("supplier_id", LongType(), True),
    StructField("invdet_id", LongType(), True),
    StructField("expire_dt", StringType(), True),
    StructField("supplier_box_id", LongType(), True),
    StructField("is_surplus", BooleanType(), True),
    StructField("has_excise", BooleanType(), True),
    StructField("ext_ids", StringType(), True),
    StructField("entry", StringType(), True),
    StructField("dt_load", StringType(), True),
])

sql_tmp_create = """create table tmp.tmp_shkCreate_edu_7
    (
        shk_id          UInt64,
        barcode         String,
        chrt_id         UInt64,
        nm_id           UInt64,
        dt              DateTime,
        employee_id     UInt64,
        place_id        UInt64,
        state_id LowCardinality(String),
        gi_id           UInt64,
        supplier_id     UInt32,
        invdet_id       UInt64,
        expire_dt       DateTime,
        has_excise      UInt8,
        supplier_box_id Int64,
        is_surplus      UInt8,
        ext_ids         String
    )
        engine = Memory
"""

sql_insert = f"""insert into {ch_db_name}.{ch_dst_table}
    select shk_id, barcode, chrt_id, nm_id, dt, employee_id, place_id, state_id
        , gi_id, supplier_id, invdet_id, expire_dt, has_excise
        , supplier_box_id, is_surplus, ext_ids, volume_sm, 'shkCreate_kafka' entry
    from tmp.tmp_shkCreate_edu_7 t1
    left any join
    (
        select nm_id, vol volume_sm
        from datamart.volume_by_nm final
        where nm_id in (select nm_id from tmp.tmp_shkCreate_edu_7)
    ) vols
    on t1.nm_id = vols.nm_id
"""

client.execute("drop table if exists tmp.tmp_shkCreate_edu_7")

def column_filter(df):
    # select только нужные колонки.
    col_tuple = []
    for col in columns_to_ch:
        col_tuple.append(f"value.{col}")
    return df.selectExpr(col_tuple)


def load_to_ch(df):
    # Преобразуем в dataframe pandas и записываем в ClickHouse.
    df_pd = df.toPandas()
    df_pd.dt = pd.to_datetime(df_pd.dt, format='ISO8601', utc=True, errors='ignore')+pd.Timedelta(hours=3)
    df_pd.expire_dt = df_pd.expire_dt.str.slice(0, 10)
    df_pd.expire_dt = df_pd.expire_dt.fillna('1970-01-01')
    df_pd.expire_dt = df_pd.expire_dt.str.replace('2270','2260')
    df_pd.expire_dt = pd.to_datetime(df_pd.expire_dt, format='%Y-%m-%d', errors='ignore')
    df_pd.has_excise = df_pd.has_excise.astype(bool)
    df_pd.ext_ids = df_pd.ext_ids.fillna('').astype(str)

    client.insert_dataframe('INSERT INTO tmp.tmp_shkCreate_edu_7 VALUES', df_pd)

# Функция обработки batch. На вход получает dataframe-spark.
def foreach_batch_function(df2, epoch_id):

    df_rows = df2.count()
    # Если dataframe не пустой, тогда продолжаем.
    if df_rows > 0:
        # df2.printSchema()
        # df2.show(5)

        # Убираем не нужные колонки.
        df2 = column_filter(df2)

        client.execute(sql_tmp_create)

        # Записываем dataframe в ch.
        load_to_ch(df2)

        # Добавляем объем и записываем в конечную таблицу.
        client.execute(sql_insert)
        client.execute("drop table if exists tmp.tmp_shkCreate_edu_7")


# Описание как создаются микробатчи. processing_time - задается вначале скрипта
query = df.select(from_json(col("value").cast("string"), schema).alias("value")) \
    .writeStream \
    .trigger(processingTime=processing_time) \
    .option("checkpointLocation", checkpoint_path) \
    .foreachBatch(foreach_batch_function) \
    .start()

query.awaitTermination()

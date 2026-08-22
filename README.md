# DATA ENGINEERING (course)

As of 02 August 2026, everything is now in docker containers.
The containers are:

1. Python script container;
2. HDFS namenode container;
3. HDFS datanode container;
4. YARN resourcemanager container;
5. YARN nodemanager container;
6. Spark pyspark/jupyter container;
7. Postgres database container;
8. Postgres admin4 container;
9. Clickhouse db container.

###### Contains:

1. **Python** data ingestion  
(Getting **customs import/export data** through REST API with pagination and possibility of 429 timeout)  
((Sample can be found in **data\_share/01\_ingestion**))
2. **Hadoop Yarn** MapReduce  
(Map reducing, enriching with **TNVED3** and sorting data)  
((Shell scripts are in the shell\_scripts folders))
3. **SPARK** aggregation  
(Data marts writen in parquet files, partitioned by year and month, with a little enrichment from **TNVED3** and **NULL** replacement)
4. **Postgres** table and view creation with data copy from step 03 and forward data manipulation and preparation with analytical view table  
(parquet -> csv -> copy to PG, 26.000.000 rows, 10GBs of data)
5. **Clickhouse** table as a mirror of a **Postgres** table and redesigned analitycal view table for **Clickhouse** sql  
(temporary table on ENGINE = PostgreSQL -> data copy into same table on ENGINE = MergeTree(), redesigned view from postgres)



###### In foreseeable future:

6\. Airflow

7\. Kafka

8\. NiFi

9\. Data Lake and DWH

10\. Data life cycle and data quality


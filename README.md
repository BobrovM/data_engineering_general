# DATA ENGINEERING (course)

As of 02 August 2026, everything is now in docker containers.
The containers are:
01. Python script container;
02. HDFS namenode container;
03. HDFS datanode container;
04. YARN resourcemanager container;
05. YARN nodemanager container;
06. Spark pyspark/jupyter container;
07. Postgres database container;
08. Postgres admin4 container.

###### Contains:

01. **Python** data ingestion   
(Getting **customs import/export data** through REST API with pagination and possibility of 429 timeout)    
((Sample can be found in **data_share/01_ingestion**))
02. **Hadoop Yarn** MapReduce   
(Map reducing, enriching with **TNVED3** and sorting data)  
((Shell scripts are in the shell_scripts folders))
03. **SPARK** aggregation   
(Data marts writen in parquet files, partitioned by year and month, with a little enrichment from **TNVED3** and **NULL** replacement)
04. **Postgres** table and view creation with data copy from step 03 and forward data manipulation and preparation  
(parquet -> csv -> copy to PG, 26.000.000 rows, 10GBs of data)

###### In foreseeable future:

5\. NOSQL DBs for DE

6\. Data orchestration, ETL tools

7\. Airflow

8\. Kafka

9\. NiFi

10\. Data Lake and DWH

11\. Data life cycle and data quality


# DATA ENGINEERING (course)

As of 02 August 2026, everything is now in docker containers.
The containers are:
01. Python script container;
02. HDFS namenode container;
03. HDFS datanode container;
04. YARN resourcemanager container;
05. YARN nodemanager container
06. Spark pyspark/jupyter container. 

###### Contains:

01. Python data ingestion
(Getting **customs import/export data** through REST API with pagination and possibility of 429 timeout)
((Sample can be found in **data_share/01_ingestion**))
02. Hadoop Yarn MapReduce
(Map reducing, enriching with **TNVED3** and sorting data)
((Shell scripts are in the shell_scripts folders))
03. SPARK aggregation
(Data marts writen in parquet files, partitioned by year and month, with a little enrichment from **TNVED3** and **NULL** replacement)

###### In foreseeable future:

4\. Relational DBs for DE

5\. NOSQL DBs for DE

6\. Data orchestration, ETL tools

7\. Airflow

8\. Kafka

9\. NiFi

10\. Data Lake and DWH

11\. Data life cycle and data quality


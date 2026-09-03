# DATA ENGINEERING (course)
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
10. Redis container;
11. Airflow-apiserver container;
12. Airflow-scheduler container;
13. Airflow-dag-processor container;
14. Airflow-worker container;
15. Airflow-triggerer container;
16. Airflow-init container;
17. Airflow-cli container;
18. Flower container.

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
6. **Airflow** DAGs, first one of which orchestrate the check for an updated version of TNVED3 codes through **Selenium** and downloads a new version with additional decoding if the date of the relevance date is updated, and after that the second one launches **MapReduce** jobs in **Hadoop** + **HDFS** through SSH with loading one of step's results into **Postgres** for updating the enrichment data.  
(DAG 1 (@daily): Site's frontend -> Selenium scraping -> Date comparison with Airflow variable -> Download through requests with zipfile unzipping and decoding data from cp866 with saving on disk)  
(DAG 2 (@daily): Checks file modification date -> Date comparison with Airflow variable -> Puts file into HDFS -> runs MapReduce jobs through SSH -> updates data in Postgres with the results)
7. **Kafka** streaming 26 million rows of data from a CSV:  
Producer reads customs data from CSV and sends to 'customs_log' topic in batches;  
Consumer reads messages from Kafka topic and processes them.


###### In foreseeable future:
8\. NiFi
9\. Data Lake and DWH
10\. Data life cycle and data quality
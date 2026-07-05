# #!/bin/bash

yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.map.log.level=DEBUG \
  	-D mapreduce.reduce.log.level=DEBUG \
	-input /task1/input/customs_data.csv \
	-output /task1/output_t2 \
	-mapper mapper_cli_customs_history_csv.py \
	-reducer reducer_cli_customs_history.py \
	-file /mnt/d/data_engineering_general/step_02_hadoop_map_reduce/mapper_cli_customs_history_csv.py \
	-file /mnt/d/data_engineering_general/step_02_hadoop_map_reduce/reducer_cli_customs_history.py\
	-cacheFile "/task1/output_t1/part-00000#customs_codes_descs"

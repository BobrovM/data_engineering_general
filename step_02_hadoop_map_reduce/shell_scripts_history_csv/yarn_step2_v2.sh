yarn jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.5.0.jar \
	-D mapreduce.map.log.level=DEBUG \
  	-D mapreduce.reduce.log.level=DEBUG \
	-input /task1/input/customs_data.csv \
	-output /task1/output_t2 \
	-mapper mapper_cli_customs_history_csv.py \
	-reducer reducer_cli_customs_history.py \
	-file /scripts/mapper_cli_customs_history_csv.py \
	-file /scripts/reducer_cli_customs_history.py\
	-cacheFile "/task1/output_t1/part-00000#customs_codes_descs"
# #!/bin/bash

yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.map.log.level=DEBUG \
  	-D mapreduce.reduce.log.level=DEBUG \
	-D stream.num.map.output.key.fields=1 \
	-D mapreduce.partition.keycomparator.options="-k1,1nr" \
	-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
	-input /task1/output_t2/part-00000 \
	-output /task1/output_lazysort \
	-mapper mapper_lazy_sort.py \
	-reducer reducer_lazysort.py \
	-file /mnt/d/data_engineering_general/step_02_hadoop_map_reduce/mapper_lazy_sort.py \
	-file /mnt/d/data_engineering_general/step_02_hadoop_map_reduce/reducer_lazysort.py

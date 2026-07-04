# #!/bin/bash

yarn jar $HADOOP_STREAMING_JAR \
	-input /task1/input/TNVED3_DECODED.TXT \
	-output /task1/output_t1 \
	-mapper mapper_cli_customs_codedescs.py \
	-reducer reducer_cli_customs_codedescs.py \
	-file /mnt/d/data_engineering_general/step_02_hadoop_map_reduce/mapper_cli_customs_codedescs.py \
	-file /mnt/d/data_engineering_general/step_02_hadoop_map_reduce/reducer_cli_customs_codedescs.py

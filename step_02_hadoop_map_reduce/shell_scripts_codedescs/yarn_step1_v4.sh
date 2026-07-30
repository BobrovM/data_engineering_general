yarn jar /opt/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.5.0.jar \
	-input /task1/input/TNVED3_DECODED.TXT \
	-output /task1/output_t1 \
	-mapper mapper_cli_customs_codedescs.py \
	-reducer reducer_cli_customs_codedescs.py \
	-file /scripts/mapper_cli_customs_codedescs.py \
	-file /scripts/reducer_cli_customs_codedescs.py
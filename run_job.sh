#!/bin/bash

# Configuration
OUTPUT_DIR="/user/praveen/output"
STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar"
INPUT_FILE="/user/praveen/input/emails.txt"

echo "-------------------------------------------"
echo "Cleaning up old HDFS output directory..."
hdfs dfs -rm -r $OUTPUT_DIR 2>/dev/null

echo "Launching Hadoop Streaming Job..."
echo "-------------------------------------------"

# Fix: Added single quotes around the $(pwd) paths
hadoop jar $STREAMING_JAR \
  -input $INPUT_FILE \
  -output $OUTPUT_DIR \
  -mapper "python3 '$(pwd)/scripts/mapper.py'" \
  -reducer "python3 '$(pwd)/scripts/reducer.py'"

echo "-------------------------------------------"
echo "Job finished. Final Word Count Results (Top 10):"
echo "-------------------------------------------"
hdfs dfs -cat $OUTPUT_DIR/part-00000 | sort -k2 -nr | head -n 10
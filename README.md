# Enron Email Word Count – Hadoop MapReduce

## Team Members
- EG/2020/3953 – Hapuarachchi H.P.L.
- EG/2020/3812 – Akurana B.N.T.M.
- EG/2020/4029 – Kulathilaka W.A.S.P.

## Overview
This project implements a classic Word Count MapReduce job on the Enron Email Dataset using Hadoop Streaming with Python. The goal is to analyse the frequency of meaningful words across approximately 500,000 emails, demonstrating Hadoop's capability for large‑scale distributed data processing.  
**Enhancements:** The mapper filters out common English stop words, ignores tokens shorter than 3 characters, and skips long repetitive character sequences (e.g., `aaaaa`). This yields more relevant business‑ and domain‑specific vocabulary.

## Dataset
- **Source:** [Kaggle – Enron Email Dataset](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset)
- **Original format:** CSV (columns: `file`, `message`)
- **Size:** ~1.4 GB, ~517,000 rows
- **Preprocessing:** The `message` column is extracted and saved as `data/emails.txt` (one email per line). This simplifies input for Hadoop.

## Requirements
- **Hadoop:** Version 3.3.6 (pseudo‑distributed mode)
- **Java:** OpenJDK 8
- **Python:** Version 3.x
- **Operating System:** Linux (tested on Ubuntu 24.04 via WSL2)

## Setup Instructions

### 1. Install Hadoop
Follow the steps below to install and configure Hadoop.

```bash
# Download Hadoop 3.3.6
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz
tar -xzf hadoop-3.3.6.tar.gz
sudo mv hadoop-3.3.6 /usr/local/hadoop
```

### 2. Set Environment Variables
Add the following lines to your `~/.bashrc` file:

```bash
export HADOOP_HOME=/usr/local/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
```

Then reload the profile:
```bash
source ~/.bashrc
```

### 3. Configure Hadoop
Edit the following configuration files in `$HADOOP_HOME/etc/hadoop/`:

**`core-site.xml`**
```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

**`hdfs-site.xml`**
```xml
<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>
```

**`mapred-site.xml`**
```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value>$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*</value>
  </property>
</configuration>
```

**`yarn-site.xml`**
```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
  </property>
</configuration>
```

### 4. Format HDFS and Start Services
```bash
hdfs namenode -format   # only the first time
start-dfs.sh
start-yarn.sh
```

Verify the services are running:
```bash
jps
```
You should see: `NameNode`, `DataNode`, `SecondaryNameNode`, `ResourceManager`, `NodeManager`.

### 5. Prepare the Input Data
1. **Download the dataset** from Kaggle and place `emails.csv` in the `data/` folder.
2. **Preprocess** the CSV to extract the `message` column:
   ```bash
   python3 scripts/preprocess.py
   ```
   This creates `data/emails.txt`.
3. **Create an input directory in HDFS** and upload the file:
   ```bash
   hdfs dfs -mkdir -p /user/$(whoami)/input
   hdfs dfs -put data/emails.txt /user/$(whoami)/input/
   ```

### 6. Run the MapReduce Job
Use Hadoop Streaming with the `-files` option to ship the Python scripts to the cluster. This avoids having to copy them manually to every node.

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar \
  -files "$(pwd)/scripts/mapper.py,$(pwd)/scripts/reducer.py" \
  -input /user/$(whoami)/input/emails.txt \
  -output /user/$(whoami)/output \
  -mapper "python3 mapper.py" \
  -reducer "python3 reducer.py"
```

**Note:** The `-files` option makes `mapper.py` and `reducer.py` available in the working directory of each task, so they can be invoked simply by name.

### 7. Retrieve the Results
```bash
# List output directory
hdfs dfs -ls /user/$(whoami)/output

# View the most frequent words (sorted by count)
hdfs dfs -cat /user/$(whoami)/output/part-00000 | sort -k2 -nr | head -20

# Copy output to local filesystem
hdfs dfs -get /user/$(whoami)/output/part-00000 ./output/results.txt
```

## Results
After running the job, the top 10 most frequent words (after stop‑word removal) are shown in the bar chart below. These words reflect key Enron‑specific terms and email metadata, confirming that our filtering successfully removed common English words.

![Top 10 Words Chart](enron_wordcount_chart.png)

The chart illustrates that `enron` and `com` dominate the corpus, followed by email header fields such as `recipients`, `content`, and `subject`. This indicates that the dataset retains a rich set of metadata and business terminology.

### 8. Stop Hadoop Services
When finished, shut down the daemons:
```bash
stop-yarn.sh
stop-dfs.sh
```

## File Structure
```
enron-wordcount/
├── README.md
├── scripts/
│   ├── preprocess.py          # CSV to text conversion
│   ├── mapper.py               # MapReduce mapper (with stop‑word filtering)
│   └── reducer.py              # MapReduce reducer
├── data/
│   ├── emails.csv              # Original download (not included in repo)
│   └── emails.txt              # Preprocessed input (generated)
├── input/                       # (optional) local input mirror
├── output/                      # local copy of results
├── screenshots/                 # evidence for report
├── enron_wordcount_chart.png    # bar chart of top words
└── report.pdf                   # final 2‑page report
```

## Notes
- The `-files` option requires absolute paths; `$(pwd)` expands to the current directory.
- If you encounter memory issues, adjust YARN container memory settings in `yarn-site.xml` (e.g., `yarn.nodemanager.resource.memory-mb`).
- The job may take 10–15 minutes depending on your machine’s resources.

## Troubleshooting
- **`JAVA_HOME` not found:** Ensure `JAVA_HOME` is set in `hadoop-env.sh` (uncomment and set the correct path).
- **SSH connection refused:** Set up passwordless SSH to localhost:
  ```bash
  ssh-keygen -t rsa -P "" -f ~/.ssh/id_rsa
  cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
  chmod 600 ~/.ssh/authorized_keys
  ssh localhost  # should connect without password
  ```
- **Mapper/reducer script not found:** Verify that the paths provided to `-files` are correct and that the scripts exist.

## License
This project is for educational purposes as part of the Cloud Computing module at the University of Ruhuna.
```
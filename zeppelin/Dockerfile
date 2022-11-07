FROM apache/zeppelin:0.10.1

RUN wget https://archive.apache.org/dist/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz && \
    tar -xzvf spark-3.2.1-bin-hadoop3.2.tgz

# RUN mv spark-3.2.1-bin-hadoop3.2 ../spark

RUN rm spark-3.2.1-bin-hadoop3.2.tgz

ENV SPARK_HOME=./spark-3.2.1-bin-hadoop3.2
ENV ZEPPELIN_LOG_DIR=./logs
ENV ZEPPELIN_NOTEBOOK_DIR=./notebook
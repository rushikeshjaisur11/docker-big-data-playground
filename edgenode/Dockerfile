FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8
RUN apt update && apt install  openssh-server sudo -y
RUN apt install wget
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && echo PATH="/root/miniconda3/bin":$PATH >> .bashrc \
    && exec bash \
    && conda --version
RUN cp -r /root/miniconda3 /miniconda3
RUN groupadd sshgroup && useradd -ms /bin/bash -g sshgroup rushi
RUN mkdir -p /home/sshuser/.ssh
RUN echo 'Rushi@123\nRushi@123' | sudo passwd rushi 
RUN sudo usermod -aG sudo rushi
# Start SSH service
RUN service ssh start
# Expose docker port 22
RUN wget https://archive.apache.org/dist/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz && \
    tar -xzvf spark-3.2.1-bin-hadoop3.2.tgz

# RUN mv spark-3.2.1-bin-hadoop3.2 ../spark
ENV SPARK_HOME=./spark-3.2.1-bin-hadoop3.2
RUN rm spark-3.2.1-bin-hadoop3.2.tgz
ENV PATH=$PATH:./spark-3.2.1-bin-hadoop3.2/bin/
ENV PATH=$PATH:./miniconda3/bin/
RUN echo "y" |  apt remove wget 
USER rushi
ENV PATH=$PATH:./spark-3.2.1-bin-hadoop3.2/bin/
ENV PATH=$PATH:./miniconda3/bin/
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]
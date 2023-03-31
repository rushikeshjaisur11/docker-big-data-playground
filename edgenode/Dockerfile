FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8
RUN apt update && apt install  openssh-server sudo -y
RUN apt install wget
RUN wget \
    https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Anaconda3-2023.03-Linux-x86_64.sh -b \
    && rm -f Anaconda3-2023.03-Linux-x86_64.sh \
    && echo PATH="/root/anaconda3/bin":$PATH >> .bashrc \
    && exec bash 
RUN /root/anaconda3/bin/pip3 install findspark
RUN /root/anaconda3/bin/pip3 install pyspark==3.2.1
RUN cp -r /root/anaconda3 /anaconda3
# Start SSH service
RUN service ssh start
# Expose docker port 22
ENV PATH=/opt/hadoop-3.2.1/bin/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/anaconda3/bin/:/anaconda3/bin/:/usr/lib/jvm/java-8-openjdk-amd64/bin
RUN echo "y" |  apt remove wget 
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]
COPY profile /etc/profile
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
RUN groupadd -r bigdata && useradd -ms /bin/bash -r -g bigdata rushi
RUN mkdir -p /home/rushi/.ssh
RUN echo 'Rushi@123\nRushi@123' | sudo passwd rushi 
RUN sudo usermod -aG sudo rushi
RUN echo "export PATH=$PATH" > /etc/environment
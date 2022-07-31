FROM onosproject/onos:2.7-latest
COPY backup.tar.gz /
RUN /root/onos/bin/onos-restore /backup.tar.gz
EXPOSE 8181 8101 9876 6653 6640
CMD /root/onos/bin/onos-service start



FROM confluentinc/cp-ksqldb-server:7.7.1

USER root

ARG STOREPASS

RUN mkdir --parents /usr/local/share/ca-certificates/Yandex/ && \
    wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" \
         --output-document /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt && \
    chmod 0655 /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt

RUN mkdir /truststore && \
    keytool -import \
            -file /usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt \
            -storepass ${STOREPASS} \
            -alias "kafka-ui-cert" \
            -keystore /truststore/truststore.jks \
            -noprompt

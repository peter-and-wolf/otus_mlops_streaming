kafka_bootstrap_servers=[
  'rc1a-m9eq2fpqvhar1705.mdb.yandexcloud.net:9091',
  'rc1b-vgn8nra3bkdhhhbv.mdb.yandexcloud.net:9091',
  'rc1d-kcaf229pa6mjpb8c.mdb.yandexcloud.net:9091'
]

kafka_security_protocol='SASL_SSL'
kafka_sasl_mechanism='SCRAM-SHA-512'
kafka_ssl_cafile='/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt'
kafka_input_topic='inputs'
kafka_output_topic='predictions'


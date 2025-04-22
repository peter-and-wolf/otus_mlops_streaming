kafka_bootstrap_servers=[
  'rc1a-9v8nqvdpqid88ptq.mdb.yandexcloud.net:9091',
  'rc1b-77otp66h567jsbia.mdb.yandexcloud.net:9091',
  'rc1d-ebjvsfnkp8m7iqps.mdb.yandexcloud.net:9091'
]

kafka_security_protocol='SASL_SSL'
kafka_sasl_mechanism='SCRAM-SHA-512'
kafka_ssl_cafile='/usr/local/share/ca-certificates/Yandex/YandexInternalRootCA.crt'
kafka_input_topic='inputs'
kafka_output_topic='predictions'


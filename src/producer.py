import time
import random
import json
from pathlib import Path
from typing import Annotated, Generator

import typer
import numpy as np
from numpy.typing import NDArray
from kafka import KafkaProducer # type: ignore

import cfg

def load_data(data_path: Path) -> tuple[NDArray, NDArray]:
  data = np.load(data_path)
  X = data[:, 1:]
  y = data[:, 0]
  return X, y


def unlimited() -> Generator[int, None, None]:
  index = 0            
  while True:
      yield index
      index += 1


def main(data_path: Annotated[Path, typer.Option()] = Path('data/test_data.npy'),
         kafka_user: Annotated[str, typer.Option()] = 'producer',
         kafka_pass: Annotated[str, typer.Option()] = 'cat281983',
         limit: Annotated[int | None, typer.Option()] = None):
  
  X, y = load_data(data_path)
  
  producer = KafkaProducer(
    bootstrap_servers=cfg.kafka_bootstrap_servers,
    security_protocol=cfg.kafka_security_protocol,
    sasl_mechanism=cfg.kafka_sasl_mechanism,
    ssl_cafile=cfg.kafka_ssl_cafile,
    sasl_plain_username=kafka_user,
    sasl_plain_password=kafka_pass,
    value_serializer=lambda m: json.dumps(m).encode('ascii')
  )

  try:
    show_must_go_on = range(limit) if limit is not None and limit > 0 else unlimited()
    
    for _ in show_must_go_on:
      index = random.randint(0, X.shape[0]-1)
      producer.send(
        topic=cfg.kafka_input_topic,
        value={
          'X': X[index].tolist(),
          'y': y[index]
        }
      )

      time.sleep(1)

      print(_)

  finally:
    producer.close()


if __name__ == '__main__':
  typer.run(main)
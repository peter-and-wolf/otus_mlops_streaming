import json
from pathlib import Path
from typing import Annotated
from datetime import datetime

import torch
import typer
import numpy as np
from kafka import KafkaConsumer, KafkaProducer # type: ignore

import cfg
from model import MNISTClassifier


def load_model(model_path: Path) -> MNISTClassifier:
  model = MNISTClassifier()
  model.load_state_dict(
    torch.load(model_path, weights_only=True)
  )
  model.eval()
  
  return model


def predict(model: MNISTClassifier, values: dict) -> tuple[float, float]:
  y = float(values['y'])
  X = torch.Tensor(values['X']).float().reshape(1, 1, 28, 28)
  pred = float(np.argmax(model(X).detach().numpy()))
  return pred, y


def kafka_init(kafka_user: str, kafka_pass: str) -> KafkaConsumer:
  return KafkaConsumer(
    cfg.kafka_input_topic,
    bootstrap_servers=cfg.kafka_bootstrap_servers,
    security_protocol=cfg.kafka_security_protocol,
    sasl_mechanism=cfg.kafka_sasl_mechanism,
    ssl_cafile=cfg.kafka_ssl_cafile,
    sasl_plain_username=kafka_user,
    sasl_plain_password=kafka_pass,
    value_deserializer=lambda m: json.loads(m.decode('ascii')),
    group_id='consume-to-predict'
  )
 

def main(model_path: Annotated[Path, typer.Option()] = Path('data/MNISTClassifier.pt'),
         kafka_user: Annotated[str, typer.Option()] = 'consumer',
         kafka_pass: Annotated[str, typer.Option()] = 'cat281983') -> None:
  
  model = load_model(model_path)

  consumer = kafka_init(kafka_user, kafka_pass)

  try:
    for msg in consumer:
      pred, gt = predict(model, msg.value)
      
      print(f'pred={pred}, gt={gt}')
  finally:
    consumer.close()


if __name__ == '__main__':
  typer.run(main)
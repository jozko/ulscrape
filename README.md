# ulscrape

## Development & tests

```bash
pip install -r requirements.txt -r dev-requirements.txt
python -m unittest test/**/test_*.py -vv
flake8
```

## Docker

```bash
# RabbitMQ (via Docker Compose)
docker-compose -f ./docker-compose.yml up rabbitmq

# Master
docker run -ti --rm -v `pwd`:/home/scrapy/Code --network ulscrape_default \
  --link ulscrape_rabbitmq_1:rabbitmq \
  --entrypoint scrapy jozko/ulscrape crawl uradni-list -a mode=Master
 
# Slave(s)
docker run -ti --rm -v `pwd`:/home/scrapy/Code --network ulscrape_default \
  --link ulscrape_rabbitmq_1:rabbitmq \
  --entrypoint scrapy jozko/ulscrape crawl uradni-list -a mode=Slave
```

## S3

Example with [Minio]:

```
AWS_ENDPOINT_URL='http://a1.univizor.si:9000'
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
S3_FILES_STORE='s3://ulscrape/'
```

## Authors

- [jozko](https://github.com/jozko)
- [otobrglez](https://github.com/otobrglez)

[Minio]: https://github.com/minio/minio

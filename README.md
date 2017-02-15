# ulscrape

## Development & tests

```bash
pip install -r requirements.txt -r dev-requirements.txt
```

```bash
# Tests
python -m unittest test/**/test_*.py -vv
# Linter
flake8
```

## Docker

```bash
# RabbitMQ (via Docker Compose)
docker-compose -f ./docker-compose.yml up rabbitm

# Master
docker run -ti --rm -v `pwd`:/home/scrapy/Code --network ulscrape_default \
  --link ulscrape_rabbitmq_1:rabbitmq \
  --entrypoint scrapy jozko/ulscrape crawl uradni-list -a mode=Master
 
# Slave(s)
docker run -ti --rm -v `pwd`:/home/scrapy/Code --network ulscrape_default \
  --link ulscrape_rabbitmq_1:rabbitmq \
  --entrypoint scrapy jozko/ulscrape crawl uradni-list -a mode=Slave
```

## Authors

- [jozko](https://github.com/jozko)


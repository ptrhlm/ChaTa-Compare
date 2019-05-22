# ChaTa-Compare
> Part of [ChaTa project](chata-url): App for creating plot comparison surveys

[![Maintainability](codeclimate-maint-image)](codeclimate-maint-url)
[![Test Coverage](codeclimate-cov-image)](codeclimate-cov-url)

## Requirements

* Docker
* Docker Compose

## Development setup

Start whole application with:
```bash
docker-compose up
```

After application finishes startup procedure following services will be available:
  - App (http://localhost)
  - API docs (http://localhost:8888/docs, http://localhost:8888/redoc)
  - PGAdmin (http://localhost:5050) - PostgreSQL DB administation
  - Flower (http://localhost:5555) - Celery task queue administration
  - Traefik UI (http://localhost:8090) - routing configuration

## Deployment

TODO

## Release History

* 0.0.1
    * Work in progress

## Acknowledgements

TODO

## Meta

Authors:
- Wiktor Gontarczyk ([@gontarczykw](https://github.com/gontarczykw))
- Piotr Halama ([@ptrhlm](https://github.com/ptrhlm))
- Andrzej Szczesiak ([@quarcom](https://github.com/quarcom))
- Patryk Wróbel

Distributed under the Apache 2.0 license. See ``LICENSE`` for more information.

<!-- Markdown link & img dfn's -->
[chata-url]: https://github.com/mini-pw/2019L-ProjektZespolowy
[codeclimate-maint-image]: https://api.codeclimate.com/v1/badges/649680309ba0d6208981/maintainability
[codeclimate-maint-url]: https://codeclimate.com/github/ptrhlm/ChaTa-Compare/maintainability
[codeclimate-cov-image]: https://api.codeclimate.com/v1/badges/649680309ba0d6208981/test_coverage
[codeclimate-cov-url]: https://codeclimate.com/github/ptrhlm/ChaTa-Compare/test_coverage

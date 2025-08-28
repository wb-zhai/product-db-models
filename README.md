# Overview

This repository has two primary purposes:

- `zhai_db_models`: This provides the SQLAlchemy models for the `zhai_db` database as a reusable Python package
    - This does _not_ include database connection helpers.

- **Alembic migrations**: database schema changes are managed from here using [alembic](https://alembic.sqlalchemy.org/en/latest/). New migrations should be created and applied from here.

#### Installing `zhai_db_models`
```
uv add "git+ssh://git@github.com/wb-zhai/product-db-models.git"
```
or
```
uv add -e <path/to/product-db-models>
```

#### To use
```
from zhai_db_models import Geotaxonomy
```
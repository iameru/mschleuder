some but not all infos

#### poetry

möhrenschleuder recommends `poetry` as a dependency manager.

ms also has some `pre-commits` depending on poetry. they generate requirements.txt and requirements-dev.txt though.

```
poetry update # install
```

ms uses `invoke`. ` invoke --list` to check some tasks build in `tasks.py`.


#### testing

```
invoke test # start testing
invoke failfast # start failfast testing
```

#### database migrations

since this release möhrenschleuder uses `alembic`, wrapped by `flask-migrate`.
workflow, when changing something in the DB is:

```
flask db migrate # to generate the migration pattern
 # check the migration pattern in migration/versions/$VERSION.py
flask db upgrade # to apply changes to database
```

this might be necessary (upgrade) when first starting development on this.

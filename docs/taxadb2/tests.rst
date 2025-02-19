.. _tests:


Testing Taxadb
==============

**Note:** Relies on the `pytest` module. `pip install pytest`

You can easily run some tests. Go to the root directory of this projects `cd /path/to/taxadb2` and run
`pytest -v`.

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb2/test`
directory.

.. code-block:: bash

    pytest -v

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb2/test`
directory.

It is also possible to only run tests related to accessionid or taxid as follow

.. code-block:: bash

   pytest -m 'taxid'
   pytest -m 'accessionid'

You can also use the configuration file located in root distribution `taxadb.ini` as follow. This file should contains
database connection settings:

.. code-block:: bash

   pytest taxadb2/test --config='taxadb2.ini'


Running tests against PostgreSQL or MySQL
-----------------------------------------

**Note:** The part `PostgreSQL` and/or `MySQL` was not tested as compared to the original implementation `taxadb <https://github.com/HadrienG/taxadb>`_, but might still work as expected.

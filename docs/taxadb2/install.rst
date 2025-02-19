.. _install:

Installing Taxadb2
==================

Taxadb2 requires :code:`python >= 3.10` to work. Taxadb2 can work with `SQLite`, `PostgreSQL` and `MySQL`.
By default Taxadb2 works with `SQLite` as it comes with modern Python distributions.

.. _using_pip:

Using pip
---------

To install taxadb2, simply type one of the following in a terminal:

.. code-block:: bash

    pip install taxadb2

Installing taxadb2 with `PostgreSQL` and/or `MySQL` support

**Note:** The part `PostgreSQL` and/or `MySQL` was not tested as compared to the original implementation `taxadb <https://github.com/HadrienG/taxadb>`_, but might still work as expected.

.. code-block:: bash

    pip install .[postgres, mysql] taxadb2

This should install `psycopg2` and `PyMySQL` Python packages

For testing:

.. code-block:: bash

    pip install .[test] taxadb2

.. _from_gitub:

From github
-----------

If you wish to install taxadb2 from github, you can do the following

.. code-block:: bash

    git clone https://github.com/kullrich/taxadb2.git
    cd taxadb2
    pip install .

Installing taxadb2 for `PostgreSQL` and/or `MySQL`

.. code-block:: bash

    git clone https://github.com/kullrich/taxadb2.git
    cd taxadb2
    pip install psycopg2 PyMySQL
    pip install .

Installing taxadb2 with testing

.. code-block:: bash

    git clone https://github.com/kullrich/taxadb2.git
    cd taxadb2
    pip install pytest
    pip install .

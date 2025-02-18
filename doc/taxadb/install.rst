.. _install:

Installing Taxadb2
=================

Taxadb2 requires :code:`python >= 3.10` to work. Taxadb can work with `SQLite`, `PostgreSQL` and `MySQL`. By default Taxadb2
works with `SQLite` as it comes with modern Python distributions.

.. _using_pip:

Using pip
---------

To install taxadb2, simply type one of the following in a terminal:

.. code-block:: bash

    pip install taxadb2

Installing taxadb2 with `PostgreSQL` and/or `MySQL` support

.. code-block:: bash

    pip install .[postgres, mysql] taxadb2

This should install `psycopg2` and `PyMySQL` Python packages

.. _from_gitub:

From github
-----------

If you wish to install taxadb2 from github, you can do the following

.. code-block:: bash

    git clone https://github.com/kullrich/taxadb2.git
    cd taxadb2
    python setup.py install

Installing Taxadb for `PostgreSQL` and/or `MySQL`

.. code-block:: bash

    git clone https://github.com/kullrich/taxadb2.git
    cd taxadb2
    pip install psycopg2 PyMySQL
    python setup.py install

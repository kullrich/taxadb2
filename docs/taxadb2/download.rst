.. _download:

Create a database
=================

.. _build_own_databases:

Build you own database
----------------------

In order to create your own database, you first need to download the required data from
the ncbi ftp. The following command does it for you:

.. code-block:: bash

   taxadb2 download --outdir taxadb --type taxa

where :code:`--outdir` refers to an output directory where to download the data.


.. _using_sqlite:

SQLite
^^^^^^

The following command will create an **SQLite** database in the current directory.

.. code-block:: bash

   taxadb2 create --division taxa --input taxadb --dbname taxadb.sqlite

.. _using_mysql:

MySQL
^^^^^

Note: This part was not tested as compared to the original implementation `taxadb <https://github.com/HadrienG/taxadb>`

Creating databases is a very vendor specific task. **Peewee**, as most ORMs, can create tables but not databases.
In order to use taxadb with **MySQL**, you'll have to create the database yourself.

.. code-block:: bash

   mysql -u $user -p
   mysql> CREATE DATABASE taxadb;

Then, fill database with data

.. code-block:: bash

   taxadb2 create -i taxadb --dbname taxadb --dbtype mysql --username user --password secret --port 3306 --hostname localhost

.. _using_postgres:

PostgreSQL
^^^^^^^^^^

Note: This part was not tested as compared to the original implementation `taxadb <https://github.com/HadrienG/taxadb>`

Creating databases is a very vendor specific task. **Peewee**, as most ORMs, can create tables but not databases.
In order to use taxadb with **PostgreSQL**, you'll have to create the database yourself.

.. code-block:: bash

   psql -U $user -d postgres
   psql> CREATE DATABASE taxadb;

Then, fill database with data

.. code-block:: bash

   taxadb2 create -i taxadb --dbname taxadb --dbtype postgres --username user --password secret --port 5432 --hostname localhost


The following options have default value if not set on the command line:

* :code:`--port` (:code:`5432` for **PostgreSQL**, :code:`3306` for **MySQL**)
* :code:`--hostname` (localhost)

For more information about all the available options, please type:

.. code-block:: bash

   taxadb2 create --help

.. warning::

   When building your database with downloaded data, you can increase the speed
   of data loading by using --fast option. This option avoid checking existence
   of each accession id in the database before loading related info. In certain
   case this may lead to duplicate entries in table accession when loading
   the same file twice for example.

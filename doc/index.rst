.. taxadb2 documentation master file, created by
   sphinx-quickstart on Thu Mar 1 19:09:27 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Taxadb2
======

Taxadb2 is an application to locally query the ncbi taxonomy.

Taxadb2 is a fork from `https://github.com/HadrienG/taxadb <https://github.com/HadrienG/taxadb>` and handles the merged.dmp ncbi taxonomy file to deal with updated taxIDs.

Taxadb2 is written in python, and access its database using
the `peewee <http://peewee.readthedocs.io>`_ library.

.. .. image:: biobook_taxonomy_graphik_6.png
..    :scale: 50
..
.. ..   :height: 246
.. ..   :width: 200

In brief Taxadb2:

* is a small tool to query the `ncbi <https://ncbi.nlm.nih.gov/taxonomy>`_ taxonomy.
* is written in python >= 3.10.
* has built-in support for `SQLite <https://www.sqlite.org>`_, `MySQL <https://www.mysql.com>`_ and
  `PostgreSQL <https://www.postgresql.org>`_.
* has available pre-built SQLite databases (:ref:`Download build databases <download>`).
* has a comprehensive :ref:`API documentation <api>`.
* is actively being developed on `GitHub <https://github.com/kullrich/taxadb2.git>`_ and available under the MIT license. Please see the `README <https://github.com/kullrich/taxadb2>`_ for more information on development, support, and contributing.

Quickstart
----------

Click on the images below to access the documentation for creating the database with the engine you wish to use:

.. image:: img/postgresql.png
    :target: taxadb2/download.html#using-postgres
    :alt: postgresql

.. image:: img/mysql.png
    :target: taxadb2/download.html#using-mysql
    :alt: mysql

.. image:: img/sqlite.png
    :target: taxadb2/download.html#using-sqlite
    :alt: sqlite

* :ref:`Installation guide <install>` explains how to install Taxadb2.
* :ref:`Download or build data <download>` explains how to build Taxadb2 database(s).
* :ref:`Test the application <tests>` allows to run several tests for supported databases.
* :ref:`Querying taxadb <query>` shows examples on how to query a Taxadb database.
* :ref:`API reference <api>` describes available classes and methods to use Taxadb.


Contents
---------

.. toctree::
   :maxdepth: 2
   :glob:

   taxadb2/install
   taxadb2/download
   taxadb2/tests
   taxadb2/query
   taxadb2/api

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. |date| date::
.. |time| date:: %H:%M

*This documentation was generated on* |date| *at* |time|.

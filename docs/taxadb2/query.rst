.. _query:


Querying the database
=====================

Firstly make sure you have :ref:`downloaded <download>` and :ref:`built <build_own_databases>` the database.

Below you can find basic examples. For more complex examples, please refer to the complete :ref:`documentation <api>`.

.. _taxids:

taxids
------

Several operations on taxids are available in taxadb:

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname='taxadb.sqlite'),
    >>>    'names': SciName(dbtype='sqlite', dbname='taxadb.sqlite')
    >>> }

    >>> taxid2name = ncbi['taxid'].sci_name(7955)
    >>> print(taxid2name)
    Danio rerio
    >>> lineage = ncbi['taxid'].lineage_name(7955)
    >>> print(lineage[:5])
    ['Danio rerio', 'Danio', 'Danioninae', 'Danionidae', 'Cyprinoidei']
    >>> lineage = ncbi['taxid'].lineage_name(7955, reverse=True)
    >>> print(lineage[:5])
    ['cellular organisms', 'Eukaryota', 'Opisthokonta', 'Metazoa', 'Eumetazoa']

    >>> ncbi['taxid'].has_parent(33208, 'Eukaryota')
    True

You can also get the taxid from the scientific name

Get the taxid from a scientific name.

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname='taxadb.sqlite'),
    >>>    'names': SciName(dbtype='sqlite', dbname='taxadb.sqlite')
    >>> }
    
    >>> name2taxid = ncbi['names'].taxid('Metazoa')
    >>> print(name2taxid)
    33208

Automatic detection of old taxIDs imported from merged.dmp.

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname='taxadb.sqlite'),
    >>>    'names': SciName(dbtype='sqlite', dbname='taxadb.sqlite')
    >>> }

    >>> taxid2name = ncbi['taxid'].sci_name(1240228)
    TaxID 1240228 is deprecated, using 8855 instead.
    >>> print(taxid2name)
    Cairina moschata

If you are using MySQL or postgres, you'll have to provide your username and password
(and optionally the port and hostname):

.. code-block:: python

    >>> from taxadb2.taxid import TaxID

    >>> taxid = TaxID(dbype='postgres', dbname='taxadb',
                        username='taxadb', password='*****')
    >>> name = taxid.sci_name(33208)
    >>> print(name)
    Metazoa

.. _accessions:

accession numbers
-----------------

Get taxonomic information from accession number(s).

.. code-block:: python

   >>> from taxadb2.accessionid import AccessionID

   >>> my_accessions = ['X17276', 'Z12029']
   >>> accession = AccessionID(dbtype='sqlite', dbname='taxadb.sqlite')
   >>> taxids = accession.taxid(my_accessions)
   >>> taxids
   <generator object taxid at 0x1051b0830>

   >>> for tax in taxids:
           print(tax)
   ('X17276', 9646)
   ('Z12029', 9915)

.. _useconfig:

Using configuration file or environment variable
------------------------------------------------

Note: This part was not tested as compared to the original implementation `taxadb <https://github.com/HadrienG/taxadb>`

Taxadb2 can now take profit of configuration file or environment variable to
set database connection parameters.

* Using configuration file

You can pass a configuration file when building your object:

.. code-block:: python

   >>> from taxadb2.taxid import TaxID

   >>> taxid = TaxID(config='/path/to/taxadb2.cfg')
   >>> name = taxid.sci_name(33208)
   >>> ...

* Configuration file format

The configuration file must use syntax supported by `configparser object
<https://docs.python.org/3.10/library/configparser.html>`_.
You must set database connection parameters in a section called
:code:`DBSETTINGS` as below:

.. code-block:: bash

   [DBSETTINGS]
   dbtype=<sqlite|postgres|mysql>
   dbname=taxadb
   hostname=
   username=
   password=
   port=

Some value will default it they are not set.

**hostname** will be set to value :code:`localhost` and **port** is set to
:code:`5432` for :code:`dbtype=postgres` and :code:`3306` for
:code:`dbtype=mysql`.

* Using environment variable

Taxadb can as well use an environment variable to automatically point the
application to a configuration file. To take profit of it, just set
:code:`TAXADB2_CONFIG` to the path of your configuration file:

.. code-block:: bash

   (bash) export TAXADB2_CONFIG='/path/to/taxadb2.cfg'
   (csh) set TAXADB2_CONFIG='/path/to/taxadb2.cfg'

Then, just create your object as follow:

.. code-block:: python

   >>> from taxadb2.taxid import TaxID

   >>> taxid = Taxid()
   >>> name = taxid.sci_name(33208)
   >>> ...

.. note::

   Arguments passed to object initiation will always overwrite default values
   as well as values that might have been set by configuration file or
   environment variable :code:`TAXADB2_CONFIG`.

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
    >>> from taxadb2.accessionid import AccessionID
    >>> dbname = "taxadb2/test/test_db.sqlite"
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname=dbname),
    >>>    'names': SciName(dbtype='sqlite', dbname=dbname),
    >>>    'accessionid': AccessionID(dbtype='sqlite', dbname=dbname)
    >>> }

    >>> taxid2name = ncbi['taxid'].sci_name(2)
    >>> print(taxid2name)
    Bacteria
    >>> lineage = ncbi['taxid'].lineage_name(17)
    >>> print(lineage[:5])
    ['Methylophilus methylotrophus', 'Methylophilus', 'Methylophilaceae', 'Nitrosomonadales', 'Betaproteobacteria']
    >>> lineage = ncbi['taxid'].lineage_name(17, reverse=True)
    >>> print(lineage[:5])
    ['cellular organisms', 'Bacteria', 'Pseudomonadati', 'Pseudomonadota', 'Betaproteobacteria']

    >>> ncbi['taxid'].has_parent(17, 'Bacteria')
    True

You can also get the taxid from the scientific name

Get the taxid from a scientific name.

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> from taxadb2.accessionid import AccessionID
    >>> dbname = "taxadb2/test/test_db.sqlite"
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname=dbname),
    >>>    'names': SciName(dbtype='sqlite', dbname=dbname),
    >>>    'accessionid': AccessionID(dbtype='sqlite', dbname=dbname)
    >>> }
    
    >>> name2taxid = ncbi['names'].taxid('Pseudomonadota')
    >>> print(name2taxid)
    1224

Automatic detection of old taxIDs imported from merged.dmp.

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> from taxadb2.accessionid import AccessionID
    >>> dbname = "taxadb2/test/test_db.sqlite"
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname=dbname),
    >>>    'names': SciName(dbtype='sqlite', dbname=dbname),
    >>>    'accessionid': AccessionID(dbtype='sqlite', dbname=dbname)
    >>> }

    >>> taxid2name = ncbi['taxid'].sci_name(30)
    TaxID 30 is deprecated, using 29 instead.
    >>> print(taxid2name)
    Myxococcales

If you are using MySQL or postgres, you'll have to provide your username and password
(and optionally the port and hostname):

.. code-block:: python

    >>> from taxadb2.taxid import TaxID

    >>> taxid = TaxID(dbype='postgres', dbname='taxadb',
                        username='taxadb', password='*****')
    >>> name = taxid.sci_name(2)
    >>> print(name)
    Bacteria

.. _accessions:

accession numbers
-----------------

Get taxonomic information from accession number(s).

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> from taxadb2.accessionid import AccessionID
    >>> dbname = "taxadb2/test/test_db.sqlite"
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname=dbname),
    >>>    'names': SciName(dbtype='sqlite', dbname=dbname),
    >>>    'accessionid': AccessionID(dbtype='sqlite', dbname=dbname)
    >>> }

    >>> my_accessions = ['A01460']
    >>> taxids = ncbi['accessionid'].taxid(my_accessions)
    >>> taxids
    <generator object AccessionID.taxid at 0x103e21bd0>
    >>> for ti in taxids:
        print(ti)
    ('A01460', 17)

.. _useconfig:

Using configuration file or environment variable
------------------------------------------------

**Note:** This part was only tested sporadically as compared to the original implementation `taxadb <https://github.com/HadrienG/taxadb>`_

Taxadb2 can now take profit of configuration file or environment variable to
set database connection parameters.

* Using configuration file

You can pass a configuration file when building your object:

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> from taxadb2.accessionid import AccessionID
    >>> config_path = "taxadb2/test/taxadb2.cfg"
    >>> ncbi = {
    >>>    'taxid': TaxID(config=config_path),
    >>>    'names': SciName(config=config_path),
    >>>    'accessionid': AccessionID(config=config_path)
    >>> }

    >>> ncbi['taxid'].sci_name(2)
    Bacteria
    >>> ...

* Configuration file format

The configuration file must use syntax supported by `configparser object
<https://docs.python.org/3.10/library/configparser.html>`_.
You must set database connection parameters in a section called
:code:`DBSETTINGS` as below:

Here you can see one example using `sql`

.. code-block:: bash

    [sql]
    dbname=taxadb2/test/test_db.sqlite
    username=
    password=
    hostname=
    port=
    dbtype=sqlite

Some value will default it they are not set.

**hostname** will be set to value :code:`localhost` and **port** is set to
:code:`5432` for :code:`dbtype=postgres` and :code:`3306` for
:code:`dbtype=mysql`.

* Using environment variable

Taxadb2 can as well use an environment variable to automatically point the
application to a configuration file. To take profit of it, just set
:code:`TAXADB2_CONFIG` to the path of your configuration file:

.. code-block:: bash

   (bash) export TAXADB2_CONFIG='taxadb2/test/taxadb2.cfg'
   (csh) set TAXADB2_CONFIG='taxadb2/test/taxadb2.cfg'

Then, just create your object as follow:

.. code-block:: python

    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> from taxadb2.accessionid import AccessionID
    >>> ncbi = {
    >>>    'taxid': TaxID(),
    >>>    'names': SciName(),
    >>>    'accessionid': AccessionID()
    >>> }

    >>> ncbi['taxid'].sci_name(2)
    Bacteria
    >>> ...

.. note::

   Arguments passed to object initiation will always overwrite default values
   as well as values that might have been set by configuration file or
   environment variable :code:`TAXADB2_CONFIG`.

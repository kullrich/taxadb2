# Taxadb2

[![Documentation Status](https://readthedocs.org/projects/taxadb2/badge/?version=latest)](http://taxadb.readthedocs.io/en/latest/?badge=latest)
[![made-with-python](https://img.shields.io/badge/made%20with-python3-blue.svg)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/taxadb2.svg)](https://pypi.org/project/taxadb2/)
[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/kullrich/taxadb2)

Taxadb2 is an application to locally query the ncbi taxonomy. Taxadb2 is written in python, and access its database using the [peewee](http://peewee.readthedocs.io) library.

Taxadb2 is a fork from [https://github.com/HadrienG/taxadb](https://github.com/HadrienG/taxadb) and handles the `merged.dmp` ncbi taxonomy file to deal with updated taxIDs.

* the built-in support for [MySQL](https://www.mysql.com) and [PostgreSQL](https://www.postgresql.org) was not touched and kept as it is
* `merged.dmp` support was added

In brief Taxadb2:

* is a small tool to query the [ncbi](https://ncbi.nlm.nih.gov/taxonomy) taxonomy.
* is written in python >= 3.10.
* has built-in support for [SQLite](https://www.sqlite.org), [MySQL](https://www.mysql.com) and [PostgreSQL](https://www.postgresql.org).
* has available pre-built SQLite databases.
* has a comprehensive API documentation.


## Installation

Taxadb2 requires python >= 3.10 to work. To install taxadb2 with sqlite support, simply type the following in your terminal:

    pip3 install taxadb2

If you wish to use MySQL or PostgreSQL, please refer to the full [documentation](http://taxadb2.readthedocs.io/en/latest/)

## Usage

### Querying the Database

Firstly, make sure you have [built](#creating-the-database) the database

Below you can find basic examples. For more complete examples, please refer to the complete [API documentation](http://taxadb2.readthedocs.io/en/latest/)

```python
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
```

Get the taxid from a scientific name.

```python
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
```

Automatic detection of `old` taxIDs imported from `merged.dmp`.


```python
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
```

Get the taxonomic information for accession number(s).

```python
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
```

You can also use a configuration file in order to automatically set database connection parameters at object build. Either set config parameter to __init__ object method:

```python
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
```

or set environment variable TAXADB_CONFIG which point to configuration file:

```bash
    $ export TAXADB2_CONFIG='taxadb2/test/taxadb2.cfg'
```

```python
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
```

Check documentation for more information.

### Creating the Database

#### Download data

The following commands will download the necessary files from the [ncbi ftp](https://ftp.ncbi.nlm.nih.gov/) into the directory `taxadb`.
```
$ taxadb2 download --outdir taxadb --type taxa
```

#### Insert data

##### SQLite

```
$ taxadb2 create --division taxa --input taxadb --dbname taxadb.sqlite
```
You can then safely remove the downloaded files
```
$ rm -r taxadb
```

You can easily rerun the same command, `taxadb2` is able to skip already inserted `taxid` as well as `accession`.

## Tests

**Note:** Relies on the `pytest` module. `pip install pytest`

You can easily run some tests. Go to the root directory of this projects `cd /path/to/taxadb2` and run
`pytest -v`.

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb2/test`
directory.

It is also possible to only run tests related to accessionid or taxid as follow
```
$ pytest -m 'taxid'
$ pytest -m 'accessionid'
```

You can also use the configuration file located in root distribution `taxadb2.ini` as follow. This file should contain
database connection settings:
```
$ pytest taxadb2/test --config='taxadb2.ini'
```

## License

Code is under the [MIT](LICENSE) license.

## Issues

Found a bug or have a question? Please open an [issue](https://github.com/kullrich/taxadb2/issues)

## Contributing

Thought about a new feature that you'd like us to implement? Open an [issue](https://github.com/kullrich/taxadb2/issues) or fork the repository and submit a [pull request](https://github.com/kullrich/taxadb2/pulls)

## Code of Conduct - Participation guidelines

This repository adhere to [Contributor Covenant](http://contributor-covenant.org) code of conduct for in any interactions you have within this project. (see [Code of Conduct](https://github.com/kullrich/taxadb2/blob/devel/CODE_OF_CONDUCT.md))

See also the policy against sexualized discrimination, harassment and violence for the Max Planck Society [Code-of-Conduct](https://www.mpg.de/11961177/code-of-conduct-en.pdf).

By contributing to this project, you agree to abide by its terms.

## References

https://github.com/HadrienG/taxadb


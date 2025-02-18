# Taxadb2

[![Documentation Status](https://readthedocs.org/projects/taxadb2/badge/?version=latest)](http://taxadb.readthedocs.io/en/latest/?badge=latest)
[![made-with-python](https://img.shields.io/badge/made%20with-python3-blue.svg)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/taxadb2.svg)](https://pypi.org/project/taxadb2/)
[![LICENSE](https://img.shields.io/badge/license-MIT-lightgrey.svg)](https://github.com/kullrich/taxadb2)

Taxadb2 is an application to locally query the ncbi taxonomy. Taxadb is written in python, and access its database using the [peewee](http://peewee.readthedocs.io) library.

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
```

Get the taxid from a scientific name.

```python
    >>> from taxadb2.taxid import TaxID
    >>> from taxadb2.names import SciName
    >>> ncbi = {
    >>>    'taxid': TaxID(dbtype='sqlite', dbname='taxadb.sqlite'),
    >>>    'names': SciName(dbtype='sqlite', dbname='taxadb.sqlite')
    >>> }
    
    >>> name2taxid = ncbi['names'].taxid('Metazoa')
    >>> print(name2taxid)
    33208
```

Automatic detection of `old` taxIDs imported from `merged.dmp`.


```python
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

You can easily rerun the same command, `taxadb` is able to skip already inserted `taxid` as well as `accession`.

## Tests

You can easily run some tests. Go to the root directory of this projects `cd /path/to/taxadb2` and run
`nosetests`.

This simple command will run tests against an `SQLite` test database called `test_db.sqlite` located in `taxadb/test`
directory.

It is also possible to only run tests related to accessionid or taxid as follow
```
$ nosetests -a 'taxid'
$ nosetests -a 'accessionid'
```

You can also use the configuration file located in root distribution `taxadb2.ini` as follow. This file should contains
database connection settings:
```
$ nosetests --tc-file taxadb2.ini
```

You can easily override configuration file settings using command line options `--tc` such as:
```
$ nosetest --tc-file taxadb2.ini --tc=sql.dbname:another_dbname
```

More info at [nose-testconfig](https://pypi.python.org/pypi/nose-testconfig)

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

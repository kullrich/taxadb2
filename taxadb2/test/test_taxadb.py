#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import unittest
import pytest

from taxadb2.taxid import TaxID
from taxadb2.names import SciName
from taxadb2.taxadb import TaxaDB
from taxadb2.util import md5_check
from taxadb2.schema import Taxa, Accession, DeprecatedTaxID
from taxadb2.accessionid import AccessionID
from taxadb2.parser import TaxaParser, TaxaDumpParser, Accession2TaxidParser

from testconfig import config


class TestMainFunc(unittest.TestCase):
    """Class to test global methods"""

    def test_max_limit_exceeded(self):
        """Check max length of ids raises an exception"""
        ids = [i for i in range(1, 1001)]
        with self.assertRaises(SystemExit):
            TaxaDB.check_list_ids(ids)

    def test_max_limit_ok(self):
        ids = [i for i in range(1, 90)]
        self.assertTrue(TaxaDB.check_list_ids(ids))

    def test_wrong_dbtype(self):
        """Check wrong dbtype raises an exception"""
        with self.assertRaises(SystemExit):
            TaxaDB(dbtype='fake')


class TestUtils(unittest.TestCase):
    """Class to test taxadb2.util"""

    @pytest.mark.util
    def test_md5check_success(self):
        """Check md5 is ok"""
        okfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              'good.txt')
        self.assertIsNone(md5_check(okfile))

    @pytest.mark.util
    def test_md5check_fails(self):
        """Check md5 fails"""
        badfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'wrong.txt')
        with self.assertRaises(SystemExit):
            md5_check(badfile)


class TestTaxadb(unittest.TestCase):
    """Main class to test AccessionID and TaxID method with sqlite"""

    def setUp(self):
        # Set attributes
        self.dbtype = None
        self.username = None
        self.password = None
        self.hostname = None
        self.port = None
        self.dbname = None
        self.testdir = os.path.dirname(os.path.realpath(__file__))
        self.back_env = None

        # If config does not contains key sql, it means no config file passed
        #  on command line
        # so we default to sqlite test
        if 'sql' not in config:
            config['sql'] = {'dbtype': 'sqlite',
                             'dbname': 'taxadb2/test/test_db.sqlite'}

        self.dbtype = config['sql']['dbtype']
        # Defaults to sqlite
        if self.dbtype is None or self.dbtype == '':
            self.dbtype = 'sqlite'
        if self.dbtype not in ['postgres', 'mysql', 'sqlite']:
            self.fail("dbtype option %s not supported" % str(self.dbtype))

        self.dbname = config['sql']['dbname']
        # Defaults to sqlite test database
        if self.dbname is None or self.dbname == '':
            self.dbname = 'taxadb/test/test_db.sqlite'

        if 'username' in config['sql'] \
                and config['sql']['username'] is not None:
            self.username = config['sql']['username']
        if 'password' in config['sql'] \
                and config['sql']['password'] is not None:
            self.password = config['sql']['password']
        if 'hostname' in config['sql'] \
                and config['sql']['hostname'] is not None:
            self.hostname = config['sql']['hostname']
        if 'port' in config['sql'] and config['sql']['port']:
            self.port = int(config['sql']['port'])
        self._unset_user_env()

    def tearDown(self):
        """Remove previously stuff set"""
        self._set_config_back()

    def _buildTaxaDBObject(self, obj):
        sql = obj(dbname=self.dbname, dbtype=self.dbtype,
                  username=self.username, password=self.password,
                  hostname=self.hostname, port=self.port)
        return sql

    def _unset_user_env(self):
        """If user has set TAXADB2_CONFIG we remove it for our tests"""
        if os.environ.get('TAXADB2_CONFIG') is not None:
            del os.environ['TAXADB2_CONFIG']

    def _set_config_from_envvar(self):
        """Set configuration, from config file and set env variable"""
        cfg = os.path.join(self.testdir, 'taxadb2.cfg')
        if not os.path.exists(cfg):
            raise Exception("Can't find taxadb2.cfg %s" % str(cfg))
        if os.environ.get('TAXADB2_CONFIG') is not None:
            self.back_env = os.environ.get('TAXADB2_CONFIG')
            del os.environ['TAXADB2_CONFIG']
        os.environ['TAXADB2_CONFIG'] = cfg

    def _set_config_back(self):
        """Remove env variable"""
        if self.back_env is not None:
            os.environ['TAXADB2_CONFIG'] = self.back_env
            self.back_env = None
        return self.back_env

    @pytest.mark.schema
    def test_table_exists_ok(self):
        """Check the method return True when checking ofr existsing table"""
        obj = self._buildTaxaDBObject(TaxaDB)
        self.assertTrue(obj.check_table_exists(Accession))
        self.assertTrue(obj.check_table_exists(Taxa))

    @pytest.mark.schema
    def test_table_exists_failed(self):
        """Check the method throws SystemExit if a table does not exist"""
        from taxadb2.schema import BaseModel
        import peewee as pw

        class NotFound(BaseModel):
            id = pw.IntegerField(null=False)
            name = pw.CharField()
        obj = self._buildTaxaDBObject(TaxaDB)
        with self.assertRaises(SystemExit):
            obj.check_table_exists(NotFound)

    @pytest.mark.schema
    def test_has_index(self):
        """Check method returns False and True when either table or index
        does not exist"""
        from taxadb2.schema import BaseModel
        import peewee as pw

        class FooBar(BaseModel):
            id = pw.IntegerField(null=False)
            name = pw.CharField()

        idx = FooBar.index(FooBar.name, name='name')
        FooBar.add_index(idx)
        obj = self._buildTaxaDBObject(TaxaDB)
        # Test returns False
        self.assertFalse(FooBar.has_index(name='foo'))
        FooBar.create_table(fail_silently=True)
        self.assertFalse(FooBar.has_index(name='foo'))
        self.assertFalse(FooBar.has_index())
        self.assertFalse(FooBar.has_index(columns=10))
        # Test returns True
        self.assertTrue(FooBar.has_index(name='name'))
        FooBar.drop_table()

    @pytest.mark.config
    def test_setconfig_from_envvar(self):
        """Check using configuration from environment variable is ok"""
        self._set_config_from_envvar()
        db = AccessionID()
        self.assertEqual(db.get('dbname'), 'taxadb2/test/test_db.sqlite')
        self.assertEqual(db.get('dbtype'), 'sqlite')

    @pytest.mark.config
    def test_setconfig_nodbname_raises(self):
        """Check method raises SystemExit when no dbname set"""
        with self.assertRaises(SystemExit):
            AccessionID(dbtype='sqlite')

    @pytest.mark.config
    def test_setconfig_from_configfile(self):
        """Check passing a configuration file is ok"""
        db = AccessionID(config=os.path.join(self.testdir, 'taxadb2.cfg'))
        self.assertEqual(db.get('dbname'), 'taxadb/test/test_db.sqlite')
        self.assertEqual(db.get('dbtype'), 'sqlite')

    @pytest.mark.config
    def test_set_args(self):
        """Check we can set config from dict as args"""
        db = AccessionID(dbtype='sqlite',
                         dbname=os.path.join(self.testdir, 'test_db.sqlite'))
        self.assertEqual(db.get('dbtype'), 'sqlite')
        self.assertEqual(os.path.basename(db.get('dbname')), 'test_db.sqlite')

    @pytest.mark.config
    def test_set_config_with_wrong_section(self):
        """Check we catch exception by using config file with wrong section"""
        with self.assertRaises(SystemExit):
            AccessionID(config=os.path.join(self.testdir,
                                            'taxadb-nosection.cfg'))

    @pytest.mark.config
    def test_get_config_nooption(self):
        """Check get method returns None when an option is not found in the
        configuration file"""
        db = AccessionID(config=os.path.join(self.testdir, 'taxadb2.cfg'))
        self.assertIsNone(db.get('unknown'))

    @pytest.mark.config
    def test_get_config_returnsNone(self):
        """Check get method returns None when an option has no value in
        configuration file"""
        db = AccessionID(config=os.path.join(self.testdir, 'taxadb2.cfg'))
        db.set('foobar', None)
        self.assertIsNone(db.get('foobar'))

    @pytest.mark.config
    def test_set_config_option_unset_section(self):
        """Check set throws AttributeError as required section for settings
        option is not defined yet"""
        db = AccessionID(config=os.path.join(self.testdir, 'taxadb2.cfg'))
        with self.assertRaises(AttributeError):
            db.set('newoption', 'newvalue', section="UNSET_SECCTION")

    @pytest.mark.getdb
    def test_getdatabase_nouser_or_nopasswd(self):
        """Check get_database throws SystemExit when no user or no password
         is set"""
        with self.assertRaises(SystemExit):
            AccessionID(dbname='taxadb', dbtype='mysql')

    @pytest.mark.getdb
    def test_getdatabase_mysql_nohostname_noport_setdefault(self):
        """Check get_database set default hostname and port for MySQL"""
        try:
            db = AccessionID(dbname='taxadb', dbtype='mysql',
                             password="123",
                             username="admin")
            self.assertEqual(int(db.get('port')), 3306)
            self.assertEqual(db.get('hostname'), 'localhost')
        except SystemExit as err:
            unittest.skip("Can't test function: %s" % str(err))

    @pytest.mark.getdb
    def test_getdatabase_postgres_nohostname_noport_setdefault(self):
        """Check get_database set default hostname and port for MySQL"""
        try:
            db = AccessionID(dbname='taxadb', dbtype='postgres',
                             password="admin",
                             username="admin")
            self.assertEqual(int(db.get('port')), 5432)
            self.assertEqual(db.get('hostname'), 'localhost')
        except SystemExit as err:
            unittest.skip("Can't test function: %s" % str(err))

    @pytest.mark.getdb
    def test_getdatabase_sqlite_throws(self):
        """Check get_database throws SystemExit when wrong or inaccessible
         db"""
        with self.assertRaises(SystemExit):
            db = AccessionID(dbname='/unaccessible', dbtype='sqlite')

    @pytest.mark.accessionid
    def test_accession_taxid(self):
        """Check the method get the correct taxid for a given accession id"""
        accession = self._buildTaxaDBObject(AccessionID)
        taxids = accession.taxid(['A01460'])
        for taxon in taxids:
            self.assertEqual(taxon[0], 'A01460')
            self.assertEqual(taxon[1], 17)

    @pytest.mark.accessionid
    def test_accesion_taxid_null(self):
        """Check method generator throws StopIteration, no results found"""
        accession = self._buildTaxaDBObject(AccessionID)
        taxids = accession.taxid(['111111'])
        with self.assertRaises(StopIteration):
            taxids.__next__()

    @pytest.mark.accessionid
    def test_accession_sci_name(self):
        accession = self._buildTaxaDBObject(AccessionID)
        sci_name = accession.sci_name(['A01462'])
        for taxon in sci_name:
            self.assertEqual(taxon[0], 'Z12029')
            self.assertEqual(taxon[1], 'Methylophilus methylotrophus')

    @pytest.mark.accessionid
    def test_accesion_sci_name_null(self):
        """Check method generator throws StopIteration, no results found"""
        accession = self._buildTaxaDBObject(AccessionID)
        taxids = accession.sci_name(['111111'])
        with self.assertRaises(StopIteration):
            taxids.__next__()

    @pytest.mark.accessionid
    def test_accession_lineage_id(self):
        accession = self._buildTaxaDBObject(AccessionID)
        lineage_id = accession. (['X52702'])
        for taxon in lineage_id:
            self.assertEqual(taxon[0], 'X52702')
            self.assertListEqual(taxon[1], [
                9771, 9766, 9765, 9761, 9721, 91561, 314145, 1437010, 9347,
                32525, 40674, 32524, 32523, 1338369, 8287, 117571, 117570,
                7776, 7742, 89593, 7711, 33511, 33213, 6072, 33208, 33154,
                2759, 131567])

    @pytest.mark.acccesionid
    def test_accesion_lineage_id_null(self):
        """Check method generator throws StopIteration, no results found"""
        accession = self._buildTaxaDBObject(AccessionID)
        taxids = accession.sci_name(['111111'])
        with self.assertRaises(StopIteration):
            taxids.__next__()

    @pytest.mark.accessionid
    def test_accession_lineage_name(self):
        accession = self._buildTaxaDBObject(AccessionID)
        lineage_name = accession.lineage_name(['X60065'])
        for taxon in lineage_name:
            self.assertEqual(taxon[0], 'X60065')
            self.assertListEqual(taxon[1], [
                'Bos taurus', 'Bos', 'Bovinae', 'Bovidae', 'Pecora',
                'Ruminantia', 'Cetartiodactyla', 'Laurasiatheria',
                'Boreoeutheria', 'Eutheria', 'Theria', 'Mammalia', 'Amniota',
                'Tetrapoda', 'Dipnotetrapodomorpha', 'Sarcopterygii',
                'Euteleostomi', 'Teleostomi', 'Gnathostomata', 'Vertebrata',
                'Craniata', 'Chordata', 'Deuterostomia', 'Bilateria',
                'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota',
                'cellular organisms'])

    @pytest.mark.accessionid
    def test_accesion_lineage_name_null(self):
        """Check method generator throws StopIteration, no results found"""
        accession = self._buildTaxaDBObject(AccessionID)
        taxids = accession.lineage_name(['111111'])
        with self.assertRaises(StopIteration):
            taxids.__next__()

    @pytest.mark.taxid
    def test_taxid_sci_name(self):
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.sci_name(1706371)
        self.assertEqual(name, 'Cellvibrio')

    @pytest.mark.taxid
    def test_sci_name_taxid(self):
        name = self._buildTaxaDBObject(SciName)
        taxid = name.taxid('Cellvibrio')
        self.assertEqual(taxid, 1706371)

    @pytest.mark.taxid
    def test_taxid_has_parent(self):
        taxid = self._buildTaxaDBObject(TaxID)
        self.assertTrue(taxid.has_parent(335928, 'Bacteria'))

    @pytest.mark.taxid
    def test_taxid_has_parent_None(self):
        taxid = self._buildTaxaDBObject(TaxID)
        parent = taxid.has_parent(6, 'Bacteria')
        self.assertIsNone(parent)

    @pytest.mark.taxid
    def test_sci_name_taxid_None(self):
        """Check method returns None, no results found"""
        name = self._buildTaxaDBObject(SciName)
        taxid = name.taxid('qwerty')
        self.assertIsNone(taxid)

    @pytest.mark.taxid
    def test_taxid_sci_name_None(self):
        """Check method returns None, no results found"""
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.sci_name(0000)
        self.assertIsNone(name)

    @pytest.mark.taxid
    def test_taxid_lineage_id_ranks(self):
        taxid = self._buildTaxaDBObject(TaxID)
        lineage = taxid.lineage_id(9986, ranks=True)
        self.assertListEqual(lineage,
                             [('species', 9986), ('genus', 9984),
                              ('family', 9979), ('order', 9975),
                              ('no rank', 314147), ('superorder', 314146),
                              ('no rank', 1437010), ('no rank', 9347),
                              ('no rank', 32525), ('class', 40674),
                              ('no rank', 32524), ('no rank', 32523),
                              ('no rank', 1338369), ('no rank', 8287),
                              ('no rank', 117571), ('no rank', 117570),
                              ('no rank', 7776), ('no rank', 7742),
                              ('subphylum', 89593), ('phylum', 7711),
                              ('no rank', 33511), ('no rank', 33213),
                              ('no rank', 6072), ('kingdom', 33208),
                              ('no rank', 33154), ('superkingdom', 2759),
                              ('no rank', 131567)])

    @pytest.mark.taxid
    def test_taxid_lineage_id_reverse(self):
        taxid = self._buildTaxaDBObject(TaxID)
        lineage = taxid.lineage_id(9986, reverse=True)
        self.assertListEqual(lineage, [
            131567, 2759, 33154, 33208, 6072, 33213, 33511, 7711, 89593,
            7742, 7776, 117570, 117571, 8287, 1338369, 32523, 32524, 40674,
            32525, 9347, 1437010, 314146, 314147, 9975, 9979, 9984, 9986])

    @pytest.mark.taxid
    def test_taxid_lineage_id_None(self):
        """Check method returns None, no results found"""
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.lineage_id(0000)
        self.assertIsNone(name)

    @pytest.mark.taxid
    def test_taxid_lineage_id_revesrse_None(self):
        """Check method returns None, no results found"""
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.lineage_id(0000, reverse=True)
        self.assertIsNone(name)

    @pytest.mark.taxid
    def test_taxid_lineage_name(self):
        taxid = self._buildTaxaDBObject(TaxID)
        lineage = taxid.lineage_name(33208)
        self.assertListEqual(lineage, ['Metazoa', 'Opisthokonta',
                                       'Eukaryota', 'cellular organisms'])

    @pytest.mark.taxid
    def test_taxid_lineage_name_reverse(self):
        taxid = self._buildTaxaDBObject(TaxID)
        lineage = taxid.lineage_name(33208, reverse=True)
        self.assertListEqual(lineage, ['cellular organisms', 'Eukaryota',
                                       'Opisthokonta', 'Metazoa'])

    @pytest.mark.taxid
    def test_taxid_lineage_name_None(self):
        """Check method returns None, no results found"""
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.lineage_name(0000)
        self.assertIsNone(name)

    @pytest.mark.taxid
    def test_taxid_lineage_name_reverse_None(self):
        """Check method returns None, no results found"""
        taxid = self._buildTaxaDBObject(TaxID)
        name = taxid.lineage_name(0000, reverse=True)
        self.assertIsNone(name)

    @pytest.mark.taxid
    def test_taxid_unmapped_taxid_throws(self):
        """Check method throws SystemExit on demand"""
        taxid = self._buildTaxaDBObject(TaxID)
        with self.assertRaises(SystemExit):
            taxid._unmapped_taxid(0000, do_exit=True)
        self.assertTrue(taxid._unmapped_taxid(0000))


class TestTaxadbParser(unittest.TestCase):
    """Test class for taxadb.parser"""

    def setUp(self):
        self.testdir = os.path.dirname(os.path.realpath(__file__))
        self.nodes = os.path.join(self.testdir, 'test-nodes.dmp')
        self.names = os.path.join(self.testdir, 'test-names.dmp')
        self.merged = os.path.join(self.testdir, 'test-merged.dmp')
        self.acc = os.path.join(self.testdir, 'test-acc2taxid.gz')
        self.testdb = os.path.join(self.testdir, 'empty_db.sqlite')
        self.db = os.path.join(self.testdir, 'test_db.sqlite')
        self.chunk = 500

    def tearDown(self):
        if os.path.exists(self.testdb):
            os.unlink(self.testdb)

    @pytest.mark.parser    
    def test_parser_check_file_throws(self):
        """Check method throws SystemExit"""
        TaxaParser()
        with self.assertRaises(SystemExit):
            TaxaParser.check_file(None)
        with self.assertRaises(SystemExit):
            TaxaParser.check_file('/fakefile')
        with self.assertRaises(SystemExit):
            TaxaParser.check_file('/etc')

    @pytest.mark.parser
    def test_parser_check_file_True(self):
        """Check method returns True when file is ok"""
        tp = TaxaParser()
        self.assertTrue(tp.check_file(self.nodes))

    @pytest.mark.parser
    def test_taxadumpparser_taxdump_noargs(self):
        """Check method runs ok"""
        # Need connection to db. We use an empty db to fill list returned by
        #  parsing method
        db = TaxaDB(dbtype='sqlite', dbname=self.testdb)
        db.db.create_tables([Taxa])
        dp = TaxaDumpParser(verbose=True, nodes_file=self.nodes,
                            names_file=self.names)
        l = dp.taxdump()
        self.assertEqual(len(l), 14)

    @pytest.mark.parser
    def test_taxadumpparser_setnodes_throws(self):
        """Check method throws when None arg is given"""
        dp = TaxaDumpParser()
        with self.assertRaises(SystemExit):
            dp.set_nodes_file(None)

    @pytest.mark.parser
    def test_taxadumpparser_setnodes_true(self):
        """Check methods returns True"""
        dp = TaxaDumpParser()
        self.assertTrue(dp.set_nodes_file(self.nodes))

    @pytest.mark.parser
    def test_taxadumpparser_setnames_throws(self):
        """Check method throws when None arg is given"""
        dp = TaxaDumpParser()
        with self.assertRaises(SystemExit):
            dp.set_names_file(None)

    @pytest.mark.parser
    def test_taxadumpparser_setnames_true(self):
        """Check methods returns True"""
        dp = TaxaDumpParser()
        self.assertTrue(dp.set_names_file(self.names))

    @pytest.mark.parser
    def test_accessionparser_init(self):
        """Check init is ok"""
        ap = Accession2TaxidParser(acc_file=self.acc, chunk=self.chunk)
        self.assertEqual(ap.chunk, self.chunk)

    @pytest.mark.parser
    def test_accessionparser_accession2taxid(self):
        """Check method yield correct number of entries read from accession
        file"""
        # Need connection to db. We use an empty db to fill list returned by
        #  parsing method
        db = TaxaDB(dbtype='sqlite', dbname=self.testdb)
        db.db.create_tables([Taxa])
        db.db.create_tables([Accession])
        # We need to load names.dmp and nodes.dmp
        tp = TaxaDumpParser(nodes_file=self.nodes, names_file=self.names,
                            verbose=True)
        taxa_info = tp.taxdump()
        with db.db.atomic():
            for i in range(0, len(taxa_info), self.chunk):
                Taxa.insert_many(taxa_info[i:i + self.chunk]).execute()
        ap = Accession2TaxidParser(acc_file=self.acc, chunk=self.chunk,
                                   verbose=True)
        acc_list = ap.accession2taxid()
        total_entrires = 0
        for accs in acc_list:
            total_entrires += len(accs)
        self.assertEqual(total_entrires, 55211)

    @pytest.mark.parser
    def test_accessionparser_set_accession_file_throws(self):
        """Check method throws when file is None or does not exists"""
        ap = Accession2TaxidParser()
        with self.assertRaises(SystemExit):
            ap.set_accession_file(None)
        with self.assertRaises(SystemExit):
            ap.set_accession_file('/not-real')

    @pytest.mark.parser
    def test_accesionparser_set_accession_file_True(self):
        """Check method returns True when correct file is set"""
        ap = Accession2TaxidParser()
        self.assertTrue(ap.set_accession_file(self.acc))

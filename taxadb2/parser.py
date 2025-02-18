#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import gzip
import logging

from taxadb2.schema import Taxa, Accession, DeprecatedTaxID


class TaxaParser(object):

    """Base parser class for taxonomic files"""

    def __init__(self, verbose=False):
        """Base class"""
        self._verbose = verbose

    @property
    def logger(self):
        component = "{}.{}".format(type(self).__module__, type(self).__name__)
        return logging.getLogger(component)

    @staticmethod
    def cache_taxids():
        """Load data from taxa table into a dictionary

        Returns:
            data (:obj:`dict`): Data from taxa table mapped as dictionary

        """
        data = {}
        for x in Taxa.select(Taxa.ncbi_taxid).dicts():
            data[str(x['ncbi_taxid'])] = True
        return data

    @staticmethod
    def cache_merged_taxids():
        """Load merged tax IDs data from the DeprecatedTaxID table into a dictionary
    
        Returns:
            data (:obj:`dict`): Dictionary mapping old_taxid to new_taxid
        """
        data = {}
        # Load the old and new taxid mapping from the DeprecatedTaxID table
        for entry in DeprecatedTaxID.select(DeprecatedTaxID.old_taxid, DeprecatedTaxID.new_taxid).dicts():
            data[str(entry['old_taxid'])] = str(entry['new_taxid'])
        return data

    @staticmethod
    def check_file(element):
        """Make some check on a file

        This method is used to check an `element` is a real file.

        Args:
            element (:obj:`type`): File to check

        Returns:
            True

        Raises:
            SystemExit: if `element` file does not exist
            SystemExit: if `element` is not a file

        """
        logger = logging.getLogger('parser')
        if element is None:
            logger.error("Please provide an input file to check")
            sys.exit(1)
        if not os.path.exists(element):
            logger.error("File %s does not exist" % str(element))
            sys.exit(1)
        if not os.path.isfile(element):
            logger.error("%s is not a file" % str(element))
            sys.exit(1)
        return True


class TaxaDumpParser(TaxaParser):

    """Main parser class for ncbi taxdump files

    This class is used to parse NCBI taxonomy files found in taxdump.gz archive

    Args:
        nodes_file (:obj:`str`): Path to nodes.dmp file
        names_file (:obj:`str`): Path to names.dmp file
        merged_file (:obj:`str`): Path to merged.dmp file

    """
    def __init__(self, nodes_file=None, names_file=None, merged_file=None, dbtype=None, dbname=None, **kwargs):
        """

        """
        super().__init__(**kwargs)
        self.nodes_file = nodes_file
        self.names_file = names_file
        self.merged_file = merged_file
        self.dbtype = dbtype
        self.dbname = dbname

    def taxdump(self, nodes_file=None, names_file=None, merged_file=None):
        """Parse .dmp files and return both taxa and deprecated taxid data

        Parse nodes.dmp, names.dmp, and merged.dmp files and return:
        - A list of taxonomic information to insert into the Taxa table
        - A list of deprecated tax ID mappings to insert into the DeprecatedTaxID table

        Args:
            nodes_file (:obj:`str`): Path to nodes.dmp file
            names_file (:obj:`str`): Path to names.dmp file
            merged_file (:obj:`str`): Path to merged.dmp file

        Returns:
            tuple:
                - List of dictionaries to insert into Taxa
                - List of dictionaries to insert into DeprecatedTaxID
        """
        if nodes_file is None:
            nodes_file = self.nodes_file
        if names_file is None:
            names_file = self.names_file
        if merged_file is None:
            merged_file = self.merged_file
        self.check_file(names_file)
        self.check_file(nodes_file)
        self.check_file(merged_file)
        # parse nodes.dmp
        nodes_data = list()
        self.logger.debug("Loading taxa data ...")
        ncbi_ids = self.cache_taxids()
        self.logger.debug("Parsing %s" % str(nodes_file))
        with open(nodes_file, 'r') as f:
            for line in f:
                line_list = line.split('|')
                ncbi_id = line_list[0].strip('\t')
                if ncbi_id in ncbi_ids:
                    continue
                data_dict = {
                    'ncbi_taxid': ncbi_id,
                    'parent_taxid': line_list[1].strip('\t'),
                    'tax_name': '',
                    'lineage_level': line_list[2].strip('\t')
                }
                nodes_data.append(data_dict)
        self.logger.info('Parsed nodes.dmp')

        # parse names.dmp
        names_data = list()
        self.logger.debug("Parsing %s" % str(names_file))
        with open(names_file, 'r') as f:
            for line in f:
                if 'scientific name' in line:
                    line_list = line.split('|')
                    ncbi_id = line_list[0].strip('\t')
                    if ncbi_id in ncbi_ids:
                        continue
                    data_dict = {
                        'ncbi_taxid': line_list[0].strip('\t'),
                        'tax_name': line_list[1].strip('\t')
                    }
                    names_data.append(data_dict)
        self.logger.info('Parsed names.dmp')

        # parse merged.dmp
        merged_data = list()
        self.logger.debug("Parsing %s" % str(merged_file))
        with open(merged_file, 'r') as f:
            for line in f:
                parts = line.strip().split("\t|")
                if len(parts) < 2:
                    self.logger.warning(f"Skipping malformed line: {line.strip()}")
                    continue
                try:
                    old_taxid = int(parts[0].strip())
                    new_taxid = int(parts[1].strip())
                    # DeprecatedTaxID.get_or_create(old_taxid=old_taxid, new_taxid=new_taxid)
                    merged_data.append({'old_taxid': old_taxid, 'new_taxid': new_taxid})
                except ValueError as e:
                    self.logger.error(f"Error parsing line '{line.strip()}': {e}")
                    continue  # Skip invalid entries
        self.logger.info(f"Parsed {len(merged_data)} entries from merged.dmp")

        # merge the two dictionaries
        taxa_info_list = list()
        for nodes, names in zip(nodes_data, names_data):
            taxa_info = {**nodes, **names}  # PEP 448, requires python 3.5
            taxa_info_list.append(taxa_info)
        self.logger.debug('merge successful')
        return taxa_info_list, merged_data

    def set_nodes_file(self, nodes_file):
        """Set nodes_file

        Set the accession file to use

        Args:
            nodes_file (:obj:`str`): Nodes file to be set

        Returns:
            True

        Raises:
            SystemExit: If `nodes_file` is None or not a file (`check_file`)

        """
        if nodes_file is None:
            self.logger.error("Please provide an nodes file to set")
            sys.exit(1)
        self.check_file(nodes_file)
        self.nodes_file = nodes_file
        return True

    def set_names_file(self, names_file):
        """Set names_file

        Set the accession file to use

        Args:
            names_file (:obj:`str`): Nodes file to be set

        Returns:
            True

        Raises:
            SystemExit: If `names_file` is None or not a file (`check_file`)

        """
        if names_file is None:
            self.logger.error("Please provide an names file to set")
            sys.exit(1)
        self.check_file(names_file)
        self.names_file = names_file
        return True

    def set_merged_file(self, merged_file):
        """Set merged_file

        Set the merged file to use (deprecated TaxIDs mapping)

        Args:
            merged_file (:obj:`str`): Merged file to be set

        Returns:
            True

        Raises:
            SystemExit: If `merged_file` is None or not a file (`check_file`)

        """
        if merged_file is None:
            self.logger.error("Please provide a merged file to set")
            sys.exit(1)
        self.check_file(merged_file)
        self.merged_file = merged_file
        return True

    def resolve_taxid(self, taxid):
        """Check if a taxID is deprecated in the database and return the new one.

        Args:
            taxid (int): The queried TaxID.

        Returns:
            int: Updated TaxID if found in DeprecatedTaxID table, otherwise original.
        """
        try:
            deprecated_entry = DeprecatedTaxID.get(DeprecatedTaxID.old_taxid == taxid)
            new_taxid = deprecated_entry.new_taxid
            self.logger.warning(f"TaxID {taxid} is deprecated, using {new_taxid} instead.")
            return new_taxid
        except DeprecatedTaxID.DoesNotExist:
            return taxid  # If no replacement exists, return the original


class Accession2TaxidParser(TaxaParser):

    """Main parser class for nucl_xxx_accession2taxid files

    This class is used to parse accession2taxid files.

    Args:
        acc_file (:obj:`str`): File to parse
        chunk (:obj:`int`): Chunk insert size. Default 500
        fast (:obj:`bool`): Directly load accession into database, do not check
                            existence.
    """

    def __init__(self, acc_file=None, chunk=500, fast=False, **kwargs):
        super().__init__(**kwargs)
        self.acc_file = acc_file
        self.chunk = chunk
        self.fast = fast

    def accession2taxid(self, acc2taxid=None, chunk=None):
        """Parses the accession2taxid files

        This method parses the accession2taxid file, build a dictionary,
            stores it in a list and yield for insertion in the database.

        ::

            {
                'accession': accession_id_from_file,
                'taxid': associated_taxonomic_id
            }


        Args:
            acc2taxid (:obj:`str`): Path to acc2taxid input file (gzipped)
            chunk (:obj:`int`): Chunk size of entries to gather before
                yielding. Default 500 (set at object construction)

        Yields:
            list: Chunk size of read entries

        """
        # Some accessions (e.g.: AAA22826) have a taxid = 0
        entries = []
        counter = 0
        taxids = self.cache_taxids()
        if not self.fast:
            accessions = {}
        if acc2taxid is None:
            acc2taxid = self.acc_file
        self.check_file(acc2taxid)
        if chunk is None:
            chunk = self.chunk
        self.logger.debug("Parsing %s" % str(acc2taxid))
        self.logger.debug("Fast mode %s" % "ON" if self.fast else "OFF")
        with gzip.open(acc2taxid, 'rb') as f:
            f.readline()  # discard the header
            for line in f:
                line_list = line.decode().rstrip('\n').split('\t')
                # Check the taxid already exists and get its id
                if line_list[2] not in taxids:
                    continue
                # In case of an update or parsing an already inserted list of
                # accessions
                if not self.fast:
                    if line_list[0] in accessions:
                        continue
                    try:
                        Accession.get(Accession.accession == line_list[0])
                    except Accession.DoesNotExist:
                        accessions[line_list[0]] = True
                    data_dict = {
                        'accession': line_list[0],
                        'taxid': line_list[2]
                    }
                else:
                    data_dict = {
                        'accession': line_list[0],
                        'taxid': line_list[2]
                    }
                entries.append(data_dict)
                counter += 1
                if counter == chunk:
                    yield(entries)
                    entries = []
                    counter = 0
        if len(entries):
            yield(entries)

    def set_accession_file(self, acc_file):
        """Set the accession file to use

        Args:
            acc_file (:obj:`str`): File to be set

        Returns:
            True
        Raises:
            SystemExit: If `acc_file` is None or not a file (`check_file`)

        """
        if acc_file is None:
            self.logger.error("Please provide an accession file to set")
            sys.exit(1)
        self.check_file(acc_file)
        self.acc_file = acc_file
        return True

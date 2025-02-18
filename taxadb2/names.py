from taxadb2.schema import Taxa
from taxadb2.taxadb import TaxaDB
from taxadb2.parser import TaxaDumpParser


class SciName(TaxaDB, TaxaDumpParser):
    """Main class for querying scientific names

    Provide methods to request taxa table and get associated taxid ids.

    Args:
        **kwargs: Arbitrary arguments. Supported (username, password, port,
            hostname, config, dbtype, dbname)

    Raises:
        SystemExit: If table `taxa` does not exist
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.check_table_exists(Taxa)
        TaxaDumpParser.__init__(self, **kwargs)

    def taxid(self, sci_name):
        """Get taxid from scientific name

        Given a taxid, return its associated scientific name

        Args:
            sci_name (:obj:`int`): a scientific name
        Returns:
            int: ncbi_taxid, taxid matching scientific name or None if
                taxid not found
        """
        try:
            ncbi_taxid = Taxa.get(Taxa.tax_name == sci_name).ncbi_taxid
            return self.resolve_taxid(ncbi_taxid) 
        except Taxa.DoesNotExist:
            return None

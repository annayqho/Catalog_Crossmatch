import requests 
from astropy.io.votable import parse_single_table 
 
# from https://michaelmommert.wordpress.com/2017/02/13/accessing-the-gaia-and-pan-starrs-catalogs-using-python/

def panstarrs_query(ra_deg, dec_deg, rad_deg, mindet=1, 
                    maxsources=10000,
                    server=('https://archive.stsci.edu/'+
                            'panstarrs/search.php')): 
    """
    Query Pan-STARRS DR1 @ MAST
    parameters: ra_deg, dec_deg, rad_deg: RA, Dec, field 
                                          radius in degrees
                mindet: minimum number of detection (optional)
                maxsources: maximum number of sources
                server: servername
    returns: astropy.table object
    """
    r = requests.get(server, 
    params= {'RA': ra_deg, 'DEC': dec_deg, 
             'SR': rad_deg, 'max_records': maxsources, 
             'outputformat': 'VOTable', 
             'ndetections': ('>%d' % mindet)}) 
 
    # parse local file into astropy.table object 
    data = parse_single_table('panstarrs.xml')
    return data.to_table(use_names_over_ids=True) 
 
# Example query
print(panstarrs_query(118.024438, 46.684244, 3/3600))


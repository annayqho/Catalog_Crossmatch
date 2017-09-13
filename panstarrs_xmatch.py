import requests 
from astropy.io.votable import parse_single_table 
from astropy.table import Table,Column
 
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
 
    # write query data into local file 
    outf = open('panstarrs.xml', 'w') 
    outf.write(r.text) 
    outf.close() 

    # parse local file into astropy.table object 
    data = parse_single_table('panstarrs.xml')
    tab = data.to_table(use_names_over_ids=True) 
    g = tab['gMeanPSFMag'] - tab['gMeanKronMag']
    r = tab['rMeanPSFMag'] - tab['rMeanKronMag']
    i = tab['iMeanPSFMag'] - tab['iMeanKronMag']
    z = tab['zMeanPSFMag'] - tab['zMeanKronMag']
    y = tab['yMeanPSFMag'] - tab['yMeanKronMag']
    sep = tab["Ang Sep (')"] * 60 # in arcsec
    t = Table(
        [ra_deg,dec_deg,g,r,i,z,y,sep], 
        names=['RA', 'Dec', 'gval', 'rval', 'ival', 'zval', 'yval', 'Sep'])
    return t


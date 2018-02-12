import requests 
import numpy as np
from astropy.io.votable import parse_single_table 
from astropy.table import Table,Column
 
# from https://michaelmommert.wordpress.com/2017/02/13/accessing-the-gaia-and-pan-starrs-catalogs-using-python/

def is_star(ra_deg, dec_deg, rad_deg, mindet=1, 
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
    returns: whether source is a star
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
    if len(tab['objName']):
        mag_names = ['g', 'r', 'i', 'z', 'y']
        mags= [tab['gMeanPSFMag'], tab['rMeanPSFMag'], tab['iMeanPSFMag'], tab['zMeanPSFMag'], tab['yMeanPSFMag']]
        print(len(mags))
        choose = np.argmin(mags)
        is_star = mags[choose] - tab['%sMeanKronMag' %mag_names[choose]] < 0
        sep = tab["Ang Sep (')"] * 60 # in arcsec
        return is_star,sep
    return False

import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates as coords
from astropy.table import Table


def wise_colors(names,ras,decs,rad):
    """ rad in arcsec """
    names_out = []
    res = []
    for ii,name in enumerate(names):
        print(name)
        # no WISE: 15bgf, 16bse, 17ahn, 13dqr, 13agt, 13nn, 16ccd
        vquery = Vizier(
                columns=['_q', 'W1mag', 'e_W1mag', 'W2mag', 
                         'e_W2mag', 'W3mag', 'e_W3mag', '_r'])
        sources = coords.SkyCoord(ras[ii], decs[ii], unit='deg')
        res_out = vquery.query_region(sources, radius='3arcsec', catalog='ALLWISE')
        if len(res_out) > 0:
            names_out.append(name)
            res.append(res_out[0])
    return res
    #return res['_q', 'W1mag', 'e_W1mag', 'W2mag', 'e_W2mag', 'W3mag', 'e_W3mag', '_r']

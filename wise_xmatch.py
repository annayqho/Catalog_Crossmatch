import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates as coords
from astropy.table import Table


def wise_colors(names,ras,decs,rad):
    """ rad in arcsec """

    # First, check to see who *has* a counterpart
    has_counterpart = []
    for ii,name in enumerate(names):
        # no WISE: 15bgf, 16bse, 17ahn, 13dqr, 13agt, 13nn, 16ccd
        vquery = Vizier(
                columns=['_q', 'W1mag', 'e_W1mag', 'W2mag', 
                         'e_W2mag', 'W3mag', 'e_W3mag', '_r'])
        sources = coords.SkyCoord(ras[ii], decs[ii], unit='deg')
        res_out = vquery.query_region(sources, radius='3arcsec', catalog='ALLWISE')
        if len(res_out) > 0:
            has_counterpart.append(name)

    # Now, only do the search for those with counterparts
    inds = np.array([np.where(names==name)[0][0] for name in has_counterpart])
    name_choose = names[inds]
    ra_choose = ras[inds]
    dec_choose = decs[inds]
    vquery = Vizier(
            columns=['_q', 'W1mag', 'e_W1mag', 'W2mag',
                'e_W2mag', 'W3mag', 'e_W3mag', '_r'])
    sources = coords.SkyCoord(ra_choose, dec_choose, unit='deg')
    res = vquery.query_region(sources, radius='3arcsec', catalog='ALLWISE')[0]
    return name_choose, res['_q', 'W1mag', 'e_W1mag', 'W2mag', 'e_W2mag', 'W3mag', 'e_W3mag', '_r']

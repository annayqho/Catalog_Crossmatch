import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates as coords
from astropy.table import Table

def wise_colors(ras,decs):
    sources = coords.SkyCoord(ras, decs, unit='deg')
    nsources = len(sources)
    w1 = np.zeros(nsources)
    w2 = np.zeros(nsources)
    w3 = np.zeros(nsources)
    w1_err = np.zeros(nsources)
    w2_err = np.zeros(nsources)
    w3_err = np.zeros(nsources)
    sep = np.zeros(nsources)

    for ii in np.arange(nsources):
        out_raw = Vizier.query_region(
                sources[ii], radius='3arcsec', catalog='ALLWISE')
        if len(out_raw) > 0:
            out = out_raw[0]
            choose = np.argmin(out['_r'])
            w1[ii] = out['W1mag'][choose]
            w1_err[ii] = out['e_W1mag'][choose]
            w2[ii] = out['W2mag'][choose]
            w2_err[ii] = out['e_W2mag'][choose]
            w3[ii] = out['W3mag'][choose]
            w3_err[ii] = out['e_W3mag'][choose]
            sep[ii] = out['_r'][choose]
    return w1,w2,w3,w1_err,w2_err,w3_err,sep

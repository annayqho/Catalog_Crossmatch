import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates as coords
from astropy.table import Table

def wise_colors(ras,decs):
    sources = coords.SkyCoord(ras, decs, unit='deg')
    nsources = len(sources)
    out_raw = Vizier.query_region(
            sources, radius='3arcsec', catalog='ALLWISE')
    w1s = np.zeros(nsources)
    w2s = np.zeros(nsources)
    w3s = np.zeros(nsources)
    w4s = np.zeros(nsources)
    seps = np.zeros(nsources)

    if out is not None:
        out = out_raw[0]
        inds = np.array(out['_q']-1)
        
        w1s[inds] = out['W1mag']
        w1s[w1s==0] = None
        w2s[inds] = out['W2mag']
        w2s[w2s==0] = None
        w3s[inds] = out['W3mag']
        w3s[w3s==0] = None
        w4s[inds] = out['W4mag']
        w4s[w4s==0] = None
        seps[inds] = out['_r']
        seps[seps==0] = None
        return w1s,w2s,w3s,w4s,seps

    else:
        return None


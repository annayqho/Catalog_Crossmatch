import numpy as np
from astroquery.vizier import Vizier
from astropy import coordinates as coords
from astropy.table import Table

def wise_colors(ras,decs,rad):
    """ rad in arcsec """
    vquery = Vizier(columns=['_q', 'W1mag', 'W2mag', 'W3mag', '_r'])
    sources = coords.SkyCoord(ras, decs, unit='deg')
    return vquery.query_region(sources, radius='3arcsec', catalog='ALLWISE')[0]

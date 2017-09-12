import numpy as np
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy.table import Table
import astropy.units as u
from astropy.table import Table,Column

def get_colors(objid):
    stmt = "SELECT u,g,r,i,z FROM PhotoPrimary as p\
            WHERE p.objid = '%s'" %objid
    out = SDSS.query_sql(stmt)
    u = float(out['u'])
    g = float(out['g'])
    r = float(out['r'])
    i = float(out['i'])
    z = float(out['z'])
    return u,g,r,i,z


def get_redshift(objid):
    """ Return the best redshift, from photo or spec """
    stmt = "SELECT z,zErr from Photoz as p\
            WHERE p.objID = '%s'" %objid
    photo_out = SDSS.query_sql(stmt)
    stmt = "SELECT z,zErr FROM SpecPhotoAll as s\
            WHERE s.objid = '%s'" %objid
    spec_out = SDSS.query_sql(stmt)
    if spec_out is not None:
        out = spec_out[0]
    elif photo_out is not None:
        out = photo_out[0]
    else:
        return -9999,-9999
    return out['z'], out['zErr']


def get_type(ras, decs, rad):
    """ For ra and dec within rad, get SDSS ID of nearest object """
    tosearch = coords.SkyCoord(ras, decs, unit='deg')
    nsources = len(ras)
    out = SDSS.query_crossid(
            tosearch, photoobj_fields=['ra,dec,type'], radius=3*u.arcsec)
    # note that these are zero-indexed
    inds = np.array(
            [val.split("_")[1] for val in out['obj_id'].astype(str)]).astype(int)
    found = coords.SkyCoord(out['ra'], out['dec'], unit='deg')
    dist_deg = found.separation(tosearch[inds])
    dist_arcsec = dist_deg.arcsec
    dist = np.zeros(nsources)
    dist[inds] = dist_arcsec
    dist_col = Column(name="Separation", data=dist)
    out.add_column(dist_col)
    return out['type1', 'Separation']
    


def sdss_data(ras,decs,rad):
    """ Query within search radius, rad entered in arcseconds
    Note that this won't work at all if it's farther than a degree away """
    sources = coords.SkyCoord(ras, decs, unit='deg')
    nsources = len(sources)
    u = np.zeros(nsources)
    g = np.zeros(nsources)
    r = np.zeros(nsources)
    i = np.zeros(nsources)
    z = np.zeros(nsources)
    redshifts = np.zeros(nsources)
    redshifterrs = np.zeros(nsources)
    types = np.zeros(nsources, dtype=str)
    seps = np.zeros(nsources)

    for ii in np.arange(nsources):
        objid = get_objid(ras[ii], decs[ii], rad)
        uval = None
        gval = None
        rval = None
        ival = None
        zval = None
        redshift = None
        redshifterr = None
        sepval = None
        typ = None
        if objid is not None:
            uval,gval,rval,ival,zval = get_colors(objid)
            redshift,redshifterr = get_redshift(objid)
            typ = get_type(objid)
        u[ii] = uval
        g[ii] = gval
        r[ii] = rval
        i[ii] = ival
        z[ii] = zval
        redshifts[ii] = redshift
        redshifterrs[ii] = redshifterr
        types[ii] = typ
        seps[ii] = sepval
    return u,g,r,i,z,redshifts,redshifterrs,seps,types

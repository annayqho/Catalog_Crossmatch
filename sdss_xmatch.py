import numpy as np
from astroquery.sdss import SDSS
from astropy import coordinates as coords
from astropy.table import Table


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


def get_type(objid):
    stmt = "SELECT type FROM PhotoPrimary as p\
            WHERE p.objid = '%s'" %objid
    out = SDSS.query_sql(stmt)
    if out['type'] == 3:
        return 'galaxy'
    elif out['type'] == 6:
        return 'star'


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


def get_objid(ra, dec, rad):
    """ For ra and dec within rad, get SDSS ID of nearest object """
    xid = SDSS.query_sql(
        """ SELECT n.objID,n.distance\
            FROM dbo.fGetNearestObjEq(%s,%s,1) as n""" %(ra,dec))
    if xid is not None:
        objid = xid['objID'].data[0]
        sep = xid['distance'].data[0]
        sepval = sep*60
        if sepval <= rad: # within the provided search radius
            return objid
    return None


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

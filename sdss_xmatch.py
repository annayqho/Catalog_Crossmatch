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


def sdss_data(ras,decs):
    sources = coords.SkyCoord(ras, decs, unit='deg')
    nsources = len(sources)
    u = np.zeros(nsources)
    g = np.zeros(nsources)
    r = np.zeros(nsources)
    i = np.zeros(nsources)
    z = np.zeros(nsources)
    redshifts = np.zeros(nsources)
    redshifterrs = np.zeros(nsources)
    seps = np.zeros(nsources)

    for ii in np.arange(nsources):
        xid = SDSS.query_sql(
                """ SELECT n.objID,n.distance\
                    FROM dbo.fGetNearestObjEq(%s,%s,5) as n""" %(ras[ii],decs[ii]))
        objid = xid['objID'].data[0]
        sep = xid['distance'].data[0]
        if sep*60 <= 3: # within 3 arcseconds
            print(objid)
            uval,gval,rval,ival,zval = get_colors(objid)
            redshift,redshifterr = get_redshift(objid)
            u[ii] = uval
            g[ii] = gval
            r[ii] = rval
            i[ii] = ival
            z[ii] = zval
            redshifts[ii] = redshift
            redshifterrs[ii] = redshifterr
            seps[ii] = sep*60
    return u,g,r,i,z,redshifts,redshifterrs,seps

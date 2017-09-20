""" Code from Matthew Graham """

from astroquery.irsa import Irsa
import astropy.coordinates as coord
import astropy.units as u



def getWISE(ra, dec):
  w1aw, w1nwr, w2aw, w2nwr = [], [], [], []

  # AllWISE Multiepoch Photometry Table
  table = Irsa.query_region(coord.SkyCoord(ra, dec, unit = (u.deg, u.deg)), catalog = 'allwise_p3as_mep', radius='0d0m5s')
  table.sort('mjd')
  df = table.to_pandas()
  # Filter on poor quality frames, charged particle hits, and scattered moonlight
  dfp = df.query('saa_sep >= 0 and moon_masked == "0000"')
  if len(dfp) > 0:
    raw1 = dfp[['mjd', 'w1mpro_ep', 'w1sigmpro_ep']]
    raw2 = dfp[['mjd', 'w2mpro_ep', 'w2sigmpro_ep']]
    raw1 = raw1.query('w1mpro_ep != "NaN" and w1sigmpro_ep != "NaN"')
    raw2 = raw2.query('w2mpro_ep != "NaN" and w2sigmpro_ep != "NaN"')
    w1aw = groupByDate2(raw1.values.T) # this gives weighted daily averages of magnitude and magnitude error
    w2aw = groupByDate2(raw2.values.T)

  # NEOWISE-R Single Exposure (L1b) Source Table
  table = Irsa.query_region(coord.SkyCoord(ra, dec, unit = (u.deg, u.deg)), catalog = 'neowiser_p1bs_psd', radius='0d0m5s')
  table.sort('mjd')
  df = table.to_pandas()
  # Filter on poor quality frames, charged particle hits, and scattered moonlight
  dfp = df.query('qual_frame != 0')
  if len(dfp) > 0:
    raw1 = dfp[['mjd', 'w1mpro', 'w1sigmpro']]
    raw2 = dfp[['mjd', 'w2mpro', 'w2sigmpro']]
    raw1 = raw1.query('w1mpro != "NaN" and w1sigmpro != "NaN"')
    raw2 = raw2.query('w2mpro != "NaN" and w2sigmpro != "NaN"')
    w1nwr = groupByDate2(raw1.values.T)
    w2nwr = groupByDate2(raw2.values.T)

  w1 = w1aw and np.concatenate((w1aw, w1nwr), axis = 1) or w1nwr
  w2 = w2aw and np.concatenate((w2aw, w2nwr), axis = 1) or w2nwr

  return w1, w2

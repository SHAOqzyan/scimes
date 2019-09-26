from astropy.io import fits
from myPYTHON import *
from astrodendro import Dendrogram
from astrodendro import ppv_catalog
from astropy import units as u
from scimes import SpectralCloudstering


testFITS="G214CO12.fits"

data,head =  myFITS.readFITS( testFITS )

metadata = {}
metadata['data_unit'] = u.K
metadata['spatial_scale'] =  30 * u.arcsec
metadata['beam_major'] =  50 * u.arcsec # FWHM
metadata['beam_minor'] =  50 * u.arcsec # FWHM
c= 299792458.
f=115271202000.0
wavelength=c/f*u.meter

metadata['wavelength'] = wavelength  # 22.9 * u.arcsec # FWHM


class mySCIMES:

	def __init__(self ):

		pass


	cat = ppv_catalog(d, metadata)



	sigma = 0.5 #K, noise level

	d = Dendrogram.compute(data, min_value=3*sigma, min_delta=3*sigma, min_npix=500)


	dclust = SpectralCloudstering(d,cat,hd)
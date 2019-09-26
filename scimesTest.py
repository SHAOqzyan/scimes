from astropy.io import fits
from myPYTHON import *
from astrodendro import Dendrogram
from astrodendro import ppv_catalog
from astropy import units as u
from scimes import SpectralCloudstering




class mySCIMES:

	metadata = {}
	metadata['data_unit'] = u.K
	metadata['spatial_scale'] =  30 * u.arcsec
	metadata['beam_major'] =  50 * u.arcsec # FWHM
	metadata['beam_minor'] =  50 * u.arcsec # FWHM
	c= 299792458.
	f=115271202000.0
	wavelength=c/f*u.meter

	metadata['wavelength'] = wavelength  # 22.9 * u.arcsec # FWHM

	sigma = 0.5 #K, noise level


	def __init__(self ):

		pass


	def doDendro(self, data,minV=3,minDelta=3,minP=1000 ):

		d = Dendrogram.compute(data, min_value=minV*sigma, min_delta=minDelta*sigma, min_npix=minP)
		return d

	def doCluster(self,dendroCase ,saveName,head ):



		saveCloudFITS=saveName+"CloudAsgn.fits"
		saveTrunkFITS=saveName+"TrunkAsgn.fits"

		saveCloudCat=saveName+"CloudCat.fits"


		cat = ppv_catalog(dendroCase, self.metadata)

		dclust = SpectralCloudstering(dendroCase,cat,head)

		sigma = 0.5 #K, noise level

		d = Dendrogram.compute(data, min_value=3*sigma, min_delta=3*sigma, min_npix=500)


		dclust = SpectralCloudstering(d,cat,hd)

		cloudHDU=dclust.clusters_asgn

		cloudHDU.writeto(saveCloudFITS,overwrite=True)


		trunkHDU=dclust.trunks_asgn

		trunkHDU.writeto(trunkHDU,overwrite=True)



		cCat=cat[dclust.clusters]

		cCat.write(saveCloudCat,overwrite=True)






		return len(d.trunk)

	def ZZZ(self):
		pass

doSCIMES=mySCIMES()

testFITS="G214CO12.fits"

data,head =  myFITS.readFITS( testFITS )

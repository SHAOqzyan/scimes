from astropy.io import fits
from myPYTHON import *
from astrodendro import Dendrogram
from astrodendro import ppv_catalog
from astropy import units as u
from scimes import SpectralCloudstering

from astropy.wcs import WCS


class mySCIMES:
	dataPath="./data/"
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
		print "Calculating dendrogram...."
		d = Dendrogram.compute(data, min_value=minV*self.sigma, min_delta=minDelta*self.sigma, min_npix=minP)
		print "Done"
		return d

	def doCluster(self,dendroCase ,saveName,head ):
		savePath=self.dataPath+saveName+"/"

		trunkN = len(dendroCase.trunk)
		print "trunkN: {} ".format(trunkN  )


		os.system("mkdir "+savePath)

		saveCloudFITS=savePath+saveName+"CloudAsgn.fits"
		saveTrunkFITS=savePath+saveName+"TrunkAsgn.fits"

		saveCloudCat=savePath+saveName+"CloudCat.fit"
		saveDenroCat=savePath+saveName+"DendroCat.fit"
		saveDenroFITS=savePath+saveName+"DendroFITS.fits"
		dendroCase.save_to(saveDenroFITS) #save dendro

		self.metadata['wcs'] = WCS( head )

		cat = ppv_catalog(dendroCase, self.metadata)



		dclust = SpectralCloudstering(dendroCase,cat,head  )

		cloudHDU=dclust.clusters_asgn

		cloudHDU.writeto(saveCloudFITS,overwrite=True)


		trunkHDU=dclust.trunks_asgn

		trunkHDU.writeto(saveTrunkFITS,overwrite=True)

		cCat=cat[dclust.clusters]
		cCat.write(saveCloudCat,overwrite=True)

		cat.write(saveDenroCat,overwrite=True)

		cloudN=   len( set( cloudHDU.data.reshape(-1) ) )-1


		#save dendro cat


		print "trunkN: {}, cloudN: {}".format(trunkN,cloudN)
		return trunkN,cloudN

	def ZZZ(self):
		pass




doSCIMES=mySCIMES()


testFITS="scimesTest.fits"


data,head =  myFITS.readFITS( testFITS )


trunkNList=[]
cloudNList=[]

for minPs in np.arange(3500,10500,500):


	dendroCase=doSCIMES.doDendro(data,minP=minPs)
	testRegion="G2650TestMinp{}".format(minPs)
	trunkN,cloudN=doSCIMES.doCluster(dendroCase, testRegion, head )

	trunkNList.append(trunkN )
	cloudNList.append(cloudN )

print trunkNList
print cloudNList
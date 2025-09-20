try:
	import cv2
	import numpy as np
	from glob import glob
	from sklearn.cluster import KMeans
	from sklearn.svm import SVC
	from sklearn.preprocessing import StandardScaler
	from matplotlib import pyplot as plt
	print("Library Loaded")
except Exception as e:
	print("Library not Found", e)


class ImageHelpers:
	def __init__(self):
		# self.siftObject = cv2.xfeatures2d.SIFT_create()
		# self.surfObject = cv2.xfeatures2d.SURF_create()
		self.siftObject = cv2.SIFT_create()

	def gray(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		return gray

	def FeaturesExtract(self, image):
		keypoints, descriptors = self.siftObject.detectAndCompute(image, None)
		# keypoints, descriptors = self.surfObject.detectAndCompute(image, None)
		return [keypoints, descriptors]


class BOVHelpers:
	def __init__(self, n_clusters=20):
		self.n_clusters = n_clusters
		self.kmeansObjects = KMeans(n_clusters=n_clusters)
		self.kmeansReturn = None
		self.descriptorVStack = None
		self.mega_histogram = None
		self.clf = SVC()

	def Cluster(self):
		"""
		cluster using KMeans algorithm, 

		"""
		self.kmeansReturn = self.kmeansObjects.fit_predict(self.descriptorVStack)

	def DevelopVocabulary(self, n_images, descriptor_list, kmeansReturn=None):

		"""
		Each cluster refer a particular visual word
		Every image can be represeted as a combination of multiple 
		visual words. The best method is to generate a sparse histogram
		that contains the frequency of occurence of each visual word 

		Thus the vocabulary comprises of a set of histograms of encompassing
		all descriptions for all images

		"""

		self.mega_histogram = np.array([np.zeros(self.n_clusters) for i in range(n_images)])
		old_count = 0
		for i in range(n_images):
			l = len(descriptor_list[i])
			for j in range(l):
				if kmeansReturn is None:
					idx = self.kmeansReturn[old_count + j]
				else:
					idx = kmeansReturn[old_count + j]
				self.mega_histogram[i][idx] += 1
			old_count += l
		print("Vocabulary Histogram Generated")

	def standardize(self, std=None):
		"""
		
		standardize is required to normalize the distribution
		wrt sample size and features. If not normalized, the classifier may become
		biased due to steep variances.

		"""
		if std is None:
			self.scale = StandardScaler().fit(self.mega_histogram)
			self.mega_histogram = self.scale.transform(self.mega_histogram)
		else:
			print("STD not none. External STD supplied")
			self.mega_histogram = std.transform(self.mega_histogram)

	def formatND(self, l):
		"""
		restructures list into vstack array of shape
		M samples x N features for sklearn

		"""
		vStack = np.array(l[0])
		for remaining in l[1:]:
			vStack = np.vstack((vStack, remaining))
		self.descriptorVStack = vStack.copy()
		return vStack

	def train(self, train_labels):
		"""
		uses sklearn.svm.SVC classifier (SVM) 


		"""
		print("Training SVM")
		# print(self.clf)
		print("Train labels", train_labels)
		self.clf.fit(self.mega_histogram, train_labels)
		print("Training completed")

	def Predict(self, iplist):
		predictions = self.clf.predict(iplist)
		return predictions

	def HisttrogramPlotting(self, vocabulary=None):
		print("Plotting histogram")
		if vocabulary is None:
			vocabulary = self.mega_histogram

		x_scalar = np.arange(self.n_clusters)
		y_scalar = np.array([abs(np.sum(vocabulary[:, h], dtype=np.int32)) for h in range(self.n_clusters)])

		print(y_scalar)

		plt.bar(x_scalar, y_scalar)
		plt.xlabel("Visual Word Index")
		plt.ylabel("Frequency")
		plt.title("Complete Vocabulary Generated")
		plt.xticks(x_scalar + 0.4, x_scalar)
		plt.show()


class FileHelpers:

	def __init__(self):
		pass

	@staticmethod
	def GetFiles(path: object) -> object:
		"""


		"""
		images = {}
		count = 0
		for each in glob(path + "*"):
			word = each.split("\\")[-1]
			# print("Reading image category ", word)
			images[word] = []
			for imagefile in glob(path+word+"/*"):
				# print("Reading file ", imagefile)
				im = cv2.imread(imagefile, 0)
				images[word].append(im)
				count += 1

		return [images, count]


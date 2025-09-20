try:
    from helpers import *
    from matplotlib import pyplot as plt
    print("Library Loaded")
except Exception as e:
    print("Library not Found", e)


class BagOfWords:
    def __init__(self, no_clusters):
        self.no_clusters = no_clusters
        self.trainingPath = None
        self.testingPath = None
        self.imageHelper = ImageHelpers()
        self.bovHelper = BOVHelpers(no_clusters)
        self.fileHelper = FileHelpers()
        self.images = None
        self.trainImageCount = 0
        self.train_labels = np.array([])
        self.name_dict = {}
        self.descriptor_list = []

    def TrainModel(self):
        """

        """

        # read file. prepare file lists.
        print("Train ImageCount", self.trainingPath)
        self.images, self.trainImageCount = self.fileHelper.GetFiles(self.trainingPath)
        print("Train ImageCount", self.trainImageCount)
        # extract SIFT/SURF Features from each image
        label_count = 0
        for word, images in self.images.items():
            self.name_dict[str(label_count)] = word
            # print("Computing Features for ", word)
            for image in images:
                # cv2.imshow("im", im)
                # cv2.waitKey()
                self.train_labels = np.append(self.train_labels, label_count)
                kp, des = self.imageHelper.FeaturesExtract(image)
                # print(des)
                self.descriptor_list.append(des)

            label_count += 1

        # print(self.descriptor_list)
        # perform clustering
        self.bovHelper.formatND(self.descriptor_list)
        self.bovHelper.Cluster()
        self.bovHelper.DevelopVocabulary(n_images=self.trainImageCount, descriptor_list=self.descriptor_list)

        # show vocabulary trained
        self.bovHelper.HisttrogramPlotting()

        self.bovHelper.standardize()
        self.bovHelper.train(self.train_labels)

    def recognize(self, test_img, test_image_path=None):

        """
        This method recognizes a single image
        It can be utilized individually as well.


        """

        kp, des = self.imageHelper.FeaturesExtract(test_img)
        # print kp
        print(des.shape)

        # generate vocab for test image
        vocab = np.array([[0 for i in range(self.no_clusters)]])
        # locate nearest clusters for each of
        # the visual word (feature) present in the image

        # testReturnSet =<> return of kmeans nearest clusters for N features
        testReturnSet = self.bovHelper.kmeansObjects.predict(des)
        # print testReturnSet

        # print vocab
        for each in testReturnSet:
            vocab[0][each] += 1

        print(vocab)
        # Scale the features
        vocab = self.bovHelper.scale.transform(vocab)

        # predict the class of the image
        lb = self.bovHelper.clf.predict(vocab)
        # print("Image belongs to class : ", self.name_dict[str(int(lb[0]))])
        return lb

    def TestModel(self):
        """

        read all images from testing path
        use BOVHelpers.predict() function to obtain classes of each image

        """

        self.testImages, self.testImageCount = self.fileHelper.GetFiles(self.testingPath)

        predictions = []

        for word, images in self.testImages.items():
            # print("processing ", word)
            for image in images:
                # print images[0].shape, images[1].shape
                print(image.shape)
                cl = self.recognize(image)
                print(cl)
                predictions.append({
                    'image': image,
                    'class': cl,
                    'object_name': self.name_dict[str(int(cl[0]))]
                })

        print(predictions)
        for each in predictions:
            # cv2.imshow(each['object_name'], each['image'])
            # cv2.waitKey()
            # cv2.destroyWindow(each['object_name'])
            #
            plt.imshow(cv2.cvtColor(each['image'], cv2.COLOR_GRAY2RGB))
            plt.title(each['object_name'])
            plt.show()

    def print_vars(self):
        pass


if __name__ == '__main__':
    # init object
    bagOfWords = BagOfWords(no_clusters=100)

    # set training images paths
    bagOfWords.trainingPath = "download_raw_images/train/"
    # set testing images paths
    bagOfWords.testingPath = "download_raw_images/test/"
    # train the model
    bagOfWords.TrainModel()

    print("Train Model Competed")
    
    # test model
    bagOfWords.TestModel()

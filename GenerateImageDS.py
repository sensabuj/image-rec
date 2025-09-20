from pathlib import Path
# Use built-in range instead of xrange
import os as os
from shutil import copyfile
import random
import shutil
"""
- images/ ** this is the parent image folder
    |- test /
        |- obj1/
        |- obj2/
    |- train /
        |- obj1/
        |- obj2/
"""


# let us make a clone of the image folder structure
# default training data is 70%. Change this as you want
def cloneParentImageFolder(parentPath, ratio=70):
    # lets imagine that w want to create these two 
    # new folders [test and train] in the parent dir
    dirList = getTheListOfSubDirectories(parentPath)

    for dirList in dirList:
        # initialize the folder clone back to false
        train = False
        test = False

        # create individual sub directory
        # return the dir name and the status
        tr_subDir, train = createDir(parentPath, "train", dirList)  # create the train
        te_subDir, test = createDir(parentPath, "test", dirList)  # create the test

        if train == test:
            # print("done")
            pass

        # lets collect all the images in this diectory into a list and index them
        imgCollection = next(os.walk(parentPath + "\\" + dirList))[2]

        # lets count how many images this directory has
        imgCount = len(imgCollection)

        # now lets find the stopping point of images to go int training folder
        trainFileCoult = int(round(imgCount * (ratio / 100)))  # we use round becuse we are going to to be
        # indexing a list and we do not want decimals
        # that will give us an error!

        # lets do something nice! Lets note take the image in the sequential manner they come in the folder
        # lets pict them randomly. How ever, the size must  macth the total count items in the folder
        my_randoms = random.sample(range(imgCount), imgCount)

        # now these files go to the train
        for randIteration in my_randoms[0:trainFileCoult]:
            source = parentPath + "\\" + dirList + "\\" + imgCollection[int(randIteration)]
            dest = tr_subDir + "\\" + imgCollection[int(randIteration)]
            print("Completed --> ", copyfile(str(source), str(dest)))

        # now for the test
        for randIteration in my_randoms[trainFileCoult + 1:imgCount]:
            source = parentPath + "\\" + dirList + "\\" + imgCollection[int(randIteration)]
            dest = te_subDir + "\\" + imgCollection[int(randIteration)]
            print("Completed --> ", copyfile(str(source), str(dest)))



# get the list of all dir in the parent
def getTheListOfSubDirectories(parentDir):
    # get the list of folder names
    dirName = []
    for _, _dir, _ in os.walk(str(parentDir)):
        if len(_dir) > 0:
            dirName.append(_dir)
    return dirName[0]


# parentDir, type[test or train], name_of_sub_dir
def createDir(parentPath, typeOfDir, _1_level_sub_dir):
    # string to get the full path
    fullDir = str(parentPath + "\\" + typeOfDir + "\\" + _1_level_sub_dir)
    # str() not needed but just to be on the safe side

    # if directory does not exist just create a new one
    if not os.path.exists(fullDir):
        os.makedirs(fullDir)

    # just confirm if theh folder was created
    # computers! sometimes you just cnt trust them enough ^..^
    # tell us the path was created and giev usthe name to confirm
    return fullDir, Path(fullDir).exists()


def main():
    parentPath = "E:\\@master_repo\\training\\python\\basic\\download_raw_images"
    dirList = getTheListOfSubDirectories(parentPath)
    cloneParentImageFolder(parentPath, ratio=70)
    for dirList in dirList:
        shutil.rmtree(parentPath + "\\" + dirList)


if __name__ == "__main__":
    main()

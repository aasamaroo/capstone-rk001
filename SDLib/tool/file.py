import os.path
from os import makedirs,remove
from re import compile,findall,split
from config import LineConfig
from collections import defaultdict
class FileIO(object):
    def __init__(self):
        pass

    # @staticmethod
    # def writeFile(filePath,content,op = 'w'):
    #     reg = compile('(.+[/|\\\]).+')
    #     dirs = findall(reg,filePath)
    #     if not os.path.exists(filePath):
    #         os.makedirs(dirs[0])
    #     with open(filePath,op) as f:
    #         f.write(str(content))

    @staticmethod
    def writeFile(dir,file,content,op = 'w'):
        if not os.path.exists(dir):
            os.makedirs(dir)
        if type(content)=='str':
            with open(dir + file, op) as f:
                f.write(content)
        else:
            with open(dir+file,op) as f:
                f.writelines(content)

    @staticmethod
    def deleteFile(filePath):
        if os.path.exists(filePath):
            remove(filePath)

    @staticmethod
    def loadDataSet(conf, file, bTest=False):
        trainingData = defaultdict(dict)
        testData = defaultdict(dict)
        ratingConfig = LineConfig(conf['ratings.setup'])
        if not bTest:
            print 'loading training data...'
        else:
            print 'loading test data...'
        with open(file) as f:
            ratings = f.readlines()
        # ignore the headline
        if ratingConfig.contains('-header'):
            ratings = ratings[1:]
        # order of the columns
        order = ratingConfig['-columns'].strip().split()

        for lineNo, line in enumerate(ratings):
            items = split(' |,|\t', line.strip())
            if not bTest and len(order) < 3:
                print 'The rating file is not in a correct format. Error: Line num %d' % lineNo
                exit(-1)
            try:
                userId = items[int(order[0])]
                itemId = items[int(order[1])]
                if bTest and len(order)<3:
                    rating = 1 #default value
                else:
                    rating  = items[int(order[2])]

            except ValueError:
                print 'Error! Have you added the option -header to the rating.setup?'
                exit(-1)
            if not bTest:
                trainingData[userId][itemId]=float(rating)
            else:
                testData[userId][itemId] = float(rating)
        if not bTest:
            return trainingData
        else:
            return testData

    @staticmethod
    def loadRelationship(conf, filePath):
        socialConfig = LineConfig(conf['social.setup'])
        relation = []
        print 'loading social data...'
        with open(filePath) as f:
            relations = f.readlines()
            # ignore the headline
        if socialConfig.contains('-header'):
            relations = relations[1:]
        # order of the columns
        order = socialConfig['-columns'].strip().split()
        if len(order) <= 2:
            print 'The social file is not in a correct format.'
        for lineNo, line in enumerate(relations):
            items = split(' |,|\t', line.strip())
            if len(order) < 2:
                print 'The social file is not in a correct format. Error: Line num %d' % lineNo
                exit(-1)
            userId1 = items[int(order[0])]
            userId2 = items[int(order[1])]
            if len(order) < 3:
                weight = 1
            else:
                weight = float(items[int(order[2])])
            relation.append([userId1, userId2, weight])
        return relation


    @staticmethod
    def loadLabels(filePath):
        labels = {}
        with open(filePath) as f:
            for line in f:
                items = split(' |,|\t', line.strip())
                labels[items[0]] = items[1]
        return labels



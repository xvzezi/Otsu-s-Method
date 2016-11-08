class ByteOtsu:
    """
    Class: Byte Otsu
        It takes in bytes stream, and output the result in
    user's demand.
        It provides get_binary()        # return the bytes of bin-image
                    get_foreground()    # make the background 0
                    get_background()    # make the foreground 255

    Alert: Because we use the basic integer object, it can process not-so-
           big data. In this class, you are not allowed to change a image
           content.
    """

    def __init__(self, grayLevel, ignore = []):
        '''
        Constructor
            We get in some bytes data, and will pre-process on that. ignore is
        a list of 0~255, indicate which kind of pixel gray level is not allowed
        to be counted.
        :param grayLevel: bytes stream
        :param ignore: unwanted gray level sets
        '''

        # check if ignore and grayLevel is good enough
        if not isinstance(ignore, list):
            ignore = []
        if not isinstance(grayLevel, bytes):
            grayLevel = bytes()

        # assign the data values
        self._ignore = ignore
        self.gray = grayLevel

        # pre-process
        self.threshold = 0
        self.run_pre_pro()

    ###################################### process the data ###################################

    def getMeanBefore(self, index, statistics):
        means = 0
        for i in range(0, index):
            means += i * statistics[i]
        return means

    def getProbBefore(self, index, statistics):
        prob = 0
        for i in range(0, index):
            prob += statistics[i]
        return prob

    def run_pre_pro(self):
        '''
        Pre Process Function
        :return: None
        '''
        # run the statistics
        amount = len(self.gray)
        ignore_count = 0
        statistics = [0] * 256
        for i in range(0, amount):
            s_index = self.gray[i]
            if s_index not in self._ignore:
                statistics[s_index] += 1
            else:
                ignore_count += 1

        # get basic mean
        mean_of_all = 0
        for i in range(0, 256):
            statistics[i] = statistics[i] * 1.0 / (amount - ignore_count)
            mean_of_all += i * statistics[i]

        # process and get the result
        result = [0] * 256
        left_prob = 0
        right_prob = 0
        for t in range(0, 256):
            # raw mean
            tempo = self.getMeanBefore(t, statistics)
            # prob
            left_prob = self.getProbBefore(t, statistics)
            if left_prob == 0 or left_prob == 1:
                continue
            right_prob = 1 - left_prob
            # right mean
            tar = tempo / left_prob - (mean_of_all - tempo) / right_prob
            result[t] = tar * tar * left_prob * right_prob

        # get the threshold
        maxRe = 0
        thres = 0
        for i in range(0, 256):
            if result[i] > maxRe:
                maxRe = result[i]
                thres = i
        self.threshold = thres
        print("get thres %d with %d anti %d" % (thres, result[thres], result[183]))

    ###################################### fetch the data ###################################

    def get_binary(self):
        print("bin %d" % self.threshold)
        amount = len(self.gray)
        newImg = [0] * amount
        for i in range(0, amount):
            if self.gray[i] < self.threshold:
                newImg[i] = 0
            else:
                newImg[i] = 255
        return bytes(newImg)

    def get_foreground(self):
        print("fore %d" % self.threshold)
        amount = len(self.gray)
        newImg = [0] * amount
        for i in range(0, amount):
            if self.gray[i] < self.threshold:
                newImg[i] = 0
            else:
                newImg[i] = self.gray[i]
        return bytes(newImg)

    def get_background(self):
        print("back %d" % self.threshold)
        amount = len(self.gray)
        newImg = [0] * amount
        for i in range(0, amount):
            if self.gray[i] >= self.threshold:
                newImg[i] = 255
            else:
                newImg[i] = self.gray[i]
        return bytes(newImg)

    def get_anti_sigh(self):
        print("anti %d" % self.threshold)
        amount = len(self.gray)
        newImg = [0] * amount
        for i in range(0, amount):
            if self.gray[i] >= self.threshold:
                newImg[i] = 0
            else:
                newImg[i] = self.gray[i]
        return bytes(newImg)
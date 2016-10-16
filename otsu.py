from PIL import Image

class MyOtsuMethod:
    """
    This Class implements a way to read in a gray level image,
    and apply otsu's method onto that. it will provide a binary
    image, with 0 and 255 to present.
    """
    def __init__(self, file_path):
        '''
        init the needed data
        :param file_path:
        '''
        # png img handler
        self.img = Image.open(file_path)
        self.img = self.img.convert('L')
        # probabilities
        self.left_prob = 0
        self.right_prob = 1
        # means
        self._mean = 0
        self.result = [0] * 256
        # gay-level bytes
        self.gray = bytes()
        # statistics
        self.statistics = [0] * 256
        self.sta_size = 0
        # run and get gay-level image
        self.gray = self.img.tobytes()
        self.run_statistics()
        self.run_analysis()

    def run_statistics(self):
        self.sta_size = len(self.gray)
        for i in range(0, self.sta_size):
            self.statistics[self.gray[i]] += 1
        # convert into probability and get the means
        for i in range(0, 256):
            self.statistics[i] = self.statistics[i] * 1.0 / self.sta_size
            self._mean += i * self.statistics[i]

    def getMeanBefore(self, index):
        means = 0
        for i in range(0, index):
            means += i * self.statistics[i]
        return means

    def getProbBefore(self, index):
        prob = 0
        for i in range(0, index):
            prob += self.statistics[i]
        return prob

    def run_analysis(self):
        for t in range(0, 256):
            # raw mean
            tempo = self.getMeanBefore(t)
            # prob
            self.left_prob = self.getProbBefore(t)
            if self.left_prob == 0 or self.left_prob == 1:
                continue
            self.right_prob = 1 - self.left_prob
            # right mean
            tar = tempo / self.left_prob - (self._mean - tempo) / self.right_prob
            self.result[t] = tar * tar * self.left_prob * self.right_prob

    def get_threshold(self):
        maxRe = 0
        thres = 0
        for i in range(0, 256):
            if self.result[i] > maxRe:
                maxRe = self.result[i]
                thres = i
        return thres

    def process_gray_level(self):
        threshold = self.get_threshold()
        newImg = [0] * self.sta_size
        for i in range(0, self.sta_size):
            if self.gray[i] < threshold:
                newImg[i] = 0
            else:
                newImg[i] = 255
        self.img.frombytes(bytes(newImg))

    def get_bytes(self):
        return self.gray

    def saveTo(self, path):
        self.img.save(path)

    def show(self):
        self.img.show()



def test_main():
    otsu = MyOtsuMethod('D:/source.jpg')
    otsu.process_gray_level()
    print(otsu.get_threshold())
    otsu.saveTo("D:/house_otsu.jpg")

test_main()




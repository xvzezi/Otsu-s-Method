from PIL import Image

from otsu.ByteOtsu import ByteOtsu


class OstuCherry:
    def __init__(self, path):
        self.img = Image.open(path).convert('L')
        self.imgBytes = self.img.tobytes()
        self.processor = ByteOtsu(self.imgBytes)

    def saveTo(self, path, type='B'):
        newImg = None
        if type == 'F':
            newImg = self.processor.get_foreground()
        elif type == 'BA':
            newImg = self.processor.get_background()
        else:
            newImg = self.processor.get_binary()
        self.img.frombytes(newImg)
        self.img.save(path)

    def cutTheBruiseAndSave(self, path):
        newImg = self.processor.get_foreground()
        newPro = ByteOtsu(newImg, [0])
        newImg = newPro.get_anti_sigh()
        self.img.frombytes(newImg)
        self.img.save(path)



def test_main():
    otsu = OstuCherry('D:/cherry.png')
    # otsu.saveTo('D:/back.png', type='BA')
    # otsu.saveTo('D:/fore.png', type='F')
    otsu.cutTheBruiseAndSave('D:/bru.png')

test_main()
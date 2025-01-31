from PIL.Image import open


class Image:
    """
    Image:
        图像检索系统中使用的表示图像的基类，应在该类的基础上派生类来绑定与图片相关的信息
    PILObj: 
        使用PIL库打开图像的对象类型
    feature:
        图像检索系统计算出的图像的特征向量
    ID:
        图片对应的ID
    """

    def __init__(self, image_dir=None, ID=None):
        self.ID = ID
        if image_dir == None:
            self.PILObj = None
        else:
            self.PILObj = open(image_dir)
            if self.PILObj.mode == 'RGBA':
                self.PILObj = self.PILObj.convert('RGB')
        self.feature = None

    def open(self, image_dir):
        """
        open:
            使用该函数来获得self.PILObj
        image_dir: str
            图像的路径
        """
        self.PILObj = open(image_dir)
        if self.PILObj.mode == 'RGBA':
            self.PILObj = self.PILObj.convert('RGB')

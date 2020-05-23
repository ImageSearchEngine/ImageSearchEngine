from PIL.Image import open


class Image:
    """
    Image:
        图像检索系统中使用的表示图像的基类，应在该类的基础上派生类来绑定与图片相关的信息
    PILObj: 
        使用PIL库打开图像的对象类型
    feature:
        图像检索系统计算出的图像的特征向量
    """

    def __init__(self):
        self.PILObj = None
        self.feature = None

    def open(self, image_dir):
        """
        open:
            使用该函数来获得self.PILObj
        image_dir: str
            图像的路径
        """
        self.PILObj = open(image_dir)

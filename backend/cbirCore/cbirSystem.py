from cbirCore.multigrain.lib import get_multigrain
from cbirCore.multigrain.utils import cuda
from cbirCore.multigrain.augmentations import get_transforms
import torch
import numpy as np
import gc


class CBIRSystem:

    def __init__(self):
        self.model = get_multigrain('pnasnet5large', include_sampling=False)
        if torch.cuda.is_available():
            self.model = cuda(self.model)
        self.model.eval()
        self.transform = get_transforms(crop=False, need=(
            'val'), backbone='pnasnet5large')['val']
        self.dataset = []
        self.ckpt_loaded = self.dataset_loaded = False

    def load_checkpoint(self, ckpt_dir):
        """
        load_checkpoint: 
            加载模型的参数，在使用检索系统之前一定要调用
        ckpt_dir: str
            模型参数的路径，下载地址为https://dl.fbaipublicfiles.com/multigrain/finetuned_models/pnasnet5large-finetune500.pth
        """
        checkpoint = torch.load(ckpt_dir)
        self.model.load_state_dict(checkpoint['model_state'])
        self.ckpt_loaded = True

    def load_image(self, image):
        """
        load_image:
            加载到检索系统中一张图片，使用检索系统之前请多次调用
        image: class Image
            加载进检索系统中的图片，要求是Image类的派生类，注意系统直接image引用上更改
        """
        img = self.transform(image.PILObj)
        img = torch.unsqueeze(img, dim=0)
        if torch.cuda.is_available():
            img = cuda(img)
        with torch.no_grad():
            output_dict = self.model(img)
        feature = output_dict['normalized_embedding'].detach().cpu().numpy()[0]
        image.feature = feature
        del image.PILObj  # 释放图片占用的内存
        gc.collect()
        self.dataset.append(image)
        self.dataset_loaded = True

    # def load_data(self, data_dir):
    #     """
    #     load_data:
    #         加载预处理好的数据，不用使用load_image了
    #     images: list of class Image
    #         检索的所有图片，列表中的每一项都是Image类的派生类
    #     """
    #     self.dataset = images
    #     for image in self.dataset:
    #         img = self.transform(image.PILObj)
    #         img = torch.unsqueeze(img, dim=0)
    #         if torch.cuda.is_available():
    #             img = cuda(img)
    #         with torch.no_grad():
    #             output_dict = self.model(img)
    #         feature = output_dict['normalized_embedding'].detach().cpu().numpy()[
    #             0]
    #         image.feature = feature
    #     self.dataset_loaded = True

    def _loss(self, x1, x2):
        return np.linalg.norm(x1-x2, 2)

    def retrieve_image(self, image_r, number=0):
        """
        retrieve_image: list of class Image
            使用图片检索系统，返回一个根据相关度排序好的Image类派生类的列表，
        image_r: class Image
            检索的图片，是Image类的派生类
        number: int
            希望得到结果数量，number<=0表示返回整个图像库的排序
        """
        assert self.ckpt_loaded and self.dataset_loaded
        img_r = self.transform(image_r.PILObj)
        img_r = torch.unsqueeze(img_r, dim=0)
        if torch.cuda.is_available():
            img_r = cuda(img_r)
        with torch.no_grad():
            output_dict = self.model(img_r)
        feature = output_dict['normalized_embedding'].detach().cpu().numpy()[0]
        image_r.feature = feature
        self.dataset.sort(key=lambda image: self._loss(
            image.feature, image_r.feature))
        if number <= 0:
            return self.dataset
        else:
            return self.dataset[:number]

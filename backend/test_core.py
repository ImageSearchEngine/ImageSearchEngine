from cbirCore import CBIRSystem, Image
import os
system = CBIRSystem()

system.load_checkpoint('static/pnasnet5large-finetune500.pth')

# 使用以下方法只需计算一次，之后的话加载数据使用load_data

# image_path = '../cbir-core/data/jpg/'

# image_ids = os.listdir(image_path)
# for image_id in image_ids:
#     system.load_image(Image(image_id[:-4], image_path+image_id))
#     print(image_id)
# system.save_data('static/')

# 保存之后再加载图库只需使用load

system.load_data('static/')
print(len(system.dataset))

from cbirCore import CBIRSystem, Image

system = CBIRSystem()

system.load_checkpoint('static/pnasnet5large-finetune500.pth')

# 使用以下方法只需计算一次，之后的话加载数据使用load_data

image_path = '../cbir-core/data/jpg/'
image_ids = [
    '132301.jpg',
    '136002.jpg',
    '138502.jpg',
    '141802.jpg',
    '146200.jpg']
for image_id in image_ids:
    system.load_image(Image(image_id, image_path+image_id))
system.save_data('static/')

# 保存之后再加载图库只需使用load

system.load_data('static/')
print(len(system.dataset))

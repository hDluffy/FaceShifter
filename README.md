# FaceShifter
Try to reproduce FaceShifter </br>
基于taotaonice/FaceShifter做了简单调整，后续进一步改进
# up 
## 2021/4/29
在face_modules/preprocess_images.py和train_AEI.py中添加argparse解析，方便外部设置参数
## 2021/5/6
在train_AEI.py中设置每10000次迭代保存一次模型，每show_step后保存一次中间结果

# make data
cd face_modules </br>
python preprocess_images.py -s <img_root_dir> -t <save_path>

# train
cd ../ </br>
python train_AEI -sm './saved_models' -ip <images_path> -sp 0.8 -lid 5

# demo
python inference_demo.py -s ./src.jpg -t ./tag.jpg

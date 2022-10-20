task_num='Triple'

if [ ${task_num} = 'Triple' ];then
    CUDA_VISIBLE_DEVICES=6,7 \
    python TrainTriple_AEI.py -sm './saved_models' -ip /data2/jiaqing/face_swap/tx_india -sp 0.8 -lid 10
fi

if [ ${task_num} = 'Shift' ];then
    CUDA_VISIBLE_DEVICES=2,3,4,5,6,7 \
    python train_AEI.py -sm './saved_models' -ip /data2/jiaqing/FaceShifter/FaceSwap_256 -sp 0.8 -lid 10
fi
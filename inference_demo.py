import sys
sys.path.append('./face_modules/')
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
from face_modules.model import Backbone, Arcface, MobileFaceNet, Am_softmax, l2_norm
from network.AEI_Net import *
from face_modules.mtcnn import *
import cv2
import PIL.Image as Image
import numpy as np
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--Xs_path', default='./src.jpg', metavar='STR',
                    help='Xs_path')
parser.add_argument('-t', '--Xt_path', default='./tag.jpg', metavar='STR',
                    help='Xt_path')
args = parser.parse_args()

detector = MTCNN()
device = torch.device('cuda')
G = AEI_Net(c_id=512)
G.eval()
G.load_state_dict(torch.load('./saved_models/G_latest.pth', map_location=torch.device('cpu')))
G = G.cuda()

arcface = Backbone(50, 0.6, 'ir_se').to(device)
arcface.eval()
arcface.load_state_dict(torch.load('./face_modules/model_ir_se50.pth', map_location=device), strict=False)

test_transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

Xs_path = args.Xs_path
Xt_path = args.Xt_path

Xs_raw = cv2.imread(Xs_path)
Xt_raw = cv2.imread(Xt_path)
Xs = detector.align(Image.fromarray(Xs_raw), crop_size=(256, 256))
Xt = detector.align(Image.fromarray(Xt_raw), crop_size=(256, 256))

Xs_raw = np.array(Xs)
Xt_raw = np.array(Xt)

Xs = test_transform(Xs)
Xt = test_transform(Xt)

Xs = Xs.unsqueeze(0).cuda()
Xt = Xt.unsqueeze(0).cuda()
with torch.no_grad():
    embeds, _ = arcface(F.interpolate(Xs[:, :, 19:237, 19:237], (112, 112), mode='bilinear', align_corners=True))
    embedt, __ = arcface(F.interpolate(Xt[:, :, 19:237, 19:237], (112, 112), mode='bilinear', align_corners=True))
    Yt, _ = G(Xt, embeds)
    Ys, _ = G(Xs, embedt)
    Ys = Ys.squeeze().detach().cpu().numpy().transpose([1, 2, 0])*0.5 + 0.5
    Yt = Yt.squeeze().detach().cpu().numpy().transpose([1, 2, 0])*0.5 + 0.5

    Y = np.concatenate((Ys, Yt), axis=1)
    X = np.concatenate((Xs_raw/255., Xt_raw/255.), axis=1)
    image = np.concatenate((X, Y), axis=0)
    cv2.imshow('image', image)
    cv2.waitKey(0)

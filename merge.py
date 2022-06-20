import os
import sys
import cv2
import numpy as np

WIDTH = 1920
HEIGHT = 1080

def read_info(path):#os.curdir+path
    path_upd = path + "/"
    _files = [f for f in os.listdir(path) if os.path.isfile(path_upd+f)]
    _dir = [d for d in os.listdir(path) if os.path.isdir(path_upd+d)]    
    return(_files, _dir)

def extract_frames(file):
    cap_vid = cv2.VideoCapture(file)
    frameCount = int(cap_vid.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap_vid.get(cv2.CAP_PROP_FPS))
    count = 0
    frame, image = cap_vid.read()
    buf = np.empty((frameCount, 540, 640, 3), np.dtype('uint8'))
    while frame:
        img = cv2.resize(image, (640, 540))
        buf[count] = img
        frame, image = cap_vid.read()
        count += 1
    cap_vid.release()
    return buf, fps

def stitch_frames(img_1, img_2, img_3, img_4, img_5, img_6):
    _tmp_up = np.hstack((img_1,img_2,img_3))
    _tmp_down = np.hstack((img_4, img_5, img_6))
    return(np.vstack((_tmp_up, _tmp_down)))

def make_video(path, file, fps = 30):
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (file.shape[2], file.shape[1]))
    for i in range(file.shape[0]):
        data = file[i]
        out.write(data)
    #out.release()
    
if __name__ == "__main__":
    #path = os.curdir+"//"+sys.argv[1]
    #files, dir = read_info(path)
    vid_01, fps = extract_frames("video.mp4")
    vid_02, fps = extract_frames("video.mp4")
    vid_03, fps = extract_frames("video.mp4")
    imgblank = np.zeros((540,640,3), np.uint8)
    #files = [001.txt, 002.txt, 003.txt]
    buf = np.empty((vid_01.shape[0], HEIGHT, WIDTH, 3), np.dtype('uint8'))
    for i in range(vid_01.shape[0]):
         buf[i] = stitch_frames(vid_01[i], imgblank, vid_02[i], imgblank, vid_03[i], imgblank)
    make_video("sa.mp4", buf)
 #   cv2.imshow("",r)
 #   cv2.waitKey(0)
    

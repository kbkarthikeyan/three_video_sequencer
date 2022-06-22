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
    print("\nCreating Video..")
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (file.shape[2], file.shape[1]))
    progress_bar(0, file.shape[0])
    for i in range(file.shape[0]):
        data = file[i]
        out.write(data)
        progress_bar(i, file.shape[0])
    out.release()
    print("\nConversion Successful")
    
def progress_bar(progress, total):
        percent = 100*(progress/float(total))
        bar = '#'*int(percent) + '-'*(100 - int(percent))
        print(f"\r|{bar}|{percent:.2f}%", end = "\r")
        
if __name__ == "__main__":
    path = os.curdir+"//"+sys.argv[1]
    files, dir = read_info(path)
    tmp = []
    print("Please wait loading files... ")
    for f in files:
        if ".mp4" in f:
                new_path = path+"/"+f
                #print(new_path)
                tmp.append(new_path)
    progress_bar(0, len(tmp))
    vid_01, fps = extract_frames(tmp[0])
    progress_bar(1, len(tmp))
    vid_02, fps = extract_frames(tmp[1])
    progress_bar(2, len(tmp))
    vid_03, fps = extract_frames(tmp[2])
    progress_bar(3, len(tmp))
    print("\nFiles loaded..")
    imgblank = np.zeros((540,640,3), np.uint8)
    buf = np.empty((vid_01.shape[0], HEIGHT, WIDTH, 3), np.dtype('uint8'))
    for i in range(vid_01.shape[0]):
         buf[i] = stitch_frames(vid_01[i], imgblank, vid_02[i], imgblank, vid_03[i], imgblank)
    make_video(sys.argv[2], buf, fps = fps)
    #cv2.imshow("",vid_01[1])
    #cv2.waitKey(0)

import os
import sys
import cv2

def read_info(path):#os.curdir+path
    path_upd = path + "/"
    _files = [f for f in os.listdir(path) if os.path.isfile(path_upd+f)]
    _dir = [d for d in os.listdir(path) if os.path.isdir(path_upd+d)]    
    _tmp = []
    return(_files, _dir)

def extract_frames(file):
    tmp = []
    cap_vid = cv2.VideoCapture(file)
    frame, image = cap_vid.read()
    count = 0
    while frame:
        img = cv2.resize(image, (640, 360))
        tmp.append(img)
        frame, image = cap_vid.read()
        count += 1
    print(count)    
    return tmp

if __name__ == "__main__":
    #path = os.curdir+"//"+sys.argv[1]
    #files, dir = read_info(path)
    t = extract_frames("video.mp4")
    print(len(t))
    #files = [001.txt, 002.txt, 003.txt]
    cv2.imshow("",t[10])
    cv2.waitKey(0)
    
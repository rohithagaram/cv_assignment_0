import numpy as np
import cv2
from threading import Thread
import argparse
import os

def matting(b1, b2, c1, c2 ,bg,cnt):

    b1_r, b1_g, b1_b = b1[:,:,0], b1[:,:,1], b1[:,:,2]    
    b2_r, b2_g, b2_b = b2[:,:,0], b2[:,:,1], b2[:,:,2]    
    c1_r, c1_g, c1_b = c1[:,:,0], c1[:,:,1], c1[:,:,2]
    c2_r, c2_g, c2_b = c2[:,:,0], c2[:,:,1], c2[:,:,2]
    
    img_shape = b1.shape # all images have same shape
    fg = np.zeros(img_shape)
    alpha = np.zeros(img_shape[:2])
    
    matrix = np.array([[1,0,0,1,0,0],[0,1,0,0,1,0],[0,0,1,0,0,1]])
    
    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            a = np.array([b1_r[i,j],b1_g[i,j],b1_b[i,j],b2_r[i,j],b2_g[i,j],b2_b[i,j]])
            b = np.array([c1_r[i,j]-b1_r[i,j],c1_g[i,j]-b1_g[i,j],c1_b[i,j]-b1_b[i,j],c2_r[i,j]-b2_r[i,j],c2_g[i,j]-b2_g[i,j],c2_b[i,j]-b2_b[i,j]])
            A = np.vstack((matrix, -1*a))
            x = np.clip(np.dot(b,np.linalg.pinv(A)), 0.0, 1.0)
            fg[i,j] = np.array([x[0], x[1], x[2]])
            alpha[i,j] = x[3]
    
    b = np.zeros(new_bg.shape)
    b[:,:,0] = new_bg[:,:,0] * (1-alpha)
    b[:,:,1] = new_bg[:,:,1] * (1-alpha)
    b[:,:,2] = new_bg[:,:,2] * (1-alpha)
    
    composite = fg + b
    file_name = 'fg_output/'+str(cnt)+'.jpg'
    cv2.imwrite(file_name, fg*255.0)
    file_name = 'alpha_output/'+str(cnt)+'.jpg'
    cv2.imwrite(file_name, alpha*255.0)
    file_name = 'output/'+str(cnt)+'.jpg'
    cv2.imwrite(file_name, composite*255.0)
    


 
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--new_bg",
                         type=str,
                         help="new_bg_video",
                         default="new_bg.mp4")
    parser.add_argument("--blue_vid",
                         type=str,
                         help="blue_screen_video",
                         default="blue_screen.mp4")
    parser.add_argument("--green_vid",
                         type=str,
                         help="green_screen_video",
                         default="green_screen.mp4")
    parser.add_argument("--blue_bg_img",
                         type=str,
                         help="blue_bg_image",
                         default="blue.jpg")
    parser.add_argument("--green_bg_img",
                         type=str,
                         help="green_bg_img",
                         default="green.jpg")
    parser.add_argument("--num_threads",
                         type=str,
                         help="num_threads",
                         default="4")
                         
    options = parser.parse_args() 
    
    new_bg_video_file_name = options.new_bg
    c1_video_file_name = options.blue_vid
    c2_video_file_name = options.green_vid
    b1_file_name = options.blue_bg_img
    b2_file_name = options.green_bg_img
    num_threads = int(options.num_threads)
    
    if(os.path.isdir("output") == False):
            os.mkdir("output")
    if(os.path.isdir("alpha_output") == False):
            os.mkdir("alpha_output")
    if(os.path.isdir("fg_output") == False):
            os.mkdir("fg_output")
    
    bg_cap = cv2.VideoCapture(new_bg_video_file_name)
    c1_cap = cv2.VideoCapture(c1_video_file_name)
    c2_cap = cv2.VideoCapture(c2_video_file_name)
    
    bg_frames_cnt = int(bg_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    c1_frames_cnt = int(c1_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    c2_frames_cnt = int(c2_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    total_frames = 0
    
    if(bg_frames_cnt < c1_frames_cnt) and (bg_frames_cnt < c1_frames_cnt):
        total_frames = bg_frames_cnt
    elif (c1_frames_cnt < bg_frames_cnt) and (c1_frames_cnt < c2_frames_cnt):
        total_frames = c1_frames_cnt
    else :
        total_frames = c2_frames_cnt
    
    
    b1 = cv2.imread(b1_file_name)
    b2 = cv2.imread(b2_file_name)
    b1 = cv2.resize(b1, (640, 480),interpolation = cv2.INTER_NEAREST)
    b2 = cv2.resize(b2, (640, 480),interpolation = cv2.INTER_NEAREST)
    b1 = b1/255.0
    b2 = b2/255.0
    
    threads = [];
    ff = 0;
    iterations = total_frames/num_threads
    cnt = 0
    for i in range(int(iterations)):
        for k in range(num_threads):
            
            if(((i*num_threads)+k+1) == total_frames):
                break
            ret, new_bg = bg_cap.read()
            ret, c1 = c1_cap.read()
            ret, c2 = c2_cap.read()

            new_bg = cv2.resize(new_bg, (640, 480),interpolation = cv2.INTER_NEAREST)
            c1 = cv2.resize(c1, (640, 480),interpolation = cv2.INTER_NEAREST)
            c2 = cv2.resize(c2, (640, 480),interpolation = cv2.INTER_NEAREST)
            
            c1 = c1/255.0
            c2 = c2/255.0
            new_bg = new_bg/255.0

    
            cnt = cnt + 1
            t = Thread(target=matting, args=(b1,b2,c1,c2,new_bg,cnt))
            t.start()
            if(ff == 0):
                threads.append(t)
                ff= 1
            else:
                threads.insert(k,t)
            
        for thread in threads:
            thread.join()
    

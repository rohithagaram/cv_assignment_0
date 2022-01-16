
import cv2
import argparse
import os

def main(options) :
    if options.video2img == True :

        if(os.path.isdir(options.dest_path) == False):
            os.mkdir(options.dest_path)
            
        cap = cv2.VideoCapture(options.data_path)
        
        if (cap.isOpened() == False):
            print("Error in the opeing of the video file")
          
        i=0
        while(cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                filename = options.dest_path+"/"+str(i)+".jpg"
                
                cv2.imwrite(filename, frame)
                img = cv2.imread(filename)
            else: 
                print("Issue in Reading the file")
                break

        cap.release()
    else :
        file_names = os.listdir(options.data_path)
        file_size = len(file_names)
        img = cv2.imread(options.data_path+ "/"+file_names[0])
        height = img.shape[0]
        width = img.shape[1]
        size = (img.shape[1] , img.shape[0])
        video_path = options.dest_path + "/" + "result.avi"
        fps = options.fps
        result = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'MJPG'),fps, size) 
        
        for i in range(file_size):
     
            file_name_n = options.data_path+ "/" + "final_"+str(i)+".jpg"
            print(file_name_n)
            img = cv2.imread(file_name_n)
            if (img.shape[1] != width or img.shape[0] != height) :
                img = cv2.resize(img, (width, height))
        
            result.write(img)
        result.release()
    
        
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path",
                         type=str,
                         help="video_path",
                         default="C:/Users/Manasa/Documents/triangulation-matting/green_screen.mp4")
    parser.add_argument("--dest_path",
                         type=str,
                         help="destination_path",
                         default="C:/Users/Manasa/Documents/triangulation-matting/green")
    
    parser.add_argument("--video2img",
                         dest = 'video2img',
                         action='store_true',
                         help="conversion type",
                          )
                         
    parser.add_argument("--fps",
                         type=int,
                         help="frame_rate",
                         default=30)
    options = parser.parse_args()
    main(options)

import cv2
import argparse
cap = cv2.VideoCapture(0)
currentFrame = 0

print("Enter q to exit")
print("Enter c to capture")

def capture(options):
    while(True):

        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        cv2.imshow('frame',frame)
        
        if cv2.waitKey(1) & 0xFF == ord('c'):
            filename = options.dest_path+"/"+str(currentFrame)+".jpg"
            cv2.imwrite(filename, frame)
            currentFrame += 1
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        
    cap.release()
    cv2.destroyAllWindows()
 
if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest_path",
                         type=str,
                         help="destination_path",
                         default="C:/Users/Manasa/Downloads/test/")
    options = parser.parse_args()
    capture(options)
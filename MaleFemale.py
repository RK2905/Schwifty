import cv2
import os
from PIL import Image
import numpy as np

cascadepath="haarcascade_frontalface_default.xml"
facecascade=cv2.CascadeClassifier(cascadepath)

font=cv2.FONT_HERSHEY_SIMPLEX
recognizer=cv2.face.createFisherFaceRecognizer()

def get_images(path):
    m_path=path+'/Male/'    
    m_image_path = [os.path.join(m_path, f) for f in os.listdir(m_path) if not f=='Thumbs.db'] 
    f_path=path+'/Female/'    
    f_image_path = [os.path.join(f_path, f) for f in os.listdir(f_path) if not f=='Thumbs.db']  
    
    images=[]
    labels=[]

    for image_path in m_image_path:
        image_pil=Image.open(image_path).convert('L')
        image=np.array(image_pil,'uint8')
        faces=facecascade.detectMultiScale(image)
        for (x,y,w,h) in faces:
            temp=cv2.resize(image[y:y+h,x:x+h],(100,100))
            images.append(temp)
            labels.append(1);
            cv2.imshow("Adding Faces To Training Set.....",temp)
            cv2.waitKey(1)
            
    for image_path in f_image_path:
        image_pil=Image.open(image_path).convert('L')
        image=np.array(image_pil,'uint8')
        faces=facecascade.detectMultiScale(image)
        for (x,y,w,h) in faces:
            temp=cv2.resize(image[y:y+h,x:x+h],(100,100))
            images.append(temp)
            labels.append(0);
            cv2.imshow("Adding Faces To Training Set.....",temp)
            cv2.waitKey(1)
    
    return images,labels
    
path='./Celebs'

images,labels=get_images(path)
cv2.destroyAllWindows()

print('Training Images....')
recognizer.train(images,np.array(labels))
print('Training Complete....')

cap=cv2.VideoCapture('faces.mp4')

male=0
female=0
no_frames=0

while True:
    _,frame=cap.read()
    no_frames=(no_frames+1)
    if _==False:
        break
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces=facecascade.detectMultiScale(gray)

    for (x,y,w,h) in faces:
         temp=cv2.resize(gray[y: y + h, x: x + w],(100,100))
         
         result = cv2.face.MinDistancePredictCollector()
         recognizer.predict(temp,result, 0)
         nbr_predicted = result.getLabel()
         conf=result.getDist()
         
         if nbr_predicted==1:
             if conf < 1:
                 cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                 male=male+1
                 for i in range(35):
                     _,frame=cap.read()
                     if _==False:
                         break
         if _==False:
             break
         
         elif nbr_predicted==0:
             if conf < 1:
                 cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                 female=female+1
                 for i in range(35):
                     _,frame=cap.read()
                     if _==False:
                         break
                     
         if _==False:
             break
    
    if _==True:
    	cv2.putText(frame,'M='+ str(male),(570,320),font,0.6,(255,255,255),2,cv2.LINE_AA)
    	cv2.putText(frame,'F='+ str(female),(570,350),font,0.6,(255,255,255),2,cv2.LINE_AA) 
    	cv2.imshow('img',frame) 
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print('Frames = ' + str(no_frames))
print('Males = ' + str(male))
print('Females = ' + str(female))
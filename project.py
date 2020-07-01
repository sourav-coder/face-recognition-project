''
# loading the libraries ---
import os
import face_recognition
import cv2
import numpy as np
import datetime


# loading the files of the directory ---

files=[]
for dir,dirname,filename in os.walk('image'):
    files=filename



known_faces=[]
known_name=[]

for name in files:
        image=face_recognition.load_image_file(os.path.join('image/',name))
        location=face_recognition.face_locations(image)
        top,right,bottom,left=location[0]
        #print(location,"dir")
        image=image[top:bottom,left:right]
        encoding=face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_name.append(name[:-4])



#segregation


cap=cv2.VideoCapture(0)

#  opening ss.txt for writing the exact time of entering
file1 = open("ss.txt", "w")
#  opening biden.txt for writing the exact time of entering

file2 = open('biden.txt', 'w')

process=True
face_locations=[]
face_encoding=[]
i=0
while 1:

    _,frame=cap.read()


    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]
    #face_names = []


    if process:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding)
            name = "Unknown"
            print(matches)

            face_distances = face_recognition.face_distance(known_faces, face_encoding)
            best_match_index = np.argmin(face_distances)

            print(known_name[best_match_index])

            if matches[best_match_index]:
                name = known_name[best_match_index]


            face_names.append(name)
            if name!='Unknown':
                print(name+'  '+str(datetime.datetime.now())[:19])
                #a.add(name+'  '+str(datetime.datetime.now())[:19]+'\n')
                if name == 'ss':

                    file1.write(str(datetime.datetime.now())[:19]+'\n')
                elif name == 'biden':
                    file2.write(str(datetime.datetime.now())[:19]+'\n')




    process = not process



    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (119, 155, 0), 2)

        cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (130, 0, 75),cv2.FILLED)
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 1)

        if name=='Unknown'  and i%5==0:
            j='Unknown/' + str(i)+'_faces'+'.jpg'

            cv2.imwrite(j,frame)

        i+=1

    cv2.imshow('video',frame)


    #cv2.imwrite('Unknown/'+'faces.jpg',frame)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break


cap.release()

#file1.writelines(a)

file1.close()
file2.close()
cv2.destroyAllWindows()

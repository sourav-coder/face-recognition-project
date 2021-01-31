# importing  the libraries ---
import os
import face_recognition
import cv2
import numpy as np
import datetime
from SSIM_PIL import compare_ssim
from pymongo import MongoClient
import imagehash
from PIL import  Image
import shortuuid
import pyrebase


client = MongoClient("mongodb+srv://rupam-admin:RUPAM9064869734@cluster0.gemmv.mongodb.net/thirdeyeSpyDB?retryWrites=true&w=majority")
db = client.get_database("thirdeyeSpyDB")
records = db.takendatas
recordsGiven = db.givendatas
unknown = db.unknowns




def uploadImage():
    print("from upload image.......................!!!!!")
    config = {
        "apiKey": "AIzaSyAgeOzZ8ldHh7rJC_6lTWgvXPU_kS55Fqc",
        "authDomain": "thirdeye-spy2.firebaseapp.com",
        "databaseURL": "https://thirdeye-spy2.firebaseio.com",
        "projectId": "thirdeye-spy2",
        "storageBucket": "thirdeye-spy2.appspot.com",
        "messagingSenderId": "129369110189",
        "appId": "1:129369110189:web:f486394302d8ecc4393824"
    }
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()

    # directory = "./unknownImages"
    directory = "./Unknown/test"

    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".PNG") or filename.endswith(
                ".jpeg"):
            my_id = shortuuid.uuid()
            path_on_cloud = my_id + "." + filename.split(".")[1]
            timeOfUnknownImage = filename.split(".")[0]
            path_local = filename
            storage.child("Unknown/test/" + path_on_cloud).put("Unknown/test/" + path_local)

            # get the url of the image
            auth = firebase.auth()
            email = "test@gmail.com"
            password = "123456"
            user = auth.sign_in_with_email_and_password(email, password)
            url = storage.child("Unknown/test/" + path_on_cloud).get_url(user['idToken'])
            newUnknown = {
                "imageURL": url,
                "time": timeOfUnknownImage
            }
            unknown.insert_one(newUnknown)
        else:
            pass
    print('Upload Completed  ...... ')


# loading the files of the directory ---

files = []
for dir, dirname, filename in os.walk('image'):
    files = filename

known_faces = []
known_name = []

for name in files:
    image = face_recognition.load_image_file(os.path.join('image/', name))
    location = face_recognition.face_locations(image)
    top, right, bottom, left = location[0]
    print(location, "dir")
    image = image[top:bottom, left:right]
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_name.append(name[:-4])

# segregation

# ---------------------- VIDEO  --------------
cap = cv2.VideoCapture('samples_video/withMask1.mp4')
# cap = cv2.VideoCapture(1)

# cap1 = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)

#  opening ss.txt for writing the exact time of entering
file1 = open("ss.txt", "w")
#  opening biden.txt for writing the exact time of entering

file2 = open('biden.txt', 'w')
# face classifier
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_fullbody.xml')
mouth = cv2.CascadeClassifier('haarcascades/mouth.xml')
process = True
# face_locations=[]
# face_encoding=[]
i = 0
j = 0
k = 0
hash1=''

while 1:

    ret, frame = cap.read()
    # ret1,frame1=cap1.read()
    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

    if ret:

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # face_names = []

        if process:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            print("Face location ", face_locations)

            if face_locations == []:
                faces = face_cascade.detectMultiScale(rgb_small_frame, 1.01, 3)
                windowWidth = rgb_small_frame.shape[1]
                windowHeight = rgb_small_frame.shape[0]

                for (x, y, w, h) in faces:
                    # x*=4
                    # y*=4
                    # w*=4
                    # h*=4

                    cv2.rectangle(rgb_small_frame, (x, y), (x + w, y + h), (245,245,245), 2)

                    j = 'Unknown/test/'+str(datetime.datetime.now().strftime("%Y-%m-%d-%I_%M_%S_%p")) +'.jpg'
                    print(w, h)

                    if k % 5 == 0 :# and (h >= windowHeight // 5) and (w >= windowHeight // 5):
                        print('test')
                        rgb_small_frame = cv2.cvtColor(rgb_small_frame, cv2.COLOR_BGR2RGB)
                        img = Image.fromarray(rgb_small_frame)

                        if len(str(hash1))==0:
                            print('Initial')
                            hash1=imagehash.average_hash(img)
                            # print('Write :-')
                            # cv2.imwrite(j, frame)
                        else:
                            hash2=imagehash.average_hash(img)
                            print("minus ",hash1-hash2)
                            # if the hash value is > cutoff then it must be some other image (experimented value)
                            if hash1-hash2 > 10:
                                print('Write 2:-')
                                print(j)
                                cv2.imwrite(j, frame)
                                hash1=hash2

                    k += 1
                # cv2.imshow('video', frame)

            #  separate for known and unknown people

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
                if name != 'Unknown':
                    print(name + '  ' + str(datetime.datetime.now())[:19])
                    # a.add(name+'  '+str(datetime.datetime.now())[:19]+'\n')
                    if name == 'ss' and j % 5 == 0:
                        file1.write(str(datetime.datetime.now())[11:19] + '\n')
                        j += 1

                    if name == 'biden':
                        file2.write(str(datetime.datetime.now())[11:19] + '\n')

        process = not process


        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (119, 155, 0), 3)

            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (130, 0, 75), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 1)

            mouth_reacts = mouth.detectMultiScale(frame[top:top + right, left:left + right], 1.1, 3)
            if name == 'Unknown' and i % 5 == 0:
                j = 'Unknown/' + str(i) + '_faces' + '.jpg'

                print("length of mouth array",mouth_reacts)
                if len(mouth_reacts)==0:
                    cv2.imwrite(j, frame)

            i += 1

        # small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        cv2.imshow('video',frame )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            uploadImage()
            break

cap.release()
# cap1.release()

# file1.writelines(a)

file1.close()
file2.close()
cv2.destroyAllWindows()

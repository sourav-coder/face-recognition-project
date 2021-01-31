# version - 1.0

# 09:31:00
# 09:32:00
# 09:45:00
# 10:10:00
# 10:15:00
# 10:35:00

# loading the libraries ---
import os
import face_recognition
import cv2
import numpy as np
import datetime
from pymongo import MongoClient

mongoUrl = open('./hide.txt','r')
client = MongoClient(mongoUrl.read())
db = client.get_database("thirdeyeSpyDB")
records = db.takendatas
recordsGiven = db.givendatas


def faceRecognition():
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

    cap = cv2.VideoCapture(0)
    cap1 = cv2.VideoCapture(1)

    #  opening ss.txt for writing the exact time of entering
    # file1 = open("dataTakenFiles/", "w")
    #  opening biden.txt for writing the exact time of entering

    # file2 = open('dataTakenFiles/biden.txt', 'w')
    file1 = open("dataTakenFiles/rupam.txt", "a")
    #  opening biden.txt for writing the exact time of entering

    file2 = open("dataTakenFiles/biden.txt", "a")
    file3 = open("dataTakenFiles/lin.txt", "a")

    process = True
    # face_locations=[]
    # face_encoding=[]
    i = 0
    j = 0
    k = 0
    l = 0
    a = 0
    b = 0
    c = 0
    while 1:

        ret, frame = cap.read()
        ret1, frame1 = cap1.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]  # converting to rgb from bgr
        # face_names = []

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
                if name != 'Unknown':
                    print(name + '  ' + str(datetime.datetime.now())[:19])
                   # a.add(name+'  '+str(datetime.datetime.now())[:19]+'\n')
                    if name == 'rupam' and j % 5 == 0:
                        file1.write(str(datetime.datetime.now())[:19] + '\n')
                        j += 1

                    if name == 'biden' and k % 5 == 0:
                        file2.write(str(datetime.datetime.now())[:19] + '\n')
                        k += 1
                    if name == "lin" and l % 5 == 0:
                        file3.write(str(datetime.datetime.now())[:19] + '\n')
                        l += 1

        # process = not process

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (119, 155, 0), 2)

            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (130, 0, 75), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 1)

            if name == 'Unknown' and i % 5 == 0:
                j = 'Unknown/' + str(i) + '_faces' + '.jpg'

                cv2.imwrite(j, frame)

            i += 1

        cv2.imshow('video', frame)

        # cv2.imwrite('Unknown/'+'faces.jpg',frame)

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        print('Camera 2 started ')
        small_frame = cv2.resize(frame1, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]
        # face_names = []
        if process:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Unknown"

                print('Camera 2', matches)

                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)

                print('Camera 2', known_name[best_match_index])

                if matches[best_match_index]:
                    name = known_name[best_match_index]

                face_names.append(name)
                if name != 'Unknown':

                    print(name + '  ' + str(datetime.datetime.now())[:19])
                    print(str(datetime.datetime.now()))
                    # a.add(name+'  '+str(datetime.datetime.now())[:19]+'\n')
                    if name == 'rupam' and a % 5 == 0:
                        file1.write(str(datetime.datetime.now())[:19] + '\n')
                        a += 1

                    if name == 'biden' and b % 5 == 0:
                        file2.write(str(datetime.datetime.now())[:19] + '\n')
                        b += 1
                    if name == "lin" and c % 5 == 0:
                        file3.write(str(datetime.datetime.now())[:19] + '\n')
                        c += 1

        process = not process

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame1, (left, top), (right, bottom), (119, 155, 0), 2)

            cv2.rectangle(frame1, (left, bottom - 30), (right, bottom), (130, 0, 75), cv2.FILLED)
            font = cv2.FONT_HERSHEY_TRIPLEX
            cv2.putText(frame1, name, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 1)

            if name == 'Unknown' and i % 5 == 0:
                j = 'Unknown/' + str(i) + '_faces' + '.jpg'

                cv2.imwrite(j, frame1)

            i += 1

        cv2.imshow('video2', frame1)

        # cv2.imwrite('Unknown/'+'faces.jpg',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            algo()
            break


    cap.release()
    cap1.release()

    # file1.writelines(a)

    file1.close()
    file2.close()
    file3.close()
    cv2.destroyAllWindows()


def algo():
    givenNamesArray = ["bidenSample", "linSample", "rupamSample"]
    takenNamesArray = ["biden", "lin", "rupam"]
    totalKnownPeople = len(givenNamesArray)

    def setEverything(givenFileArray, takenFileArray, name):
        count = 0
        totalTimeDiff = []
        for i in range(0, len(givenFileArray) - 1, 4):
            flag = 1
            for j in range(0, len(takenFileArray) - 1, 2):
                if takenFileArray[j] >= givenFileArray[i] and takenFileArray[j] <= givenFileArray[i + 1] and \
                        takenFileArray[j + 1] >= givenFileArray[i + 2] and takenFileArray[j + 1] <= givenFileArray[
                    i + 3]:
                    count = count + 1
                    flag = -1

            if flag != -1:
                periodStart = str(givenFileArray[i + 1])
                periodEnd = str(givenFileArray[i + 2])
                for k in range(0, len(takenFileArray), 2):
                    if takenFileArray[k] >= givenFileArray[i]:  # and takenFileArray[k] <= givenFileArray[i+1]:
                        start = k
                        break
                for l in range(len(takenFileArray) - 1, 0, -2):
                    if takenFileArray[l] <= givenFileArray[i + 3]:  # and takenFileArray[l] >= givenFileArray[i+2]:
                        end = l
                        break
                global timeDiff
                timeDiff = datetime.datetime.now() - datetime.datetime.now()
                try:
                    for m in range(start, end + 1, 2):
                        start_dt = datetime.datetime.strptime(takenFileArray[m], '%H:%M:%S')
                        end_dt = datetime.datetime.strptime(takenFileArray[m + 1], '%H:%M:%S')
                        diff = (end_dt - start_dt)
                        timeDiff = timeDiff + diff
                except UnboundLocalError:
                    print("I am here.................................", name)
                    pass
                dictionary = {"startingTime": periodStart, "endingTime": periodEnd, "timeCovered": str(timeDiff)}
                totalTimeDiff.append(dictionary)

        return (count, totalTimeDiff)

    now = datetime.datetime.now()
    todayName = now.strftime("%A")

    for i in range(0, totalKnownPeople):
        ##fileGiven = open("dataGivenFiles/" + givenNamesArray[i] + "/" + givenNamesArray[i] + todayName + ".txt", "r")
        fileTaken = open("dataTakenFiles/" + takenNamesArray[i] + ".txt", "r")

        ##fileGivenArray = fileGiven.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        ##fileGivenArray = [x.strip() for x in fileGivenArray]

        fileTakenArray = fileTaken.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
        fileTakenArray = [x.strip() for x in fileTakenArray]

        # ---------testing----------
        nameOfTheDay = todayName.lower()
        document = recordsGiven.find_one({"name": takenNamesArray[i]})
        fileGivenArray = document[nameOfTheDay]
        # -------x-------texting-------x-------

        count, diffArray = setEverything(fileGivenArray, fileTakenArray, givenNamesArray[i])

        if count == len(fileGivenArray) / 4:
            print(count)
            print("All correct")
        elif count != len(fileGivenArray):
            print(count)
            print(diffArray)
            print("partially correct")
        # -------------initializing the level of a candidate Start-------------#
        level = "0"
        if takenNamesArray[i] == "biden":
            level = "1"
        elif takenNamesArray[i] == "lin":
            level = "2"
        else:
            level = "3"
        # -------------initializing the level of a candidate End-------------#

        # inserting document into the database start
        if len(diffArray) != 0:
            newDoc = {
                "name": takenNamesArray[i],
                "level": level,
                "totallyCorrect": count,
                "notTotallyCorrect": diffArray
            }
            records.insert_one(newDoc)
        # inserting document into the database end..!!

        ##fileGiven.close()
        fileTaken.close()


faceRecognition()
# mongodb+srv://rupam-admin:<password>@cluster0.gemmv.mongodb.net/<dbname>?retryWrites=true&w=majority
# Replace <password> with the password for the rupam-admin user. Replace <dbname> with the name of the database that connections will use by default. Ensure any option params are URL encoded.

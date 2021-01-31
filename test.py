# testing

# from deepface import  DeepFace
# v=DeepFace.verify("image/biden.jpg","image/Joe-Biden.jpg",model_name="")
# print(v)



# import face_recognition
# known_image = face_recognition.load_image_file("image/biden_2.jpg")
# unknown_image = face_recognition.load_image_file("image/Joe-Biden.jpg")
# face_locations = face_recognition.face_locations(unknown_image)
# print(face_locations)
#
# biden_encoding = face_recognition.face_encodings(known_image)[0]
# unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
#
# results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
# print(results)


# from PIL import Image,ImageOps
# import imagehash
# img1=Image.open(r"image/biden.jpg")
# img2=Image.open(r"image/biden_2.jpg")
#
# hash0 = imagehash.average_hash(img1)
# hash1 = imagehash.average_hash(img2)
#
# #  check width of the images are equal or not
# if img1.width<img2.width:
#     img2=img2.resize((img1.width,img1.height))
# else:
#     img1=img1.resize((img2.width,img2.height))
#
# from SSIM_PIL import compare_ssim
#
#
# value = compare_ssim(img1, img2)
# print(value)
#
# cutoff = 5
#
# if hash0 - hash1 < cutoff:
#     print('images are similar')
# else:
#     print('images are not similar')



import imagehash
from PIL import  Image

img1=Image.open(r"Unknown/test/5 new_faces.jpg")
img2=Image.open(r"Unknown/test/20 new_faces.jpg")

hash0 = imagehash.average_hash(img1)
hash1 = imagehash.average_hash(img2)

 # check width of the images are equal or not
if img1.width<img2.width:
    img2=img2.resize((img1.width,img1.height))
else:
    img1=img1.resize((img2.width,img2.height))

from SSIM_PIL import compare_ssim

value = compare_ssim(img1, img2)
print(value)

cutoff = 5

if hash0 - hash1 < cutoff :
    print('images are similar')
else:
    print('images are not similar')









# cascade classifier
# import cv2
# import face_recognition
#
# face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_fullbody.xml')
# upper_body = cv2.CascadeClassifier('haarcascades/haarcascade_upperbody.xml')
#
#
# # cap = cv2.VideoCapture('samples_video/withMask.mp4')
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
#
#
#
#
# i=0
# while (cap.isOpened()):
#     ret,img=cap.read()
#
#     img=cv2.resize(img,(0,0),fx=0.7,fy=0.7)
#     # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#
#     landmarks=face_recognition.face_locations(img)
#     print(landmarks)
#     if landmarks==[]:
#
#         faces = face_cascade.detectMultiScale(img,1.01,3)
#         windowWidth = img.shape[1]
#         windowHeight = img.shape[0]
#
#         for x,y,w,h in faces:
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,100),2)
#             j = 'Unknown/test/' + str(i) + ' new_faces' + '.jpg'
#             print(w,h)
#
#             if i%5==0   and (h>=windowHeight//5) and (w>=windowHeight//5) :
#                 print('Write :-')
#                 cv2.imwrite(j,img[y:y+h, x:x+w])
#         i+=1
#
#         cv2.imshow('video',img)
#
#         if cv2.waitKey(1) & 0xFF==ord('q'):
#             break
#     else:
#         cv2.imwrite('Unknown/test/' + str(i)+' maybe_new_faces' + '.jpg',img)



# cv2.destroyAllWindows()

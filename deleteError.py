import os

annotation_path="VOCdevkit/VOC2007/Annotations/"
JPEGImages_path="VOCdevkit/VOC2007/JPEGImages/"

annotation_names=[i for i in os.listdir(annotation_path)]
JPEGImages_names=[i for i in os.listdir(JPEGImages_path)]

for a in annotation_names:
    jname=a[:6]+'.jpg'
    if not jname in JPEGImages_names:
        aname=annotation_path+a
        print(aname)
        os.remove(aname)
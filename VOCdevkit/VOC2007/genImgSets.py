import os
import random

PATH='Annotations/'

val_RATIO=1/90#val num over all images ratio
test_RATIO=1/90

f_test=open('ImageSets/Main/test.txt','w')
f_train=open('ImageSets/Main/train.txt','w')
f_val= open('ImageSets/Main/val.txt','w')
f_trainval=open('ImageSets/Main/trainval.txt','w')

counter=0
file_list = os.listdir(PATH)
random.shuffle(file_list)

for filename in file_list:
    if counter<=val_RATIO * len(file_list):
        f_val.write(filename[:-4]+'\n')

        f_trainval.write(filename[:-4]+'\n')
    elif counter < (val_RATIO+test_RATIO) * len(file_list):
        f_test.write(filename[:-4]+'\n')
    else:
        f_train.write(filename[:-4]+'\n')
        f_trainval.write(filename[:-4]+'\n')
    counter+=1

f_train.close()
f_test.close()
f_val.close()
f_trainval.close()

yolov3-self
=============
Instructions
----------
* Download `yolo_weight.h5` into `model_data\`
* Place the dataset image in `VOCdevkit\VOC2007\JPEGImages\`, dataset labels in `VOCdevkit\VOC2007\Annotations`
* run `VOCdevkit\VOC2007\genImgSets.py`
* run `voc_annotation.py`
* run `getClassNum.py`, get all category names and quantities of the dataset
* Modify the content in `model_data\voc_classes.txt` to the current dataset category
* Modify the `filters`(3*(5+len(classes))) and `classes` near the Yolo section of `yolov3.cfg`
* run `train.py`

### yolo_weight.h5
* 链接：https://pan.baidu.com/s/1MfVgKV6UGect9CQcqY_NIw 
* 提取码：lgua

Other functions
----------
* If you only have `yolov3.weights`, you can put it in `\.` and run `convert_keras-yolo3.py.py`
* If your `JPEGImages` and `Annotations` numbers are different, you can run `deleteError.py` delete extra parts
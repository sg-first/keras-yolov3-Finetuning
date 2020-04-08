#!/usr/bin/env python
# -*- coding: utf8 -*-
#import _init_path
import sys
import os
from lxml import etree
import codecs

XML_EXT = '.xml'
'''
程序说明：
    本程序是在ubuntu16.04 64位 python2.7.12环境下运行的

    该程序是通过读入txt文件，生成xml文件（pascal voc标注类型） txt文件每行的格式为：label xmin ymin xmax ymax


'''

class PascalVocWriter:

    def __init__(self, foldername, txt_source_path,xml_save_path , imageSize,databaseSrc='MyData', localImgPath=None):
        self.foldername = foldername
        self.txt_source_path = txt_source_path
        self.xml_save_path= xml_save_path
        self.databaseSrc = databaseSrc
        self.imgSize = imageSize  #[1080,1920,3]
        self.localImgPath = localImgPath
        self.verified = False

    def list_dir(self,path):
        return [f for f in os.listdir(path)]

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = etree.tostring(elem, encoding='UTF-8')
        #rough_string = str(rough_string, encoding="UTF-8")
        rough_string = str(rough_string)
        root = etree.XML(rough_string)
        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    def genXML(self,image_name):
        """
            Return XML root
        """
        # Check conditions
        top = etree.Element('annotation')
        #top.set('verified', 'yes' if self.verified else 'no')

        folder = etree.SubElement(top, 'folder')
        folder.text = self.foldername

        filename = etree.SubElement(top, 'filename')
        filename.text = image_name

        localImgPath = etree.SubElement(top, 'path')
        localImgPath.text = self.localImgPath

        source = etree.SubElement(top, 'source')
        database = etree.SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = etree.SubElement(top, 'size')
        width = etree.SubElement(size_part, 'width')
        height = etree.SubElement(size_part, 'height')
        depth = etree.SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = etree.SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addBndBox(self, txt_filename):
        lines=open(txt_filename)
        boxlist=[]
        for line in lines:
            line=line.split(' ')
            bndbox = {'xmin': line[1], 'ymin': line[2], 'xmax': line[3], 'ymax': line[4]}
            bndbox['name'] = line[0]
            boxlist.append(bndbox)
        return boxlist

    def appendObjects(self, top,txt_filename):
        boxlist=self.addBndBox(os.path.join(self.txt_source_path,txt_filename))
        for each_object in boxlist:
            object_item = etree.SubElement(top, 'object')
            name = etree.SubElement(object_item, 'name')
            try:
                name.text = unicode(each_object['name'])
            except NameError:
                # Py3: NameError: name 'unicode' is not defined
                name.text = each_object['name']
            pose = etree.SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            truncated = etree.SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = etree.SubElement(object_item, 'difficult')
            difficult.text = "0"
            bndbox = etree.SubElement(object_item, 'bndbox')
            xmin = etree.SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = etree.SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = etree.SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = etree.SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])

    def save(self):
        txt_filenames=self.list_dir(self.txt_source_path)
        for txt_filename in txt_filenames:
            image_name=os.path.basename(txt_filename).split('.')[0]+'.jpg'
            xml_name=os.path.basename(txt_filename).split('.')[0]+'.xml'
            targetFile=os.path.join(self.xml_save_path,xml_name)
            root = self.genXML(image_name)
            self.appendObjects(root,txt_filename)


            out_file = codecs.open(targetFile, 'w', encoding='utf-8')

            prettifyResult = self.prettify(root)
            out_file.write(prettifyResult.decode('utf8'))
            out_file.close()


class PascalVocReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def addShape(self, label, bndbox):
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append((label, points, None, None))

    def parseXML(self):
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        content = None
        with open(self.filepath, 'r') as xmlFile:
            content = xmlFile.read()

        if content is None:
            return False

        xmltree = etree.XML(content)
        filename = xmltree.find('filename').text
        try:
            verified = xmltree.attrib['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            label = object_iter.find('name').text
            self.addShape(label, bndbox)
        return True


tempParseReader = PascalVocReader('test.xml')
print(tempParseReader.getShapes())

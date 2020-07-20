#!/usr/bin/python
#
# Нумерация страниц в Marmot - с 1, как картинок страниц, так и в файле рамочек
# Нумерация страниц в ICDAR - с 1 в нумерации картинок страниц, и с 0 - в нумерации страниц в файле рамочек
#
# encoding=UTF-8
import os
import sys
import argparse
from lxml import etree
import struct
import cv2
import csv

def dir_path(path):
	if os.path.isdir(path):
		return path
	else:
		raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def gtWrite(docName,mathMap,dest_math_dir='./'):
	with open(os.path.join(dest_math_dir,docName+'.csv'),"w") as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',')
		for pNum in sorted(mathMap.keys()):
			for ramp in mathMap[pNum]:
				ramp.insert(0,pNum)
				csv_writer.writerow(ramp)
        
parser = argparse.ArgumentParser(description='Convert Marmot Math Dataset ground truth and image files to ICDAR tools compatible csv and image files')
parser.add_argument("--xml_dir", type=dir_path, required=True, help="Directory of Marmot ground truth xml files")
parser.add_argument("--img_dir", type=dir_path, required=True, help="Directory of Marmot doc page images")
parser.add_argument("--dest_img_dir", type=dir_path, required=True, help="Destination directory of ICDAR directories of page images")
parser.add_argument("--dest_math_dir", type=dir_path, required=True, help="Destination directory of ICDAR csv files")
args = parser.parse_args()
#print(args)
docName = '' 	# имя документа в смысле ICDAR
mathMap = dict() 	# ключ - номер страницы с 0, значение - координаты прямоугольника x,y: левый верхний, правый нижний
for docPageGTname in sorted(os.listdir(args.xml_dir)):
	if os.path.isdir(os.path.join(args.xml_dir,docPageGTname)): continue
	try:
		with open(os.path.join(args.xml_dir,docPageGTname)) as gtxml:
			gtFile = etree.parse(gtxml)
	except:
		print(docPageGTname,' must be a valid xml file')
		continue
	docPath = os.path.split(docPageGTname)
	newDocName, ext = os.path.splitext(docPath[-1])
	newDocName, pageNum = newDocName.split('_')
	pageNum = int(pageNum)
	#print("FIle ",docName,newDocName,pageNum)
	if newDocName != docName: 	# новый документ
		# запишем рамочки в csv
		if mathMap:
			print('Write ',docName)
			gtWrite(docName,mathMap,args.dest_math_dir)
		mathMap = dict() 	# ключ - номер страницы с 0, значение - координаты прямоугольника x,y: левый верхний, правый нижний
		docName = newDocName
		print('New doc: ',docName)

	root = gtFile.getroot()
	pageNum1 = int(root.get('PageNum'))
	if pageNum1 != pageNum:
		print('File ',docPath[-1],' has PageNum=',pageNum1,' inside, but must be the ',pageNum)
		continue
	print('Processed ',docName,', page ',pageNum)
	# Разбираем исходный файл с рамочками
	pageBox = root.get('BBox').split()
	pageBox = list(map(lambda el: struct.unpack('!d', bytes.fromhex(el))[0],pageBox)) 	# размер страницы в point (1/72 inch) https://stackoverflow.com/questions/52824584/do-anyone-know-how-to-extract-image-coordinate-from-marmot-dataset
	pageHeight = pageBox[1] 	# в пунктах, считая, что x0 == y0 == 0
	pageWidth = pageBox[2]
	# Картинка
	imgFileName = os.path.join(args.img_dir,docName+'_'+str(pageNum)+'.tif')
	#print(imgFileName)
	img = cv2.imread(imgFileName)
	if img is None:
		print('ERROR: file '+imgFileName+' must be')
		continue
	ppp = ((img.shape[0]/pageHeight) + (img.shape[1]/pageWidth))/2 	# pixels per point
	#print(ppp)
	mathMap[pageNum-1] = list() 	#  у них принято картинки нумеровать с 1, а страницы - с 0.
	for box in root:  
		#print(box.tag)
		x, y, x1, y1 = list(map(lambda el: struct.unpack('!d', bytes.fromhex(el))[0],box.get('BBox').split())) 	# координаты рамочки в пунктах, от левого нижнего угла
		x = round(x*ppp) 	# в пикселях от левого верхнего угла
		y = img.shape[0] - round(y*ppp)
		x1 = round(x1*ppp)
		y1 = img.shape[0] - round(y1*ppp)
		mathMap[pageNum-1].append([x, y, x1, y1])
	#print(mathMap[pageNum-1])
	# копируем файл
	if not os.path.exists(os.path.join(args.dest_img_dir,docName)):
		os.makedirs(os.path.join(args.dest_img_dir,docName))
	os.system('cp '+imgFileName+' '+os.path.join(args.dest_img_dir,docName,str(pageNum)+'.tif'))

# запишем последние рамочки в csv
if mathMap:
	print('Write ',docName)
	gtWrite(docName,mathMap,args.dest_math_dir)
		


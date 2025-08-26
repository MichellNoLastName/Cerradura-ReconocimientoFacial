import cv2
import os
import numpy as np

dataPath = 'C:/Users/equipo/Documents/Politecnico/Sistemas de Vision Artificial/Proyecto/ArchivosProyecto/Data'
peopleList = os.listdir(dataPath)
print("Lista de personas",peopleList)
label = 2
labels = []
facesData = []

personPath = dataPath + '/' + peopleList[2]
#print(personPath)
for filename in os.listdir(personPath):
	#print(peopleList[1] + '/' + filename)
	labels.append(label)
	facesData.append(cv2.imread(personPath + '/' + filename,0))
	#image = cv2.imread(personPath + '/' + filename,0)
	#cv2.imshow('image',image)
	#v2.waitKey(10)
face_recognizer = cv2.face.EigenFaceRecognizer_create()
print("Entrenando....")
face_recognizer.train(facesData,np.array(labels))

face_recognizer.write("Modelos/modeloYael.xml")
print("Modelo almacenado")
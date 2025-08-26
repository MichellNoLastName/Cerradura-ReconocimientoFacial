#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5.QtCore import QObject, pyqtSignal
from PROYECTO import *
import sys
import cv2
import xlrd
import os
import time
#import serial


def credenciales():
	nombres = []
	claves = []
	umbrales = []
	modelos = []
	nPila = []
	with xlrd.open_workbook('Credenciales.xlsx') as libro:
		for hoja in libro.sheets():
			for i in range(1,hoja.nrows):
				fila = hoja.row(i)
				nombres.append(fila[0].value)
				claves.append(fila[1].value)
				umbrales.append(fila[2].value)
				modelos.append(fila[3].value)
				nPila.append(fila[4].value)

	return nombres,claves,umbrales,modelos,nPila

def SerialPort(auth):
	#puerto = serial.Serial('COM10',115200)

	puerto.write(("3\n").encode())
	time.sleep(5)
	puerto.close()
	print('Dato Enviado')


class reconocimientoFacial(QObject):
	senal = pyqtSignal(int)

	def conectarSenal(self):
		self.senal.connect(self.manejarSenal)
	def emitirSenal(self,index):
		self.senal.emit(index)
	def manejarSenal(self,index):

		#dataPath = 'C:/Users/equipo/Documents/Politecnico/Sistemas de Vision Artificial/Proyecto/ArchivosProyecto/Data'
		#imagePaths = os.listdir(dataPath)
		usuarios,_,umbrales,modelos,nPila = credenciales()
		validacion = 0

		face_recognizer = cv2.face.EigenFaceRecognizer_create()
		archivoModelo = 'Modelos' + '/' + modelos[index] + '.xml'
		archivoModelo = str(archivoModelo)
		face_recognizer.read(archivoModelo)

		cap = cv2.VideoCapture(0)
		face_cascade = cv2.CascadeClassifier('opencv-master/data/haarcascades/haarcascade_frontalface_default.xml')
		time1 = time.time()
		time2 = time.time() - time1

		while (time2) <= 15.0:
			ret,frame = cap.read()
			if ret == False: break
			gray= cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
			auxFrame = gray.copy()
			faces = face_cascade.detectMultiScale(gray,1.3,5)

			for(x,y,w,h) in faces:
				rostro = auxFrame[y:y+h,x:x+w]
				rostro = cv2.resize(rostro,(150,150),interpolation = cv2.INTER_CUBIC)
				result = face_recognizer.predict(rostro)

		#cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
				if result[1] < umbrales[index]:
					cv2.putText(frame,'{}'.format(nPila[index]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
					cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
					validacion = validacion + 1
				else:
					cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
					cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

			
			cv2.imshow('Autenticación',frame)
			k = cv2.waitKey(1)
			if k == 27 or validacion >= 10:
				print('Acceso concedido')
				#SerialPort("Y\n")
				break
			time2 = time.time() - time1

		cap.release()
		cv2.destroyAllWindows()


class myWindow(QtWidgets.QMainWindow):

	def __init__(self):
		super(myWindow,self).__init__()
		self.ui = Ui_Form()
		self.ui.setupUi(self)
		pixmap = QPixmap('seguridad2.jpg')
		self.ui.labelImage.setPixmap(pixmap)
		self.ui.buttonValidar.clicked.connect(self.validacion)

	def validacion(self):
		clave = self.ui.textBoxClave.text()
		usuarios,claves,_,_,_ = credenciales()
		if(len(clave) == 6):
			try:
				clave = int(clave)
				if clave in claves:
					index = claves.index(clave)
					usuario = usuarios[index]
					self.ui.labelTrue.setText('Usuario: {}'.format(usuario))
					self.ui.labelFalse.clear()
					self.ui.textBoxClave.clear()
					cam = reconocimientoFacial()
					cam.conectarSenal()
					cam.emitirSenal(index)
					self.ui.labelTrue.clear()
					self.ui.labelFalse.clear()
				else:
					self.ui.labelTrue.clear()
					self.ui.labelFalse.setText("Usuario Inexistente")
					self.ui.textBoxClave.clear()
			except ValueError:
				self.ui.labelTrue.clear()
				self.ui.labelFalse.setText("Clave Inválida\nInténtelo de nuevo")
				self.ui.textBoxClave.clear()
		else:
			self.ui.labelTrue.clear()
			self.ui.labelFalse.setText("Clave Inválida\nInténtelo de nuevo")
			self.ui.textBoxClave.clear()



def main():
	#SerialPort(5)
	app = QtWidgets.QApplication([[]])
	application = myWindow()
	application.show()
	sys.exit(app.exec())

if __name__ == '__main__':
	main()
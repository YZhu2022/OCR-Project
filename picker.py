# -*-coding:utf-8-*-
import tkinter
import struct
import subprocess
import tkinter.filedialog
from PIL import ImageGrab
from time import sleep
import os
import tkinter.messagebox
import pytesseract
from PIL import Image
import pyperclip
import webbrowser

location = (os.path.abspath( 'picker.py' ))
locationofcore = location.replace( r"picker.py", r"Tesseract Core\Tesseract.exe" )
locationofpicture = location.replace( "picker.py", r"\Buffer\screenshot.png" )
locationofpicture1 = location.replace( "picker.py", r"\Buffer\rotation.png" )
pytesseract.pytesseract.tesseract_cmd = locationofcore
root = tkinter.Tk()
root.geometry( '300x300+400+300' )
root.resizable( False, False )
root.title("OCR based on Tesseract")


class MyCapture:
    def __init__(self, png):
        self.X = tkinter.IntVar( value=0 )
        self.Y = tkinter.IntVar( value=0 )
        screenWidth = root.winfo_screenwidth()
        screenHeight = root.winfo_screenheight()
        self.top = tkinter.Toplevel( root, width=screenWidth, height=screenHeight )
        self.top.overrideredirect( True )
        self.canvas = tkinter.Canvas( self.top, bg='white', width=screenWidth, height=screenHeight )
        self.image = tkinter.PhotoImage( file=png )
        self.canvas.create_image( screenWidth // 2, screenHeight // 2, image=self.image )

        def onLeftButtonDown(event):
            self.X.set( event.x )
            self.Y.set( event.y )
            self.sel = True

        self.canvas.bind( '<Button-1>', onLeftButtonDown )

        def onLeftButtonMove(event):
            if not self.sel:
                return
            global lastDraw
            try:
                self.canvas.delete( lastDraw )
            except Exception as e:
                pass
            lastDraw = self.canvas.create_rectangle( self.X.get(), self.Y.get(), event.x, event.y, outline='black' )

        self.canvas.bind( '<B1-Motion>', onLeftButtonMove )

        def onLeftButtonUp(event):
            self.sel = False
            self.sel = False
            try:
                self.canvas.delete( lastDraw )
            except Exception as e:
                pass
            sleep( 0.2 )
            left, right = sorted( [self.X.get(), event.x] )
            top, bottom = sorted( [self.Y.get(), event.y] )
            pic = ImageGrab.grab( (left + 1, top + 1, right, bottom) )
            pic.save( locationofpicture )
            self.top.destroy()
        self.canvas.bind( '<ButtonRelease-1>', onLeftButtonUp )
        self.canvas.pack( fill=tkinter.BOTH, expand=tkinter.YES )

def buttonCaptureClick():
    root.state( 'icon' )
    sleep( 0.3 )
    filename = location.replace( "picker.py", "Buffer\Temp.png" )
    im = ImageGrab.grab()
    im.save( filename )
    im.close()
    w = MyCapture( filename )
    buttonCapture.wait_window( w.top )
    root.state( 'normal' )
    os.remove( filename )
    ImageTODO = Image.open( location.replace("picker.py","Buffer\screenshot.png") )
    code = pytesseract.image_to_string( ImageTODO ,lang="eng")
    pyperclip.copy(code)

def versioninfo():
    webbrowser.open( 'http://www.python.org' )
    webbrowser.open( 'https://pypi.org/project/pytesseract/' )
    webbrowser.open("https://github.com/tesseract-ocr/tesseract/blob/master/LICENSE")

def recognizeafile():
    filename2 = tkinter.filedialog.askopenfilename()
    filetype = filename2[-3:]
    if filetype not in ["jpg","peg","png","bmp","PNG","JPG","PEG","BMP"]:
        tkinter.messagebox.showinfo( "Error!", "Invalid file type!" )
    ImageTODO2 = Image.open( filename2 )
    code2 = pytesseract.image_to_string( ImageTODO2, lang="eng" )
    f = open(location.replace( "picker.py", r"\Buffer\temp.txt" ), 'w' )
    f.write(code2)
    pyperclip.copy(code2)

# part of the code has the reference : http://www.10tiao.com/html/383/201609/2247483779/1.html
# some other websites may include the code like this, like https://cloud.tencent.com/developer/article/1097904
#Cited from https://www.cnblogs.com/polly333/p/7280764.html
# ====================================
#Experimental Functions
import cv2
import math
import numpy
from scipy import misc, ndimage

def Hoff():
    filename3 = tkinter.filedialog.askopenfilename()
    img = cv2.imread( filename3)
    gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    edges = cv2.Canny( gray, 50, 150, apertureSize=3 )
    lines = cv2.HoughLines( edges, 1, numpy.pi / 180, 0 )
    for rho, theta in lines[0]:
        a = numpy.cos( theta )
        b = numpy.sin( theta )
        x0 = a * rho
        y0 = b * rho
        x1 = int( x0 + 1000 * (-b) )
        y1 = int( y0 + 1000 * (a) )
        x2 = int( x0 - 1000 * (-b) )
        y2 = int( y0 - 1000 * (a) )
    if x1 == x2 or y1 == y2:
        pass
    t = float( y2 - y1 ) / (x2 - x1)
    rotate_angle = math.degrees( math.atan( t ) )
    if rotate_angle > 45:
        rotate_angle = -90 + rotate_angle
    elif rotate_angle < -45:
        rotate_angle = 90 + rotate_angle
    rotate_img = ndimage.rotate( img, rotate_angle )
    misc.imsave(locationofpicture1, rotate_img )
    code3 = pytesseract.image_to_string( locationofpicture1, lang="eng" )
    f = open(location.replace( "picker.py", r"\Buffer\temp.txt" ), 'w' )
    f.write(code3)
    pyperclip.copy(code3)

#part of the code has the reference https://blog.csdn.net/feilong_csdn/article/details/81586322

buttonCapture = tkinter.Button( root, text='screenshot to clipboard', command=buttonCaptureClick )
buttonCapture.place( x=10, y=10, width=275, height=20 )
recognizeafile = tkinter.Button( root, text='recognize from a file to clipboard', command=recognizeafile )
recognizeafile.place( x=10, y=30, width=275, height=20 )
versioninfo = tkinter.Button( root, text='version and copyright info', command=versioninfo)
versioninfo.place( x=10, y=50, width=275, height=20 )
Hoffman = tkinter.Button( root, text="(experimental) Hough transform ", command=Hoff)
Hoffman.place( x=10, y=70, width=275, height=20 )

root.mainloop()


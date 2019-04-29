# -*-coding:utf-8-*-
import tkinter
import subprocess
import tkinter.filedialog
from PIL import ImageGrab
from time import sleep
import os
import tkinter.messagebox
import pytesseract
from PIL import Image
import pyperclip

location = (os.path.abspath( 'picker01.py' ))
locationofcore = location.replace( r"picker01.py", r"Tesseract Core\Tesseract.exe" )
locationofpicture = location.replace( "picker01.py", r"\Buffer\screenshot.png" )
pytesseract.pytesseract.tesseract_cmd = locationofcore
root = tkinter.Tk()
root.geometry( '100x40+400+300' )
root.resizable( False, False )

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
            sleep( 0.1 )
            left, right = sorted( [self.X.get(), event.x] )
            top, bottom = sorted( [self.Y.get(), event.y] )
            pic = ImageGrab.grab( (left + 1, top + 1, right, bottom) )
            pic.save( locationofpicture )
            self.top.destroy()


        self.canvas.bind( '<ButtonRelease-1>', onLeftButtonUp )
        self.canvas.pack( fill=tkinter.BOTH, expand=tkinter.YES )

def buttonCaptureClick():
    root.state( 'icon' )
    sleep( 0.2 )
    filename = location.replace( "picker01.py", "Buffer\Temp.png" )
    im = ImageGrab.grab()
    im.save( filename )
    im.close()
    w = MyCapture( filename )
    buttonCapture.wait_window( w.top )
    root.state( 'normal' )
    os.remove( filename )
    ImageTODO = Image.open( location.replace("picker01.py","Buffer\screenshot.png") )
    code = pytesseract.image_to_string( ImageTODO ,lang="eng")
    pyperclip.copy(code)


buttonCapture = tkinter.Button( root, text='screenshot', command=buttonCaptureClick )
buttonCapture.place( x=10, y=10, width=80, height=20 )
root.mainloop()
# part of the code has the reference : http://www.10tiao.com/html/383/201609/2247483779/1.html

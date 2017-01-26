from tkinter import *
import PIL
from PIL import ImageDraw
import os
import shape_classification
import cv2

white = (255, 255, 255)
black = (0, 0, 0)
n = 0
shapes_learning_pending = False

class PaintBox(Frame):    
    
    image1 = PIL.Image.new("RGB", (800, 800), white)   

    def __init__(self):
        Frame.__init__(self)
        
        self.status = ""    
        self.pack(expand = YES, fill = BOTH)
        self.master.title("Shape classifier")
        self.master.geometry("800x800")
        self.draw = ImageDraw.Draw(self.image1)
        
        self.myCanvas = Canvas(self)
        self.myCanvas.pack(expand=YES,fill=BOTH)
        
        self.myCanvas.create_oval(-300, -300, 1500, 1500, fill='SlateGray1')
           
        self.text_entry = Entry(self.myCanvas)
        self.text_entry.pack(side=TOP)
        
        self.old_x = None
        self.old_y = None
        
        button2 = Button(self.myCanvas, text='Learn shape name from single drawn shape')
        button2.bind('<Button-1>', self.save_shapes_for_learning)
        button2.pack(side=TOP) 
        
        button3 = Button(self.myCanvas, text='Predict')
        button3.bind('<Button-1>', self.predict_wrapper)
        button3.pack(side=TOP) 
            
        button4 = Button(self.myCanvas, text='Clear')
        button4.bind('<Button-1>', self.clear_canvas)
        button4.pack()
        
        button5 = Button(self.myCanvas, text='Reset')
        button5.bind('<ButtonRelease-1>', self.reset_classifier)
        button5.pack(side=BOTTOM) 
        
        #event handler for drawing
        self.myCanvas.bind( "<B1-Motion>", self.paint)
        self.myCanvas.bind('<ButtonRelease-1>', self.reset)
         
        #init the classifier module
        shape_classification.import_source_images()    
        shape_classification.import_test_images()
        shape_classification.init_classifier()
        
    
    def on_window_closing():
        for f in os.listdir(shape_classification.source_images_folder_path):
            if 'drawn' in f:
                os.remove(shape_classification.source_images_folder_path + '\\' +f)
        for f in os.listdir(shape_classification.drawn_images_folder_path):
            if 'drawn' in f:
                os.remove(shape_classification.drawn_images_folder_path + "\\" +f)
                
    def reset_classifier(self, event):
        print('gui reset')
        
        PaintBox.on_window_closing()
        shape_classification.import_source_images()
        shape_classification.import_test_images()
        shape_classification.init_classifier()
        PaintBox.clear_canvas(self, event)
                
    def learn_drawn_shapes_wrapper(self, event):
        shape_classification.learn_drawn_shapes()
        self.clear_canvas()
       
    def save_shapes_for_learning(self, event):
        global n
        global shapes_learning_pending
        
        shapes_learning_pending = True
        filename = self.text_entry.get()
        if filename == '':
            return
        filename = (filename + '--drawn--' + str(n))
                
        self.save_canvas_as_image(shape_classification.drawn_images_folder_path, filename + '.jpg')
        self.save_canvas_as_image(shape_classification.source_images_folder_path, filename +'.jpg')
       
        #draw background
        self.draw.ellipse((-300, -300, 1200, 1200), fill=white)
        self.myCanvas.create_oval(-300, -300, 1200, 1200, fill='SlateGray1')
        #resolving same filename error by appending a serial number
        n += 1
       
    def clear_canvas(self, event):
        self.draw.ellipse((-300, -300, 1200, 1200), fill=white)
        self.myCanvas.create_oval(-300, -300, 1200, 1200, fill='SlateGray1')
        #shape_classification.import_test_images()
       
    def predict_wrapper(self, event, folder_path=r'test image', filename=r'canvas.jpg'):
        global shapes_learning_pending
        
        if shapes_learning_pending:
            shape_classification.import_source_images()
            shape_classification.init_classifier()
            shapes_learning_pending = False
        
        image_path = os.path.realpath(folder_path + '\\' + filename)
        PaintBox.image1.save(image_path)
        
        contours = shape_classification.import_test_images()
        
        shape_names = shape_classification.predict()
        #drawing a rectangle around the detected shapes
        for i, c in enumerate(contours):
            x, y, w, h = cv2.boundingRect(c)
            self.myCanvas.create_rectangle(x-1, y-1, x+w+1, y+h+1, width=1, outline = 'red')
            self.myCanvas.create_text(x+w//2, y+h+10, font=('Purisa', 10),text=shape_names[i])
        
        image_path = os.path.realpath(folder_path + '\\' + filename)
        #saves canvas as jpg
        PaintBox.image1.save(image_path)
        
        
    def import_test_image_wrapper(self, event):
        shape_classification.import_test_images()
        
    def reset(self, event):
        self.old_x, self.old_y = None, None
       
    def paint(self, event):
       
       ofs = 5
       x1, y1 = (event.x - ofs ), (event.y - ofs )
       x2, y2 = (event.x + ofs ), (event.y + ofs )
       #self.myCanvas.create_oval( x1, y1, x2, y2, fill='black')
       self.draw.ellipse((x1, y1, x2, y2), fill='black')
       
       if self.old_x and self.old_y:
            self.myCanvas.create_line(self.old_x, self.old_y, event.x, event.y, width=8, capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=(0,0,0,255), width=8)
            self.draw.line((self.old_x, self.old_y, event.x, event.y), fill=(0,0,0,255), width=5)
            
       self.old_x = event.x
       self.old_y = event.y
        
    def save_canvas_as_image(self, folder_path, filename):
    
       image_path = os.path.realpath(folder_path + '\\' + filename)
       PaintBox.image1.save(image_path)
       
       
def main():
    PaintBox().mainloop()
    PaintBox.on_window_closing()

if __name__ == "__main__":
    main()

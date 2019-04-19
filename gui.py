#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 12:17:44 2019

@author: yerlan
"""

from tkinter import *
from tkinter.colorchooser import askcolor
import pyscreenshot as ImageGrab
from PIL import Image
import cv2
import numpy as np
from random import randint
from keras.preprocessing import image
from keras.models import load_model

class Paint(object):

    DEFAULT_PEN_SIZE = 30.0
    DEFAULT_COLOR = 'white'

    def __init__(self):
        
        self.loaded_model = load_model('model.h5')
    
        self.root = Tk()
        self.class_name = StringVar()

        self.get_image_button = Button(self.root,text = 'save', command = self.save_image)
        self.get_image_button.grid(row=0,column = 0)

        self.eraser_button = Button(self.root, text='clean', command=self.clean_canvas)
        self.eraser_button.grid(row=0, column=1)
        
        self.predict_button = Button(self.root, text='predict', command=self.test)
        self.predict_button.grid(row=2, column=0)
        
        self.text_output = Label(text = 'Output:')
        self.text_output.grid(row = 2 , column = 1)

        self.output_label = Label(text = '')
        self.output_label.grid(row = 2, column = 2)
        self.output_label.config(font=("Courier",25))
        self.message_entry = Entry(textvariable=self.class_name)
        self.message_entry.grid(row=0,column=3)
        
        
        self.c = Canvas(self.root, bg='black', width=200, height=200)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
      
        self.old_x = None
        self.old_y = None

        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    
    def use_eraser(self):
        
        self.activate_button(self.eraser_button, eraser_mode=True)
    
    
    def clean_canvas(self):
        self.c.delete("all")

    
    def activate_button(self, some_button, eraser_mode=False):
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    
    def paint(self, event):
        self.line_width = 15.0
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y


    def reset(self, event):
        self.old_x, self.old_y = None, None
        

    def save_image(self):       

        self.eraser_on = False
        canvas = self._canvas()  # Get Window Coordinates of Canvas
        rand = str(randint(1,10000))
        im = ImageGrab.grab(bbox = canvas).save('train_set/'+self.class_name.get()+'/screen'+rand+'.png')
        print('saved')
    
    def test(self):
        
        self.eraser_on = False
        canvas = self._canvas()  # Get Window Coordinates of Canvas
        im = ImageGrab.grab(bbox = canvas)
        im.save('screen.png')
        test_image = image.load_img('screen.png',target_size = (28,28))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        test_image = self._rgb2gray(test_image)
        test_image = test_image.reshape(1,28,28,1)
        y = self._get_class_of_img(test_image)
        self.output_label['text'] = y
        

    def _get_class_of_img(self,img):
        
        output_values = self.loaded_model.predict(img)
        y = self._get_index_of_y(output_values)
        output_letter = self._get_kazakh_letter(y)
        return output_letter

    def _get_kazakh_letter(self,y):
        kazakh_alph = 'ә,і,ң,ғ,ү,ұ,қ,ө,һ'.split(',')
        return kazakh_alph[y]

    
    def _get_index_of_y(self,y):
    
        for i in range(y.shape[1]):
            if int(y[0][i]) == 1:
                return i
                
    def _rgb2gray(self,img):
        return np.dot(img[...,:], [0.2989, 0.5870, 0.1140])

    
    def _canvas(self):
        x=self.c.winfo_rootx()
        y=self.c.winfo_rooty()
        x1=x+self.c.winfo_width()
        y1=y+self.c.winfo_height()
        box=(x+2,y+2,x1-2,y1-2)
        return box



if __name__ == '__main__':
    Paint()








 # def save_image_data(self,im):
    #     colors = []
    #     rows,cols,k = im.shape
    #     for y in range(0,cols,24):
    #         for x in range(0,rows,23):
    #             color=im[x,y]
    #             colors.append(color)
    #     return colors  
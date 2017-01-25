import PIL
import os
from sklearn import svm
import numpy as np
import cv2
from matplotlib import pyplot as plt


source_images_folder_path = r'source images'
test_images_folder_path = r'test image'
drawn_images_folder_path = r'drawn images'

source_images = [] #learned images represented as np arrays
test_images = []
drawn_images = []

ARRAY_WIDTH, ARRAY_HEIGHT = 100, 100

source_shape_types = []
test_shape_types = []
drawn_shape_types = []

shape_dictionary = {0: 'circle', 1:'star', 2:'square', 3:'triangle'}
clf = svm.SVC(kernel='linear')

number_of_types = 4

def add_type_to_list(shape_array, filename):
    
    global number_of_types
    
    if 'circle' in filename:
        shape_array.append(0)
    elif 'star' in filename:
        shape_array.append(1)
    elif 'square' in filename:
        shape_array.append(2)
    elif 'triangle' in filename:
        shape_array.append(3)
    elif 'canvas' in filename:
        pass
    else:
        names = ''
        exists = False
        for i, v in enumerate(shape_dictionary.values()):
            if v in filename:
                exists = True
                shape_array.append(i)
                break
            
        if not(exists):
            print(filename)
            shape_array.append(number_of_types)
            new_shape_name = str.split(filename, '--drawn--')
            shape_dictionary[number_of_types] = new_shape_name[0]
            number_of_types += 1
        else:
            pass  

def create_image_array(folder_path, filename, shape_array):
    """Takes source folder path and image file name as input, isolates a shape, crops it,
    converts to greyscale, resizes to 200x200 and returns a numpy array based on the color
    information
    """
    image_path = os.path.realpath(folder_path + '\\' + filename)
    
    cvimage = cv2.imread(image_path)
    
    edged = cv2.Canny(cvimage, 10, 250)
    (cnts, a, b) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    crop_coordinates = cv2.boundingRect(cnts)
    
    image = PIL.Image.open(image_path)
    image = image.convert('L')
    nparray = np.asarray(image.getdata()).reshape(image.size[1], image.size[0])
    
    x = crop_coordinates[1]
    y = crop_coordinates[0]
    h = crop_coordinates[3]
    w = crop_coordinates[2]

    image = image.crop((y, x, y+w, x+h))
    image = image.resize((ARRAY_WIDTH, ARRAY_HEIGHT))
    
    nparray = np.asarray(image.getdata()).reshape(image.size[1], image.size[0])
    
    return nparray   
    
def split_test_image_into_np_shapes(folder_path, filename):
    """Takes an image file as input and returns list of 200x200 numpy arrays containing 
    individual shapes from the input image"""
    
    shapes_np_array = []
        
    image_path = os.path.realpath(folder_path + '\\' + filename)
    
    cvimage = cv2.imread(image_path)
    
    edged = cv2.Canny(cvimage, 10, 250)
    (im, contours, hier) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for fragment in contours:
        
        crop_coordinates = cv2.boundingRect(fragment)
    
        image = PIL.Image.open(image_path)
        image = image.convert('L')
        nparray = np.asarray(image.getdata()).reshape(image.size[1], image.size[0])
    
        x = crop_coordinates[1]
        y = crop_coordinates[0]
        h = crop_coordinates[3]
        w = crop_coordinates[2]

        image = image.crop((y, x, y+w, x+h))
        image = image.resize((ARRAY_WIDTH, ARRAY_HEIGHT))
            
        nparray = np.asarray(image.getdata()).reshape(image.size[1], image.size[0])
        shapes_np_array.append(nparray)
                
    return shapes_np_array, contours 

def learn_drawn_shapes():
    global drawn_images_folder_path
    global number_of_types
    global drawn_images
    
    for f in os.listdir(drawn_images_folder_path):    
        
        image_array = create_image_array(drawn_images_folder_path, f, drawn_shape_types)
        drawn_images.append(image_array)
        add_type_to_list(drawn_shape_types, f)
        shape_dictionary[number_of_types] = f

    number_of_types += 1
    drawn_images = np.array(drawn_images)
    return drawn_images
    
    
def import_source_images(show_plotted=False):
    global source_images_folder_path
    global source_images
    global source_shape_types
    
    source_shape_types = []
    source_images = []
    
    for f in os.listdir(source_images_folder_path):    
        
        image_array = create_image_array(source_images_folder_path, f, source_shape_types)
        source_images.append(image_array)
        add_type_to_list(source_shape_types, f)
        
        if show_plotted:
            plt.matshow(image_array)
            plt.show()
            
def import_test_images():
    
    global test_images 
    test_images = []
    test_borders = []
    
    for f in os.listdir(test_images_folder_path):    
        shapes_list, test_borders = split_test_image_into_np_shapes(test_images_folder_path, f)
        
        for img_array in shapes_list:
            test_images.append(img_array) 
            add_type_to_list(test_shape_types, f)
            
    test_images = np.array(test_images)
    
    return test_borders

def init_classifier():
    
    global source_shape_types    
    global source_images
    global test_images
    global test_shape_types
    
    source_images = np.array(source_images)
    source_shape_types = np.array(source_shape_types)
    test_images = []
    test_shape_types = np.array(test_shape_types)
    
    print(shape_dictionary)
    
    clf.fit(source_images.reshape(len(source_images),-1)[:], source_shape_types[:])
    
def predict():
    
    shape_names = []       
    shape_images = []

    for ti in test_images:
        results = clf.predict(ti.reshape(-1, ti.ravel().size))
        shape_images.append(plt.matshow(ti[0:]))
        plt.show()
        
        print(shape_dictionary[results[0]])
        print(results[0])
        shape_names.append(shape_dictionary[results[0]])
    
    n, _p, _q = test_images.shape   
    print(n, 'shapes currently on the canvas')
    return shape_names
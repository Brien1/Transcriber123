import base64 as base64
import os
import sys
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path += [PARENTDIR,]
print(PARENTDIR)
def show_predicted_image(y_predict):
    """Takes the base64 string output from the model and converts it to a image, 
    and writes in static/new_image.png

    Args:
        y_predict (ndarray): Shape is (1,), a single string contained within a np.array
    """
    with open (PARENTDIR+"/application/static/new_image.png","bw") as tempwrite:
        tempwrite.write(base64.b64decode(y_predict))
   
    
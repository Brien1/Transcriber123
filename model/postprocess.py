import base64 as base64
def show_predicted_image(y_predict):
    """Takes the base64 string output from the model and converts it to a image, 
    and writes in static/new_image.png

    Args:
        y_predict (ndarray): Shape is (1,), a single string contained within a np.array
    """
    with open ("application/static/new_image.png","bw") as tempwrite:
        tempwrite.write(base64.b64decode(y_predict))
   
    
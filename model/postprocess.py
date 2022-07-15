import base64 as base64
import matplotlib.pyplot as plt
def show_predicted_image(y_predict):
    """Takes the base64 string output from the model and converts it to a image, 
    then displays it

    Args:
        y_predict (ndarray): Shape is (1,), a single string contained within a np.array
    """
    with open ("new_image.png","bw") as tempwrite:
        tempwrite.write(base64.b64decode(y_predict))
    plt.imshow(plt.imread(fname="new_image.png"))
    return "new_image.png"
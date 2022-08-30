import sys, os
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
ROOTDIR = os.path.dirname(PARENTDIR)
sys.path += [PARENTDIR,]
import model.postprocess  as pp
import unittest
import librosa
import pickle
import logging
print(PARENTDIR)
class test_postprocess(unittest.TestCase):
    def test_show_image(self):
        loaded_test_audio, sr = librosa.load(os.path.join(CURRENTDIR,"A0-test.mp3"))
        loaded_test_audio = librosa.util.fix_length(data=loaded_test_audio,size=32702)
        f1 = pickle.load(open(os.path.join(PARENTDIR,"model/model1.pkl"), 'rb'))
        f2 = pickle.load(open(os.path.join(PARENTDIR,"model/model2.pkl"), 'rb'))
        
        model_byte_string = f1+ f2
        loaded_model = pickle.loads(model_byte_string)  



        output = loaded_model.predict([loaded_test_audio])
        os.remove(PARENTDIR+"/application/static/new_image.png")
        self.assertFalse(os.path.exists(PARENTDIR+"/application/static/new_image.png"))
        pp.show_predicted_image(output)
        self.assertTrue(os.path.exists(PARENTDIR+"/application/static/new_image.png"))


if __name__ == '__main__':
    unittest.main()

import sys, os
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
sys.path += [PARENTDIR,]
import model.postprocess  as pp
import unittest
import librosa
import pickle
import logging
print(CURRENTDIR)
class test_postprocess(unittest.TestCase):
    def test_increment(self):
        loaded_test_audio, sr = librosa.load(os.path.join(CURRENTDIR,"A0-test.mp3"))
        loaded_test_audio = librosa.util.fix_length(data=loaded_test_audio,size=32702)
        loaded_model = pickle.load(open(os.path.join(PARENTDIR,"model/model.pkl"), 'rb'))



        output = loaded_model.predict([loaded_test_audio])
        
        self.assertEqual(pp.show_predicted_image(output),0)


if __name__ == '__main__':
    unittest.main()

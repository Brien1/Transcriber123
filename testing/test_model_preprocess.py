import sys, os
CURRENTDIR = os.path.dirname(os.path.realpath(__file__))
PARENTDIR = os.path.dirname(CURRENTDIR)
ROOTDIR = os.path.dirname(PARENTDIR)
sys.path += [PARENTDIR,]
import model.preprocess  as pp
import unittest
import librosa

print(PARENTDIR)
class test_preprocess(unittest.TestCase):
    def test_resize_audio(self):
        loaded_test_audio, sr = librosa.load(os.path.join(CURRENTDIR,"A0-test.mp3"))
        oldsize = len(loaded_test_audio)
        print(oldsize)
        newsize = pp.resizeaudio([loaded_test_audio],True)
        print(len(newsize[0]))
        self.assertTrue(oldsize!=newsize)
        self.assertTrue(len(newsize[0]) == 64000)
        


        
if __name__ == '__main__':
    unittest.main()
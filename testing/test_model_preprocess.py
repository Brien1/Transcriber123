import sys, os, numpy as np
from numpy import array
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
        
    def test_envelope(self):
        env = pp.compute_envelope(np.array([2,5,2,7,1]))
        print(env.__str__)
        assert(env[0]== array([7., 7., 7., 7., 7.])).all()
        assert (env[1]== array([7., 7., 7., 7., 7.])).all()
        assert (env[2]== array([1., 1., 1., 1., 1.])).all()
    
    def test_detect_note_sample_range(self):
        loaded_test_audio, sr = librosa.load(os.path.join(CURRENTDIR,"A0-test.mp3"))
        env,u,l = pp.compute_envelope(loaded_test_audio,Fs=sr)
        rangetuple = pp.detect_note_sample_range(env)
        assert rangetuple == [(385, 390), (555, 560), (635, 640)]

if __name__ == '__main__':
    unittest.main()
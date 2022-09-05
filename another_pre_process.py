import os,sys,librosa,librosa.display, matplotlib.pyplot as plt, numpy as np, soundfile as sf
path = "/Users/brienhall/Downloads/My recording 11.wav"
path2 = "/Users/brienhall/Documents/FinalProject/linear_dataset/C4/C4-5.mp3"
audio, sr = librosa.load(path)
LOUD = 0.030
QUIET = 0.005
def compute_envelope(x, win_len_sec=0.01, Fs=4000):
    """Computation of a signal's envelopes
    code lifted from https://www.audiolabs-erlangen.de/resources/MIR/FMP/C1/C1S3_Timbre.html
    USING THE MAGNITUDE ENVELOPE MAY SIMPLIFY INPUT

    Notebook: C1/C1S3_Timbre.ipynb

    Args:
        x (np.ndarray): Signal (waveform) to be analyzed
        win_len_sec (float): Length (seconds) of the window (Default value = 0.01)
        Fs (scalar): Sampling rate (Default value = 4000)

    Returns:
        env (np.ndarray): Magnitude envelope
        env_upper (np.ndarray): Upper envelope
        env_lower (np.ndarray): Lower envelope
    Doctest:
    >>> compute_envelope(np.array([2,5,2,7,1]))
    (array([7., 7., 7., 7., 7.]), array([7., 7., 7., 7., 7.]), array([1., 1., 1., 1., 1.]))

    """
    win_len_half = round(win_len_sec * Fs * 0.5)
    N = x.shape[0]
    env = np.zeros(N)
    env_upper = np.zeros(N)
    env_lower = np.zeros(N)
    for i in range(N):
        i_start = max(0, i - win_len_half)
        i_end = min(N, i + win_len_half)
        env[i] = np.amax(np.abs(x)[i_start:i_end])
        env_upper[i] = np.amax(x[i_start:i_end])
        env_lower[i] = np.amin(x[i_start:i_end])
    return env, env_upper, env_lower


def detect_note_sample_range(magnitude_envelope):
    """Takes the magnitude profile of a soundwave containing multiple notes, returns list of tuples [(note_start,note_end), ....]
    

    Args:
        magnitude_envelope (np.array): 

    Returns:
        list[(int,int), ... ,(int,int)]: returns list where each element (a tuple) is a note event with a start and end 
        sample (time * ML_SAMPLE_RATE)
    Doctest:
    >>> detect_note_sample_range([5.,1.,4.,2.,1.,8.,0,0,0,0,0,0])
    [(0, 5)]
    """
    if max(magnitude_envelope) > 0.5:
        GRADIENT = LOUD
    else:
        GRADIENT = QUIET
    gradients = []
    samples = []
    sample_separation = 5
    for sample in range(len(magnitude_envelope)-sample_separation) :
        
        if sample % sample_separation ==0:
            gradient = (magnitude_envelope[sample+sample_separation]-magnitude_envelope[sample])/((sample+sample_separation)-sample)
            gradients.append(gradient)
            samples.append((sample,sample+sample_separation))

    unconnected_note_events = []
    for n ,  gradient in enumerate(gradients):
        if gradient > GRADIENT:  #N.b. for loud notes 0.3, for quiet 0.005
            unconnected_note_events.append(samples[n])
    note_events = []
    previous_note_event = []
    for n, event in enumerate(unconnected_note_events):
        if n == 0 :
            previous_note_event.append(event) 
        if previous_note_event[0][1] + 21 > event[0]: #connected event
            previous_note_event[0] = (previous_note_event[0][0], event[1])
        else:
            note_events.append(previous_note_event[0])
            previous_note_event[0] = event
        if n == len(unconnected_note_events) - 1 :
            note_events.append(previous_note_event[0])

    return note_events

env, envupper,envlower = compute_envelope(audio,Fs=sr)
notes = detect_note_sample_range(env)

print(notes)
cutaduio = audio[notes[0][0]-300:35000]
librosa.display.waveshow(cutaduio)
plt.show()


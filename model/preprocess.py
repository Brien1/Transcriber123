import librosa
def resizeaudio(audio, max_l):
    """Resizes the audio to a certian number of bytes, which is essential for feeding
    into the .fit() method

    Args:
        audio (list/ array): where each element is a list of float values reperesenting an image
        max_l (_type_): True will add trailing zeros (bytes) onto the end of shorter audio samples
                        False will cut the audio to the matches the shortes in the list

    Returns:
        _type_: list
    """
    audio_lengths = [32702,64000]
    if max_l :
        audio = [librosa.util.fix_length(f, max(audio_lengths)) for f in audio]
    else:
        audio = [librosa.util.fix_length(f, min(audio_lengths)) for f in audio]
        
    return audio


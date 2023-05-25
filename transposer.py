import wave
import numpy as np

old_audio = wave.open('old_sample.wav', 'r')

# Set the parameters for the output file.
par = list(old_audio.getparams())
par[3] = 0  # The number of samples will be set by writeframes.
par = tuple(par)
new_audio = wave.open('new_sample.wav', 'w')
new_audio.setparams(par)

fr = 20 # Lower framerate increases reverb
sz = old_audio.getframerate()//fr  # Read and process 1/fr second at a time.

file_length = int(old_audio.getnframes()/sz)  # count of the whole file
shift = 100//fr  # shifting 100 Hz
# TODO: allow user input: shift amount, or subtract current key hertz to desired key. 
# TODO: detect key of user inputted file.

# Read data, split it in left and right channel (assuming a stereo WAV file).
for num in range(file_length):
    da = np.fromstring(old_audio.readframes(sz), dtype=np.int16)
    left, right = da[0::2], da[1::2]

    # Extract the frequencies using the Fast Fourier Transform!!
    lf, rf = np.fft.rfft(left), np.fft.rfft(right)

    # Roll the array to increase the pitch.
    lf, rf = np.roll(lf, shift), np.roll(rf, shift)

    # The highest frequencies roll over to the lowest ones. That's not what we want, so zero them.
    lf[0:shift], rf[0:shift] = 0, 0

    # use inverse Fourier transform to convert the signal back into amplitude. (??)
    nl, nr = np.fft.irfft(lf), np.fft.irfft(rf)

    # Combine left and right channels.
    ns = np.column_stack((nl, nr)).ravel().astype(np.int16)

    new_audio.writeframes(ns.tostring())

old_audio.close()
new_audio.close()
import pyaudio, atexit

AudioPort = pyaudio.PyAudio()
atexit.register(lambda : AudioPort.terminate())

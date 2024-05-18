import pygame
import numpy as np
import pyaudio

# Initialize Pygame
pygame.init()

# Set up the display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Live Audio Waveform")

# Set up PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read audio data from the stream
    data = stream.read(CHUNK)
    numpy_data = np.frombuffer(data, dtype=np.int16)

    # Normalize audio data to fit within the window height
    normalized_data = np.interp(numpy_data, (-32768, 32767), (0, WINDOW_HEIGHT))

    # Clear the window
    window.fill((0, 0, 0))

    # Draw the waveform
    for i in range(len(normalized_data) - 1):
        pygame.draw.line(window, (255, 255, 255), (i, normalized_data[i]), (i + 1, normalized_data[i + 1]))

    # Update the display
    pygame.display.flip()

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()

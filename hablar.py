import subprocess
import pygame
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

def hablar(texto, idioma='es'):
    """
    Usa gTTS para pronunciar el texto dado en el idioma especificado.
    :param texto: Texto a pronunciar.
    :param idioma: Código del idioma (por defecto 'es' para español).
    """
    try:
        tts = gTTS(texto, lang=idioma)
        
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        audio = AudioSegment.from_mp3(audio_buffer)
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": 44100})
        new_sample_rate = int(audio.frame_rate * (2.0 ** 0))
        audio = audio.set_frame_rate(44100)
        
        audio_buffer = BytesIO()
        audio.export(audio_buffer, format="wav")
        audio_buffer.seek(0)
        
        pygame.mixer.pre_init(frequency=44100)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_buffer, "wav")
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            continue

    except FileNotFoundError:
        print("eSpeak no está instalado o no se encuentra en el PATH.")

# Ejemplo de uso
# hablar("Hola, ¿cómo estás?", idioma='es')

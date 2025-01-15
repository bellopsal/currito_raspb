import subprocess
import pygame
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import google.generativeai as genai
genai.configure(api_key="AIzaSyA3TwfeFqaU_23GhnQ19V3_mrrz6K_WEK8")

def hablar(texto, idioma='es'):
    """
    Usa gTTS para pronunciar el texto dado en el idioma especificado.
    :param texto: Texto a pronunciar.
    :param idioma: Código del idioma (por defecto 'es' para español).
    """
#     print("hablar"+ texto)
    try:
        tts = gTTS(texto, lang=idioma)
        
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        audio = AudioSegment.from_mp3(audio_buffer)
        audio = audio._spawn(audio.raw_data, overrides={"frame_rate": 44100})
        new_sample_rate = int(audio.frame_rate * (1.2 ** 0))
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

def generate_text(prediction):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Tell me two interesting facts for a kid about {prediction}. Start with Here a fun fact about {prediction}  and say the two facts Make it short and in spanish, do not include any punctuation as * ")
    return response.text

# Ejemplo de uso
# hablar("Hola, ¿cómo estás?", idioma='es')

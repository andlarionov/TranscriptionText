import os
import streamlit as st
import moviepy.editor as mp
from faster_whisper import WhisperModel
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from youtube_transcript_api import YouTubeTranscriptApi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from yake import KeywordExtractor


import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Загружаем модель Whisper
model = WhisperModel("small")

def process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio):
    if subtitres_whisper == 'Распознать загруженное аудио/видео':
        if t_audio != "" and not (t_audio is None): # Распознаём аудио-файл
            return GetTextFromVideoAudio(t_audio)   
        elif t_video != "" and not (t_video is None):
            return GetTextFromVideoAudio(t_video)   # Распознаём видео-файл
    
    # Извлекаем видео ID из URL
    if ('v=' in sURL and sURL[:30] == 'https://www.youtube.com/watch?') or ('shorts/' in sURL and sURL[:31] == 'https://www.youtube.com/shorts/'):
        # Получаем информацию о видео
        yt = YouTube(sURL)
        if subtitres_whisper == 'Использовать субтитры YouTube':
            # Извлекаем субтитры
            return GetSubtitles(subtitres_lang, yt)
        elif subtitres_whisper == 'Распознать аудио с YouTube':
            # Анализ аудио
            return GetTextFromVideoYt(yt)
        
    return "Укажите параметры работы с видео материалом."

# получаем субтитры с Ютьб
def GetSubtitles(first_language_code, yt):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(yt.video_id)
    except Exception:
        return "Не удалось получить субтитры из видео. \nПопробуйте выбрать другие параметры работы с видео. \nНапример: Распознать аудио с YouTube"

    available_subtitles = {transcript.language_code: transcript for transcript in transcript_list}
    translatable_subtitles = {transcript.language_code: transcript for transcript in transcript_list if transcript.is_translatable}

    subtitles_text = ''
    languages_text = 'Базовые языки:\n' + '\n'.join(f'   - {code} - {transcript.language}' for code, transcript in available_subtitles.items())

    if first_language_code in available_subtitles:
        subtitles_text = '\n'.join(s1['text'] for s1 in available_subtitles[first_language_code].fetch())
    elif first_language_code in {tr_l['language_code'] for tr_l in translatable_subtitles[first_language_code].translation_languages}:
        subtitles_text = '\n'.join(s1['text'] for s1 in translatable_subtitles[first_language_code].translate(first_language_code).fetch())
    else:
        languages_text += '\nПереводы:\n' + '\n'.join(f'   - Базовый язык {transcript.language_code} - {transcript.language}. Переводы:\n' + '      - ' + '\n      - '.join(f'{tr_l["language_code"]} - {tr_l["language"]}' for tr_l in transcript.translation_languages) for transcript in translatable_subtitles.values())
        return f"Указанный код языка не найден. Возможно выбрать указанные ниже языки:\n{languages_text}"

    return subtitles_text


# Работа с аудио/видео на локальном диске
def GetTextFromVideoAudio(fileName):
    segments = model.transcribe(fileName)[0]
    sText = ''
    for segment in segments:
        sText += segment.text

    return sText

# получаем аудио с Ютьюб
def GetTextFromVideoYt(yt):
    try:
        fileName = yt.streams.filter(type="audio").first().download()
    except AgeRestrictedError as e:
        return "Видео имеет возрастные ограничения, и к нему невозможно получить доступ без входа в систему.. \nПопробуйте выбрать другие параметры работы с видео. \nНапример: Распознать загруженное аудио/видео"
    except:
        return "Не удалось получить аудио из видео." 
    audio_file = mp.AudioFileClip(fileName)
    writeFileName = "vrem.wav"
    audio_file.write_audiofile(writeFileName)

    sText = GetTextFromVideoAudio(writeFileName)
    os.remove(fileName)
    os.remove(writeFileName)
    return sText

def process_summarize(sIn):
    if sIn != "" and not (sIn is None) and sIn != "...":
        summarizer = LsaSummarizer()
        parser = PlaintextParser.from_string(sIn, Tokenizer("russian"))
        summarized_text = summarizer(parser.document, sentences_count=10)  # Меняем число предложений
        return "\n".join(str(sentence) for sentence in summarized_text)
    else:
        return 'Необходимо заполнить поле субтитров'


def Keyword_1(sIn):
    if sIn != "" and not (sIn is None) and sIn != "...":
        extractor = KeywordExtractor(lan="ru", n=1, top=10, features=None)
        keywords = extractor.extract_keywords(sIn)
        # Изменяем способ объединения ключевых слов, используя ';' в качестве разделителя
        return '; '.join([word[0] for word in keywords]).capitalize()
    else:
        return 'Необходимо заполнить поле субтитров'
    

if __name__ == '__main__':

    st.header('Транскрибация и суммаризация')
    st.subheader('Приложение, которое позволяет получить краткий отчет из '
            'контента на YouTube или локальных файлов. :tv: :arrow_forward: :memo:')

    t_sURL = st.text_input(
            "Введите ссылку на видео из YouTube",
            "https://www.youtube.com/watch?v=6EsCI3CbmTk", 
            on_change=st.session_state.clear)

    t_subtitres_whisper = st.radio(
            "Выберите способ получения текста из YouTube",
            ["Использовать субтитры YouTube", "Распознать аудио с YouTube", "Распознать загруженное аудио/видео"], 
            on_change=st.session_state.clear)

    t_subtitres_lang = st.selectbox(
        'Язык субтитров',
        ('RU', 'EN')).lower()
    

    t_video = st.file_uploader("Выберете видео файл для распознавания", accept_multiple_files=False, on_change=st.session_state.clear)
    t_audio = st.file_uploader("Выберете аудио файл для распознавания", accept_multiple_files=False, on_change=st.session_state.clear)

    def click_button0():
        if not t_sURL and not t_video and not t_audio:
            st.session_state['result0'] = "Укажите ссылку на видео или загрузите видео/аудио файл"
            return
        if t_subtitres_whisper == 'Использовать субтитры YouTube' and not t_subtitres_lang:
            st.session_state['result0'] = "Укажите язык субтитров"
            return
        st.session_state['result0'] = process_video(t_subtitres_whisper, t_sURL, t_subtitres_lang, t_video, t_audio)



    text_label0 = 'Субтитры из видео/аудио'
    button_name0 = 'Получить субтитры'
    if 'result0' not in st.session_state:
        st.session_state['result0'] = '...'
    st.text_area(text_label0, st.session_state['result0'], key='0')
    col1, col2, col3 = st.columns([4, 1.75, 0.6])
    with col2:
        st.button(button_name0, on_click=click_button0, key='00')
    with col3:
        st.download_button(label=":inbox_tray:", data=st.session_state['result0'], mime="text/plain", key='000', file_name=f"{button_name0[9:].capitalize()}.txt")

    def click_button1():
        if 'result0' not in st.session_state or st.session_state['result0'] == '' or st.session_state['result0'] == 'Укажите ссылку на видео или загрузите видео/аудио файл' or st.session_state['result0'] == 'Укажите язык субтитров':
            st.session_state['result1'] = "Сначала получите субтитры из видео/аудио"
            return
        st.session_state['result1'] = process_summarize(st.session_state['result0'])
    

    text_label1 = 'Краткий отчет'
    button_name1 = 'Получить краткий отчет'
    if 'result1' not in st.session_state:
        st.session_state['result1'] = '...'
    st.text_area(text_label1, st.session_state['result1'], key='1')
    col1, col2, col3 = st.columns([4, 2.2, 0.6])
    with col2:
        st.button(button_name1, on_click=click_button1, key='11')
    with col3:
        st.download_button(label=":inbox_tray:", data=st.session_state['result1'], mime="text/plain", key='111', file_name=f"{button_name1[9:].capitalize()}.txt")

    def click_button2():
        if 'result0' not in st.session_state or st.session_state['result0'] == '' or st.session_state['result0'] == 'Укажите ссылку на видео или загрузите видео/аудио файл' or st.session_state['result0'] == 'Укажите язык субтитров':
            st.session_state['result2'] = "Сначала получите субтитры из видео/аудио"
            return
        st.session_state['result2'] = Keyword_1(st.session_state['result0'])

    text_label2 = 'Ключевые слова'
    button_name2 = 'Получить ключевые слова'
    if 'result2' not in st.session_state:
        st.session_state['result2'] = '...'
    st.text_area(text_label2, st.session_state['result2'], key='2')
    col1, col2, col3 = st.columns([4, 2.35, 0.6])
    with col2:
        st.button(button_name2, on_click=click_button2, key='22')
    with col3:
        st.download_button(label=":inbox_tray:", data=st.session_state['result2'], mime="text/plain", key='222', file_name=f"{button_name2[9:].capitalize()}.txt")


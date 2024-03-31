import gradio as gr
import os
import moviepy.editor as mp
from faster_whisper import WhisperModel
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Загружаем модель Whisper
model = WhisperModel("large-v2")


def save_text_to_word(text, file_path):
    """Сохраняет текст в файл формата Word (DOCX)."""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(file_path)


def process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio):
    # Распознаём аудио-файл
    if t_audio != "" and not (t_audio is None):
        return GetTextFromVideoAudio(t_audio)
    # Распознаём видео-файл
    if t_video != "" and not (t_video is None):
        return GetTextFromVideoAudio(t_video)


    # Извлекаем видео ID из URL
    if 'v=' in sURL and sURL[:len('https://www.youtube.com/watch?')] == 'https://www.youtube.com/watch?':
        # Получаем информацию о видео
        yt = YouTube(sURL)
        if subtitres_whisper == 'Субтитры':
            # Извлекаем субтитры
            return GetSubtitres(subtitres_lang, yt)

        if subtitres_whisper == 'Распознать аудио':
            # Анализ аудио
            return GetTextFromVideoYt(yt)

    return "Укажите параметры работы с видео материалом."


# получаем субтитры с Ютьб
def GetSubtitres(first_language_code, yt):

    sLang = 'Базовые языки:' + '\n'
    bFind = False
    transcript_list = YouTubeTranscriptApi.list_transcripts(yt.video_id)
    for transcript in transcript_list:
        sLang += '   - ' + transcript.language_code + ' - ' + transcript.language + '\n'
        if transcript.language_code == first_language_code:
            Text_sub = transcript.fetch()
            bFind = True
            break
    sLang += '\n' + 'Переводы:' + '\n'

    if not bFind:
        for transcript in transcript_list:
            if transcript.is_translatable is True:
                sLang += '   - Базовый язык ' + transcript.language_code + ' - ' + transcript.language + '. Переводы:\n'
                for tr_l in transcript.translation_languages:
                    sLang += '      - ' + tr_l['language_code'] + ' - ' + tr_l['language'] + '\n'
                    if tr_l['language_code'] == first_language_code:
                        Text_sub = transcript.translate(first_language_code).fetch()
                        bFind = True
                        break
    sText = ''
    if bFind:
        for s1 in Text_sub:
            sText += s1['text'] + '\n'
        return sText
    else:
        return "Указанный код языка не найден. Возможо выбрать указанные ниже языки:" + '\n' + sLang


# получаем аудио с Ютьюб
def GetTextFromVideoYt(yt):
    fileName = yt.streams.filter(type="audio").first().download()
    audio_file = mp.AudioFileClip(fileName)
    audio_file.write_audiofile("vrem.wav")

    segments, info = model.transcribe("vrem.wav")
    sText = ''
    for segment in segments:
        sText += segment.text
    os.remove(fileName)
    os.remove("vrem.wav")

    return sText


# Работа с аудио/видео на локальном диске
def GetTextFromVideoAudio(fileName):
    audio_file = mp.AudioFileClip(fileName)
    audio_file.write_audiofile("vrem.wav")
    segments, info = model.transcribe("vrem.wav")
    sText = ''
    for segment in segments:
        sText += segment.text

    os.remove(fileName)
    os.remove("vrem.wav")

    return sText


def process_summarize(sIn):
    if sIn != "" and not (sIn is None):
        summarizer = LsaSummarizer()
        parser = PlaintextParser.from_string(sIn, Tokenizer("russian"))
        summarized_text = summarizer(parser.document, sentences_count=10)  # Меняем число предложений
    return "\n".join(str(sentence) for sentence in summarized_text)
    return 'Необходимо заполнить поле стенограмма'


with gr.Blocks() as demo:
    with gr.Column(scale=2):
        t_subtitres_whisper = gr.Radio(["Субтитры", "Распознать аудио"], label="Вариант исполнения на YouTube:")
        t_sURL = gr.Text("https://www.youtube.com/watch?v=6EsCI3CbmTk", label="YouTube - ссылка на страницу с видео")
        t_subtitres_lang = gr.Text("ru", label="Язык субтитров (основной либо перевод (указывается код): ru, en ...)")
        t_video = gr.Video(sources=['upload'])
        t_audio = gr.Audio(type='filepath', sources=['upload'])
        btn = gr.Button(value="Сформировать стенограмму")
        t_stenogr = gr.Text("", label="Стенограмма:")
        btn_summarize = gr.Button(value="Суммаризировать стенограмму")
        t_summarize = gr.Text("", label="Суммаризация:")

        btn.click(process_video, inputs=[t_subtitres_whisper, t_sURL, t_subtitres_lang, t_video, t_audio], outputs=[t_stenogr])
        btn_summarize.click(process_summarize, inputs=[t_stenogr], outputs=[t_summarize])

        # Кнопка для сохранения транскрибированного текста в Word
        btn_save_to_word = gr.Button(value="Сохранить в Word")
        btn_save_to_word.click(lambda text: save_text_to_word(text, "transcribed_text.docx"), inputs=[t_stenogr])


demo.launch(share=True)



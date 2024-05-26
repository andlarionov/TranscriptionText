import wm as wm5


def test_YTsubtitres():
    # Выдергиваем субтитры
    subtitres_whisper = 'Субтитры'
    sURL = 'https://www.youtube.com/watch?v=6EsCI3CbmTk'
    subtitres_lang = 'ru'
    t_video = ''
    t_audio = ''

    result = wm5.process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio)
    result = result.strip()
    sResult = 'Ну что дружище'

    assert result[:len(sResult)] == sResult


def test_YTvideo():
    # распознаём аудио на ютюб
    subtitres_whisper = 'Распознать аудио'
    sURL = 'https://www.youtube.com/watch?v=6EsCI3CbmTk'
    subtitres_lang = 'ru'
    t_video = ''
    t_audio = ''

    result = wm5.process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio)
    result = result.strip()
    sResult = 'Ну что, дружище'

    assert result[:len(sResult)] == sResult


def test_audio():
    # распознаём аудио файл (в папке с проверяемым фалом д/б ещё файл Kati_k_kasse.mp3)
    subtitres_whisper = 'Распознать аудио'
    sURL = 'https://www.youtube.com/watch?v=6EsCI3CbmTk'
    subtitres_lang = 'ru'
    t_video = ''
    t_audio = 'Kati_k_kasse.mp3'

    result = wm5.process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio)
    result = result.strip()
    sResult = 'Наш покупал'

    assert result[:len(sResult)] == sResult


def test_video():
    # распознаём видео файл (в папке с проверяемым фалом д/б ещё файл Kati_k_kasse.mp3)
    subtitres_whisper = 'Распознать аудио'
    sURL = 'https://www.youtube.com/watch?v=6EsCI3CbmTk'
    subtitres_lang = 'ru'
    t_video = 'Savvateev.mp4'
    t_audio = ''

    result = wm5.process_video(subtitres_whisper, sURL, subtitres_lang, t_video, t_audio)
    result = result.strip()
    sResult = 'Передаю слово Алексею Владимировичу Саватееву'

    assert result[:len(sResult)] == sResult

def test_process_summarize_valid(mocker):
    input_text = "Это пример текста. Это пример текста. Это пример текста. Это пример текста."
    summarizer_mock = mocker.patch('your_module.LsaSummarizer')
    summarizer_instance = summarizer_mock.return_value
    summarizer_instance.__call__.return_value = ["Это пример текста."]
    mocker.patch('your_module.PlaintextParser.from_string', return_value=Mock())

    result = process_summarize(input_text)
    assert "Это пример текста." in result

def test_keyword_extraction_valid(mocker):
    input_text = "Это пример текста, который содержит ключевые слова."
    extractor_mock = mocker.patch('your_module.KeywordExtractor')
    extractor_instance = extractor_mock.return_value
    extractor_instance.extract_keywords.return_value = [('ключевые', 0.1), ('слова', 0.2)]

    result = Keyword_1(input_text)
    assert "Ключевые; Слова" in result

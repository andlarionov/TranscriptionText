import wm6 as wm5


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

import wm as wm5


def test_YTsubtitres():
    # Выдергиваем субтитры
    subtitres_whisper = "Использовать субтитры YouTube"
    sURL = "https://www.youtube.com/watch?v=6EsCI3CbmTk"
    subtitres_lang = "ru"
    t_video = ""
    t_audio = ""

    result = wm5.process_video(
        subtitres_whisper, sURL, subtitres_lang, t_video, t_audio
    )
    result = result.strip()
    sResult = "Ну что дружище"

    assert result[: len(sResult)] == sResult


def test_YTvideo():
    # распознаём аудио на ютюб
    subtitres_whisper = "Распознать аудио с YouTube"
    sURL = "https://www.youtube.com/watch?v=6EsCI3CbmTk"
    subtitres_lang = "ru"
    t_video = ""
    t_audio = ""

    result = wm5.process_video(
        subtitres_whisper, sURL, subtitres_lang, t_video, t_audio
    )
    result = result.strip()
    sResult = "Ну что, дружище"

    assert result[: len(sResult)] == sResult


def test_audio():
    """распознаём аудио файл
    (файл в папке с проверяемым фалом д/б ещё файл Kati_k_kasse.mp3)"""
    subtitres_whisper = "Распознать загруженное аудио/видео"
    sURL = "https://www.youtube.com/watch?v=6EsCI3CbmTk"
    subtitres_lang = "ru"
    t_video = ""
    t_audio = "Kati_k_kasse.mp3"

    result = wm5.process_video(
        subtitres_whisper, sURL, subtitres_lang, t_video, t_audio
    )
    result = result.strip()
    sResult = "Наш покупал"

    assert result[: len(sResult)] == sResult


def test_video():
    """распознаём видео файл
    (файлв папке с проверяемым фалом д/б ещё файл Savvateev.mp4)"""
    subtitres_whisper = "Распознать загруженное аудио/видео"
    sURL = "https://www.youtube.com/watch?v=6EsCI3CbmTk"
    subtitres_lang = "ru"
    t_video = "Savvateev.mp4"
    t_audio = ""

    result = wm5.process_video(
        subtitres_whisper, sURL, subtitres_lang, t_video, t_audio
    )
    result = result.strip()
    sResult = "Передаю слово"

    assert result[: len(sResult)] == sResult


def test_process_summarize_valid():
    # Используем достаточно длинный текст для тестирования
    input_text = """
    Это пример текста, который предназначен для проверки функции суммаризации.\
    Текст содержит несколько предложений,которые описывают функциональность и\
    позволяют убедиться в корректности работы алгоритма.\nСуммаризация текста\
    - важная задача, которая позволяет выделить наиболее значимые части\
    длинного текста и представить их в сокращенном виде. Функция должна\
    корректно выбирать ключевые предложения,\
    которые наиболее полно отражают содержание всего текста.
    """
    result = wm5.process_summarize(input_text)

    # Проверяем, что результат короче исходного текста, но не пустой
    assert len(result) < len(input_text) and len(result) > 0

    # Проверяем, что результат содержит ключевые слова из исходного текста
    key_words = ["суммаризация", "важная", "значимые", "содержание"]
    assert any(key_word in result.lower() for key_word in key_words)


def test_keyword_extraction_valid():
    input_text = "Это пример текста, который содержит ключевые слова."
    result = wm5.Keyword_1(input_text)

    # Ожидаемые ключевые слова, не важен порядок, важно наличие
    expected_keywords = ["ключевые", "слова", "текста", "содержит", "пример"]

    # Приведем результат к нижнему регистру для универсальности сравнения
    result_lower = result.lower()

    # Проверяем, что все ожидаемые ключевые слова есть в результате
    assert all(keyword in result_lower for keyword in expected_keywords)

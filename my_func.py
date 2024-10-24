import re
import nltk
from wordcloud import WordCloud
from nltk.corpus import stopwords as nltk_stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
# создадим множество со стоп словами для русского и английского языка
stop_words = set(nltk_stopwords.words('english')).union(set(nltk_stopwords.words('russian'))) # добавить stopwords для других яызков
lemmatizer = WordNetLemmatizer()

# очистка текста 
def clear_text(text):
    text = str(text).lower()
    re_text = re.sub(r'[^a-zA-Zа-яА-Я0-9]', ' ', text.partition('http')[0])
    #res = " ".join(re_text.lower().split())
    res = re.sub(r'\s+', ' ', re_text).strip()
    
    return res

# лемматизация текса
def lemmatize(text):
    text = nltk.word_tokenize(text)
    text = [word for word in text if word not in stop_words] # для русского языка stemmer.stem(word)
    text = ' '.join([lemmatizer.lemmatize(w) for w in text])
    return text

# очистка текста от мусорных слов
def remove_words(df, column_name, words_to_remove):
    # Создаем регулярное выражение из списка слов
    pattern = r'\b(' + '|'.join(map(re.escape, words_to_remove)) + r')\b'
    
    # Функция для удаления слов из строки
    def clean_text(text):
        return re.sub(pattern, '', text, flags=re.IGNORECASE).strip()
    
    # Применяем функцию ко всем строкам в указанном столбце
    df[column_name] = df[column_name].apply(clean_text)
    return df

# Получение текстовой строки из списка слов
def str_corpus(corpus):
    str_corpus = ''
    for i in corpus:
        str_corpus += ' ' + i
    str_corpus = str_corpus.strip()
    return str_corpus

# Получение списка всех слов в корпусе
def get_corpus(data):
    corpus = []
    for phrase in data:
        for word in phrase.split():
            corpus.append(word)
    return corpus

# Получение облака слов
def get_wordCloud(corpus):
    wordCloud = WordCloud(background_color='white',
                              stopwords=stop_words,
                              width=3000,
                              height=2500,
                              max_words=200,
                              random_state=42
                         ).generate(str_corpus(corpus))
    return wordCloud

# замена значений в целевой переменной
def replace_values(df, index_list, correct_cartoon):
    df.loc[df.index.isin(index_list), 'cartoon'] = correct_cartoon
    return df
import os
import re
import nltk
import PyPDF2
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk import tokenize
from operator import itemgetter
import math

import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize 

nltk.download('punkt')

def preprocessing():

    doc = ""
    pdf = PyPDF2.PdfReader("2024-dbir-data-breach-investigations-report.pdf")
    for i in pdf.pages:
        doc += i.extract_text()

    stop_words = set(stopwords.words('english')) 



    # total_sentences = tokenize.sent_tokenize(doc)
    # total_sent_len = len(total_sentences)
    # print(total_sent_len)

    # import re
    # from nltk.corpus import stopwords
    # from nltk.stem.porter import PorterStemmer
    # from nltk.stem import WordNetLemmatizer
    # nltk.download('wordnet')


    ps = PorterStemmer()
    wordnet=WordNetLemmatizer()
    sentences = nltk.sent_tokenize(doc)
    corpus = []
    for i in range(len(sentences)):
        review = re.sub('[^a-zA-Z]', ' ', sentences[i])
        review = review.lower()
        review = review.split()
        review = [wordnet.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.append(review)

    # total_words = doc.split()
    # total_word_length = len(total_words)
    # print(total_word_length)

    corpus_str = " ".join(corpus)

    import pandas as pd
    df = pd.read_csv("niccs--cybersecurity-vocabulary--2024May23.csv")

    terms = df["Term"]

    list_voc = terms.tolist()
    list_voc = [wordnet.lemmatize(word) for word in list_voc]


    #tokenized_sents = [word_tokenize(i) for i in example]

    total_words = corpus_str.split()

    words_final = []
    for word in total_words:
        if word in list_voc:
            words_final.append(word)
    total_word_length = len(words_final)
    total_words = words_final

    total_word_length = len(total_words)

    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1
    # print(tf_score)

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())

    # print(tf_score)

    def check_sent(word, sentences): 
        final = [all([w in x for w in word]) for x in sentences] 
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))


    # Step 4: Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, sentences)
            else:
                idf_score[each_word] = 1
    total_sent_len = len(sentences)
    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    # print(idf_score)

    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()} 
    # print(tf_idf_score)

    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
        return result

    result = get_top_n(tf_idf_score,20)
    keywords = [result.keys()] 

    # print(get_top_n(tf_idf_score, 20))
    print(keywords)
    return keywords
preprocessing()
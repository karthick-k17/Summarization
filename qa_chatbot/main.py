from summarizer import summarize
from compound_to_simple import convertor
from validator import validate
from keywords import preprocessing

pdf_path = '../files/first_chapter.pdf'

prompt = 'Summarize the result to about 400 to 500 words.'

keywords = 'threat, secure, AI'

summary1 = summarize(pdf_path, prompt, keywords)

summary2 = convertor(pdf_path, prompt, keywords)

key_terms = preprocessing(pdf_path)

validate(summary1, summary2, key_terms)
import PyPDF2
import google.generativeai as genai
from dotenv import get_key
from langchain_text_splitters import RecursiveCharacterTextSplitter

def convertor(file_path, prompt, keywords):
    # file_name = file_path.name

    #Get API Key
    api_key = get_key('../.env', key_to_get='GEMINI_API_KEY')

    #Configure API key
    genai.configure(api_key=api_key)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000, 
        chunk_overlap=30,
        separators=['.','\n','\n\n']
    )

    pdf_file = PyPDF2.PdfReader(file_path)

    extracted_text = ""

    for i in pdf_file.pages:
        extracted_text += i.extract_text()

    #Defining model
    gen_config = genai.GenerationConfig(
        temperature=0.5,
    )

    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
    )

    print('Original text:')
    print(extracted_text)

    texts = text_splitter.split_text(extracted_text)

    converted_text = ""

    for text in texts:
        response = model.generate_content(
            f"""You are a cyber security expert and an expert summarizer. The audience is a general user who wants to know about cybersecurity. Convert the given paragraphs of text into simple sentences.
            Example:
            Input: Pure Extortion attacks have risen over the past year and are now a component of 9% of all breaches.
            Output: Pure Extortion attacks have risen over the past year . Pure Extortion attacks are now a component of 9% of all breaches.

            {text}"""
        )
        converted_text += response.text

    print('Processed text:')
    print(converted_text)
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=100000, 
        chunk_overlap=30,
        separators=['.','\n','\n\n']
    )

    texts = text_splitter.split_text(converted_text)

    summarized_content = ""

    for text in texts:
        response = model.generate_content(
            f"""You are a cyber security expert and an expert summarizer. {prompt}. Make sure to include the text that contains the following keywords:
            {keywords}
            {text}"""
        )
        summarized_content += response.text

    return summarized_content


if __name__ == '__main__':
    result = convertor('../files/first_chapter.pdf', 'Summarize the result to about 400 to 500 words.', 'threat, secure, AI')
    print('Summarized Result')
    print(result)
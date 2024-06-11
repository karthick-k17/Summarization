import PyPDF2
import google.generativeai as genai
import dotenv 
from langchain_text_splitters import RecursiveCharacterTextSplitter


def summarize(prompt, keywords, processed_text):

    summarized_content = ""
    #Get API Key
    api_key = dotenv.get_key('../.env', key_to_get='GEMINI_API_KEY')

    #Configure API key
    genai.configure(api_key=api_key)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000000, 
        chunk_overlap=30,
        separators=['.','\n','\n\n']
    )

    #Defining model
    gen_config = genai.GenerationConfig(
        temperature=0.5,
    )
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config=gen_config
    )

    # texts = text_splitter.split_text(extracted_text)
    texts = text_splitter.split_text(processed_text)
    for text in texts:
        response = model.generate_content(
            f"""You are a cyber security expert and an expert summarizer. {prompt}. Make sure to include the text that contains the following keywords:
            {keywords}
            {text}"""
        )
        summarized_content += response.text
        print(response.text)

    return summarized_content

import PyPDF2

import google.generativeai as genai

import dotenv 

from langchain_text_splitters import CharacterTextSplitter

def summarizer(file_path):

    file_name = file_path.split("/")[-1]

    summarized_content = ""
    #Get API Key
    api_key = dotenv.get_key('.env', key_to_get='GEMINI_API_KEY')

    #Configure API key
    genai.configure(api_key=api_key)

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000000, chunk_overlap=30
    )

    # pdf_file = PyPDF2.PdfReader('files/2024-dbir-data-breach-investigations-report.pdf')
    pdf_file = PyPDF2.PdfReader(file_path)

    with open(f"./tempDir/{file_name}", "wb") as f:
        f.write(file_name.getbuffer())

    extracted_text = ""

    for i in pdf_file.pages:
        extracted_text += i.extract_text()

    #Defining model
    gen_config = genai.GenerationConfig(
        temperature=0.5,
    )
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config=gen_config
    )

    prompt = input('Enter your prompt. Specify the level of Summarization required. ')
    keywords = input('Enter the keywords that needs to be searched while generating summary: (Use comma to separate the keywords)')

    #First use case
    # texts = text_splitter.split_text(extracted_text)
    # for text in texts:
    #     response = model.generate_content(
    #         f"""You are a cyber security expert and an expert summarizer. {prompt}
    #         {text}"""
    #     )
    #     summarized_content += response.text
    #     print(response.text)


    #Second use case
    texts = text_splitter.split_text(extracted_text)
    for text in texts:
        response = model.generate_content(
            f"""You are a cyber security expert and an expert summarizer. {prompt}. Make sure to include the text that contains the following keywords:
            {keywords}
            {text}"""
        )
        summarized_content += response.text
        print(response.text)

    return summarized_content 


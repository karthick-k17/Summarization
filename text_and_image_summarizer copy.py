from pdf2image import convert_from_path

import google.generativeai as genai

import dotenv 

from langchain_text_splitters import CharacterTextSplitter

#Get API Key
api_key = dotenv.get_key('.env', key_to_get='GEMINI_API_KEY')

#Configure API key
genai.configure(api_key=api_key)

pil_images = convert_from_path('files/2024-dbir-data-breach-investigations-report.pdf')

#Defining model
gen_config = genai.GenerationConfig(
    temperature=0.5,
)

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=1000000, chunk_overlap=30
)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    generation_config=gen_config
)

extracted_text = ""

for img in pil_images:
    extracted_text += model.generate_content([
        f"""You are a cyber security expert and an expert summarizer. Summarize the given information from the page. Extract insights from the figures and tables and use the adjacent text as context.""", img]
    ).text


# To Summarize once
# for img in pil_images:
#     extracted_text += model.generate_content([
#         f"""You are a cyber security expert and an expert summarizer. Extract the text from the page. Also extract insights from the figures and tables and use the adjacent text as context.""", img]
#     ).text


texts = text_splitter.split_text(extracted_text)
for text in texts:
    response = model.generate_content(
        f"""You are a cyber security expert and an expert summarizer. Summarize the given information 
        {text}"""
    )
    print(response.text)
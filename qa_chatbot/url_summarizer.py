import google.generativeai as genai
import dotenv 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader


def url_summarize(weburl, prompt, keywords):
    
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
    
    #loading data from url 
    loader = WebBaseLoader(f"{weburl}")
    loader.requests_kwargs = {'verify':False}
    temp = loader.load()
    data = str(temp)
    #Defining model
    gen_config = genai.GenerationConfig(
        temperature=0.5,
    )
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash-latest',
        generation_config=gen_config
    )

    texts = text_splitter.split_text(data)
    for text in texts:
        response = model.generate_content(
            f"""You are a cyber security expert and an expert summarizer. {prompt}. Make sure to include the text that contains the following keywords:
            {keywords}
            {text}"""
        )
        summarized_content += response.text
        print(response.text)

    return summarized_content

# def main():
#     weburl = "https://www.gov.uk/government/publications/research-on-the-cyber-security-of-ai/ai-cyber-security-survey-main-report"
#     prompt = " Summarize in bulletin points "
#     keywords = " "
#     url_summarize(weburl,prompt,keywords)

# main()

import google.generativeai as genai
import PIL
import dotenv

#Get API Key
api_key = dotenv.get_key('.env', key_to_get='GEMINI_API_KEY')

#Configure API key
genai.configure(api_key=api_key)

#Defining model
gen_config = genai.GenerationConfig(
    temperature=0.3,
    top_p=0.3,
    top_k=20
)
model = genai.GenerativeModel(
    model_name='gemini-pro-vision',
    generation_config=gen_config
)

img = PIL.Image.open('table_of_contents.png')
#Prompt

response = model.generate_content(["""Extract the page number range for each chapter. The page number range starts from the page number of the first heading till two pages before the starting page of the chapter.""", img])
print(response.text)
inter_res = response.text

response = model.generate_content([f"""Given the page number range for each chapter, include the chapter name and its page number range. Display it's subheadings under it along with the pages it covers:
                              {inter_res}""", img])
print(response.text)
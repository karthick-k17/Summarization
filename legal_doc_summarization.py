import google.generativeai as genai
from dotenv import get_key

api_key = get_key('.env', 'GEMINI_API_KEY')

genai.configure(api_key=api_key)

# gen_config = genai.GenerationConfig(
    
# )


model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest',
    system_instruction='You are a great legal advisor and can understand every legal document in existence.'
    # generation_config=gen_config
)

prompt = 'From the given US Bill, divide the law into three categories: Low, Medium and High. Under low category, include the rules that requires low priority. In medium cateogry, include rules that require medium priority and under high category, include rules, that requires high priority and has to followed under any circumstance'

with open('files/US Bill.txt', 'r', encoding='UTF-8') as f:
    text = f.read()

response = model.generate_content(f"Answer the user's query based on the given text. \nQuery: \n{prompt} \nLaw document: \n{text} ")

print(response.text)

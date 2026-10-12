from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say, hello to Talha in One Line",
)

print(response.text)
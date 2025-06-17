from google import genai

client = genai.Client(api_key="AIzaSyCUotj2f9EBg13RBWRl6ebqYfoCiHx5s4k")

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Hello, world!",
)
print(response.text)
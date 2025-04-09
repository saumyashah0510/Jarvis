from groq import Groq

# Initialize client
client = Groq(api_key="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") 
 
# Chat completion
response = client.chat.completions.create(
    model="llama3-70b-8192",  # Or "mixtral-8x7b-32768"
    messages=[
        {
            "role": "system",
            "content": "You are Jarvis, a helpful AI assistant like Alexa."
        },
        {
            "role": "user",
            "content": "What is coding?"
        }
    ],
    temperature=0.5  # Controls creativity (0-1)
)

# Print response
print(response.choices[0].message.content)
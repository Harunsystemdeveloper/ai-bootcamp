from anthropic import Anthropic  # hämta walkie-talkien
from dotenv import load_dotenv   # hämta nyckelläsaren

load_dotenv()          # öppna kassaskåpet
client = Anthropic()   # slå på walkie-talkien

# Skicka ett meddelande till Claude
response = client.messages.create(
    model="claude-haiku-5-5",   # vilken Claude-modell vi pratar med
    max_tokens=100,
    messages=[{"role": "user", "content": "Säg hej på svenska i en mening."}],
)

print(response.content[0].text)
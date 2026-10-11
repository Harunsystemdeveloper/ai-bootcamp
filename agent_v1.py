""" agent_v1.py AI-agent."""""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()
MODEL = "claude-haiku-5-5"

# ---------- DEL 1: Verktygen (anteckningsblocket) ----------
notes: list[str] = [] # en tom lista där anteckningarna hamnar

def add_note(text: str) -> str:
    notes.append(text)
    return f"Anteckning sparad (#{len(notes)})."

def list_notes() -> str:
    if not notes:
        return"Inga anteckningar ännu."
    return "\n".join(f"{i}. {n}" for i, n in enumerate(notes, start=1))

# ---------- DEL 2: Bruksanvisningen (det Claude får läsa) ----------
TOOLS = [
    {
        "name": "add_note",
        "description": "Spara en ny anteckning. Använd när användaren vill komma ihåg något.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Anteckningens innehåll."}
            },
            "required": ["text"],
        },
    },
    {
        "name": "list_notes",
        "description": "Lista alla sparade anteckningar. Använd när användaren frågar vad som finns sparat.",
        "input_schema": {"type": "object", "properties": {}},
    },
]

# Kopplar ihop namnet Claude säger med rätt Python-funktion
TOOL_FUNCTIONS = {"add_note": add_note, "list_notes": list_notes}

# ---------- DEL 3: Du som använder verktyget ----------
def run_tool(name: str, args: dict) -> str:
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        return f"Fel: okänt verktyg '{name}'."
    try:
        return func(**args)
    except Exception as e:
        return f"Fel när {name} kördes: {e}"

# ---------- DEL 4: Walkie-talkie-samtalet i en loop ----------
def run_agent(user_message: str, max_steps: int = 5) -> str:
    messages = [{"role": "user", "content": user_message}]

    for step in range(max_steps):
        # Skicka hela samtalet hittills till Claude
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        # Kom ihåg vad Claude sa
        messages.append({"role": "assistant", "content": response.content})

        # Vill Claude inte använda något verktyg? Då är den klar.
        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        # Annars: gör det Claude bad om
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"  🔧 Steg {step + 1}: {block.name}({block.input})")
                result = run_tool(block.name, block.input)
                print(f"     ↳ {result}")          
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

        # Säg "klart!" till Claude med resultatet
        messages.append({"role": "user", "content": tool_results})

    return "Stoppade: agenten tog för många steg."


if __name__ == "__main__":
    answer = run_agent(
        "Spara att jag ska köpa mjölk och att jag har möte kl 10 på måndag. "
        "Visa sedan alla mina anteckningar."
    )
    print("\n🤖", answer)
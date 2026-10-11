# AI-bootcamp 🤖

Ett strukturerat fördjupningsprogram där jag utvecklar min kompetens inom **AI-agenter** och **Model Context Protocol (MCP)**.

Som systemutvecklare med bakgrund inom .NET, molnet och AI vill jag förstå agentarkitektur på djupet: inte bara använda färdiga ramverk, utan förstå principerna bakom dem. Därför bygger jag varje del från grunden innan jag går vidare till ramverk som LangGraph.

## Mål

- Bygga en **production-grade MCP-server** med väl designade tools och resources
- Bygga agenter som använder MCP på ett genomtänkt sätt
- Designa och orkestrera **multi-agent-system** med human-in-the-loop

## Lektion 1–2: Agentloopen från grunden

En agentloop byggd direkt mot Anthropic API, **utan ramverk**, för att förstå exakt hur tool use fungerar.

Agenten hanterar anteckningar med tre verktyg:

| Verktyg | Beskrivning |
|---|---|
| `add_note` | Sparar en ny anteckning |
| `list_notes` | Listar alla anteckningar |
| `delete_note` | Tar bort en anteckning via nummer, med indatavalidering |

### Designprinciper jag tillämpat

- **Modellen ser bara kontraktet.** `name`, `description` och `input_schema` styr hur agenten använder verktyget, så tydliga beskrivningar är avgörande.
- **Fel returneras som text i stället för att krascha.** Agenten kan då läsa felet och anpassa sig.
- **Validera innan något ändras.** Ogiltig indata stoppas innan state påverkas.
- **Säkerhetsspärr i loopen.** `max_steps` förhindrar oändliga loopar och okontrollerade kostnader.

### Insikter till nästa steg

- Verktyg som utför en handling och *sedan* misslyckas kan ge dubbletter vid omförsök. Det är viktigt att tänka på för verktyg med sidoeffekter.
- Positionsbaserade nummer förskjuts efter borttagning. Stabila ID:n behövs, och det implementeras med SQLite i nästa projekt.

## Kom igång

```bash
python -m venv .venv
.venv\Scripts\activate
pip install anthropic python-dotenv
```

Skapa en `.env`-fil i projektroten:
```
ANTHROPIC_API_KEY=din-nyckel
```

Kör agenten:
```bash
python agent_v1.py
```

## Teknik

Python · Anthropic API (Claude) · Tool use

## Kommande

- [ ] MCP-grunder: server, tools, resources och prompts
- [ ] Projekt 1: MCP-server för anteckningar och tasks (SQLite)
- [ ] Projekt 2: Multi-agent-system med LangGraph
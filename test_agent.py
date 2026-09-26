import os

from dotenv import load_dotenv

from app.research_agent import ResearchAgent


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


agent = ResearchAgent(api_key)

topic = "Impact of Artificial Intelligence on Healthcare"


result = agent.run(topic)


print("\n\nFINAL RESEARCH REPORT")
print("=" * 60)

print(result["report"])

print("\n\nPIPELINE CHECK")
print("=" * 60)

print("Topic:", result["topic"])
print("Questions generated:", len(result["questions"].splitlines()))
print("Research questions searched:", len(result["research_data"]))
print("Research analyses completed:", len(result["analyses"]))
print("Report generated:", bool(result["report"]))
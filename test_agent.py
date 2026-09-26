import os

from dotenv import load_dotenv

from app.research_agent import ResearchAgent
from app.evaluation import evaluate_research_result, print_evaluation


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


# -----------------------------
# Evaluate Research Pipeline
# -----------------------------

evaluation = evaluate_research_result(result)

print_evaluation(evaluation)
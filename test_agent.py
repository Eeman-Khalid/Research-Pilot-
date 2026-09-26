import os
from dotenv import load_dotenv

from app.research_agent import ResearchAgent


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


agent = ResearchAgent(api_key)

topic = "Impact of Artificial Intelligence on Healthcare"


# Generate research questions
questions = agent.generate_research_questions(topic)

print("\nRESEARCH QUESTIONS")
print("=" * 60)
print(questions)


# Search the web for each question
research_data = agent.research_questions_to_searches(questions)

print("\n\nWEB RESEARCH RESULTS")
print("=" * 60)


for i, item in enumerate(research_data, 1):

    print(f"\nQUESTION {i}:")
    print(item["question"])

    print("\nSOURCES:")

    for j, source in enumerate(item["sources"], 1):

        print(f"\n{j}. {source['title']}")
        print(f"URL: {source['url']}")
        print(f"Snippet: {source['snippet']}")
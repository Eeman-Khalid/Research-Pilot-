import time

from ddgs import DDGS
from google import genai
from google.genai import errors


class ResearchAgent:

    def __init__(self, api_key, model="gemini-3.5-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    # -----------------------------
    # Gemini API Helper with Retry
    # -----------------------------
    def _generate_content(self, prompt, max_retries=3):

        for attempt in range(1, max_retries + 1):

            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                return response

            except errors.ServerError:

                print(
                    f"Gemini server error "
                    f"(attempt {attempt}/{max_retries})"
                )

                if attempt == max_retries:
                    raise

                wait_time = 5 * attempt

                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    # -----------------------------
    # 1. Generate Research Questions
    # -----------------------------
    def generate_research_questions(self, topic):

        prompt = f"""
You are a research planning agent.

Given the research topic below, generate 5 important research questions
that should be investigated to produce a high-quality research report.

Research Topic:
{topic}

Return only the 5 questions as a numbered list.
"""

        response = self._generate_content(prompt)

        return response.text

    # -----------------------------
    # 2. Web Search
    # -----------------------------
    def search_web(self, query, max_results=5):

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=max_results
            )

            for result in search_results:

                results.append({
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "snippet": result.get("body")
                })

        return results

    # -----------------------------
    # 3. Search Each Question
    # -----------------------------
    def research_questions_to_searches(self, questions):

        searches = []

        for question in questions.split("\n"):

            question = question.strip()

            if question and question[0].isdigit():

                question = question.split(".", 1)[-1].strip()

                results = self.search_web(
                    question,
                    max_results=3
                )

                searches.append({
                    "question": question,
                    "sources": results
                })

        return searches

    # -----------------------------
    # 4. Analyze Sources
    # -----------------------------
    def analyze_sources(self, question, sources):

        source_text = ""

        for i, source in enumerate(sources, 1):

            source_text += f"""
Source {i}

Title: {source['title']}
URL: {source['url']}
Snippet: {source['snippet']}
"""

        prompt = f"""
You are an AI research analyst.

Research Question:
{question}

Below are web search results related to this question:

{source_text}

Analyze these sources and provide:

1. The main findings
2. Important facts or claims
3. Areas where the sources agree
4. Areas where the sources differ or provide uncertainty

Do not invent information that is not supported by the provided sources.
Clearly mention when the available information is insufficient.
"""

        response = self._generate_content(prompt)

        return response.text

    # -----------------------------
    # 5. Analyze All Research
    # -----------------------------
    def analyze_all_research(self, research_data, max_retries=3):

        analyses = []

        for item in research_data:

            question = item["question"]

            for attempt in range(1, max_retries + 1):

                try:

                    print(f"\nAnalyzing: {question}")
                    print(f"Attempt {attempt}/{max_retries}")

                    analysis = self.analyze_sources(
                        question,
                        item["sources"]
                    )

                    analyses.append({
                        "question": question,
                        "analysis": analysis,
                        "sources": item["sources"]
                    })

                    print("✓ Completed")

                    break

                except Exception as e:

                    print(f"⚠ Attempt {attempt} failed: {e}")

                    if attempt < max_retries:

                        print("Retrying...")
                        time.sleep(5)

                    else:

                        print("✗ Failed after all retries")

            time.sleep(2)

        return analyses

    # -----------------------------
    # 6. Generate Final Report
    # -----------------------------
    def generate_report(self, topic, all_research):

        research_text = ""

        for i, item in enumerate(all_research, 1):

            research_text += f"""
Research Question {i}:
{item["question"]}

Analysis:
{item["analysis"]}

Sources:
"""

            for source in item["sources"]:

                research_text += (
                    f"- {source['title']} | {source['url']}\n"
                )

        prompt = f"""
You are a professional research report writer.

Research Topic:
{topic}

Below is research collected and analyzed from multiple web sources:

{research_text}

Create a clear, well-structured research report.

Use exactly these sections:

# Executive Summary

# Key Findings

# Detailed Analysis

# Conclusion

# References

Important rules:

- Base the report only on the provided research.
- Do not invent facts or sources.
- Keep the writing professional and objective.
- Include source URLs in the References section.
- Clearly distinguish findings from uncertainty.
"""

        response = self._generate_content(prompt)

        return response.text
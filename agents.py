import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from tools import web_search, scrape_url


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError(
        "MISTRAL_API_KEY not found. "
        "Please add MISTRAL_API_KEY to your .env file."
    )


# ============================================================
# MODEL SETUP
# ============================================================

llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0,
    api_key=MISTRAL_API_KEY
)


# ============================================================
# SEARCH AGENT
# ============================================================

def build_search_agent():

    return create_agent(
        model=llm,
        tools=[web_search]
    )


# ============================================================
# READER AGENT
# ============================================================

def build_reader_agent():

    return create_agent(
        model=llm,
        tools=[scrape_url]
    )


# ============================================================
# WRITER CHAIN
# ============================================================

writer_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are an expert research writer.

Your job is to transform gathered research into
a clear, structured, factual and professional
research report.

Do not invent sources or facts.
Use the research provided to you.
"""
    ),

    (
        "human",
        """
Write a detailed research report on the topic below.

Topic:
{topic}

Research Gathered:
{research}


Structure the report as:

1. Introduction

2. Key Findings
   - Finding 1
   - Finding 2
   - Finding 3
   - Add more findings when appropriate

3. Detailed Analysis

4. Conclusion

5. Sources
   - List all URLs found in the research


Requirements:

- Be factual and professional.
- Explain the important findings clearly.
- Do not invent URLs.
- Do not invent research results.
- Use the provided research as the primary source.
"""
    )

])


writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)


# ============================================================
# CRITIC CHAIN
# ============================================================

critic_prompt = ChatPromptTemplate.from_messages([

    (
        "system",
        """
You are a sharp and constructive research critic.

Your job is to evaluate research reports for:

- Accuracy
- Completeness
- Clarity
- Structure
- Quality of evidence
- Source coverage
- Professional writing

Be honest and specific.
"""
    ),

    (
        "human",
        """
Review the research report below.

Report:
{report}


Respond in exactly this format:


Score: X/10

Strengths:
- ...
- ...
- ...

Areas to Improve:
- ...
- ...
- ...

One line verdict:
...


Do not rewrite the entire report.
Focus on evaluating the report.
"""
    )

])


critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)

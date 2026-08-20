# 🔬 ResearchMind

### Multi-Agent AI Research & Report Generation System

ResearchMind is an Agentic AI system that automates the complete research workflow using specialized AI agents. It searches the web, extracts relevant information, generates a structured research report, and critically evaluates the final output.

## 🤖 Multi-Agent Architecture

- 🔎 **Search Agent** — Searches the web using Tavily.
- 📄 **Reader Agent** — Extracts relevant content using Requests and BeautifulSoup.
- ✍️ **Writer Agent** — Generates a structured report using Mistral AI.
- 🧐 **Critic Agent** — Reviews the report and provides a score and improvement suggestions.

## 🔄 Workflow

Research Topic → Search → Extract → Generate → Critique → Final Report

## 🛠️ Technologies Used

- Python
- LangChain
- Mistral AI
- Tavily API
- BeautifulSoup
- Requests
- Streamlit
- python-dotenv

## 🚀 How to Run

```bash
uv pip install -r requirements.txt
uv run streamlit run app.py


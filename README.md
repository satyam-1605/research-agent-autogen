# Virtual Research Assistant

A Streamlit-based web app that helps you find, summarize, and analyze research papers from ArXiv and Google Scholar using advanced AI agents.

## Features

- **Search Research Papers:** Enter a research topic and fetch top papers from ArXiv and Google Scholar.
- **Summarization:** Automatically generates concise summaries for each paper using an LLM agent.
- **Advantages & Disadvantages:** Analyzes each summary to provide pointwise pros and cons.
- **Async Processing:** Efficiently fetches and processes papers using asynchronous code.
- **Extensible Agents:** Modular agent design for summarization and analysis.

## Project Structure

```
autogen_agent/
├── app.py              # Streamlit app entry point
├── agents.py           # AI agent definitions for summarization and analysis
├── data_loader.py      # Fetches papers from ArXiv and Google Scholar
├── requirements.txt    # Python dependencies
```

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/satyam-1605/research-agent-autogen.git
   cd research-agent-autogen/autogen_agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Create a `.env` file in the project root.
   - Add your Groq/OpenAI API key:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

## Usage

1. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser:**  
   Go to `http://localhost:8501/`.

3. **Enter a research topic** and click "Search" to view summarized research papers and their advantages/disadvantages.

## File Descriptions

- **app.py:**  
  Main Streamlit UI. Handles user input, calls data loaders and agents, and displays results.

- **agents.py:**  
  Defines `ResearchAgents` class, which wraps LLM-based agents for summarization and analysis.

- **data_loader.py:**  
  Contains `DataLoader` class for fetching papers from ArXiv (async) and Google Scholar (sync).

- **requirements.txt:**  
  Lists all required Python packages.

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies.

## Notes

- You need a valid Groq/OpenAI API key for the LLM agents.
- The app uses the `scholarly` package for Google Scholar scraping, which may be subject to rate limits or changes by Google.
- The code is modular and can be extended with more agents or data sources.

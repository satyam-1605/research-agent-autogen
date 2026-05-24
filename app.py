
import streamlit as st
import os
import asyncio

from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

load_dotenv()

# Streamlit UI Title
st.title("📚 Virtual Research Assistant")

# Retrieve the API key from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")

# Check if API key is set, else stop execution
if not groq_api_key:
    st.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize AI Agents for summarization and analysis
agents = ResearchAgents(groq_api_key)

# Initialize DataLoader for fetching research papers
data_loader = DataLoader()

# Connect search agent (optional for topic expansion)
data_loader.search_agent = agents.summarizer_agent

# Input field for the user to enter a research topic
query = st.text_input("Enter a research topic:")

# When the user clicks "Search"
if st.button("Search"):

    with st.spinner("Fetching research papers..."):

        # CHANGED → async call
        arxiv_papers = asyncio.run(
            data_loader.fetch_arxiv_papers(query)
        )

        google_scholar_papers = data_loader.fetch_google_scholar_papers(query)
        # all_papers = arxiv_papers + google_scholar_papers

        # all_papers = arxiv_papers
        all_papers = (
    arxiv_papers[:2]
    +
    google_scholar_papers[:2]
)

        if not all_papers:
            st.error("Failed to fetch papers. Try again!")

        else:

            processed_papers = []

            for paper in all_papers:
                # CHANGED → async calls
                summary = asyncio.run(agents.summarize_paper(paper["summary"]))

                adv_dis = asyncio.run(agents.analyze_advantages_disadvantages(summary))

                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                })

            st.subheader("Top Research Papers:")
            for i, paper in enumerate(processed_papers, 1):
                st.markdown(f"### {i}. {paper['title']}")  # Paper title
                st.markdown(f"🔗 [Read Paper]({paper['link']})")  # Paper link
                st.write(f"**Summary:** {paper['summary']}")  # Paper summary
                st.write(f"{paper['advantages_disadvantages']}")  # Pros/cons analysis
                st.markdown("---")  # Separator between papers
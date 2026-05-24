
import requests
import xml.etree.ElementTree as ET
from scholarly import scholarly


class DataLoader:
    def __init__(self):
        self.search_agent = None

    async def fetch_arxiv_papers(self, query):
        """
            Fetches top 5 research papers from ArXiv based on the user query.
            If <5 papers are found, expands the search using related topics.

            Returns:
                list: A list of dictionaries containing paper details (title, summary, link).
        """

        def search_arxiv(query):
            """Helper function to query ArXiv API."""

            url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=5"

            response = requests.get(url)

            if response.status_code == 200:

                root = ET.fromstring(response.text)

                return [
                    {
                        "title": entry.find("{http://www.w3.org/2005/Atom}title").text,
                        "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text,
                        "link": entry.find("{http://www.w3.org/2005/Atom}id").text
                    }

                    for entry in root.findall("{http://www.w3.org/2005/Atom}entry")
                ]

            return []

        papers = search_arxiv(query)

        # CHANGED: generate_reply -> run
        if len(papers) < 5 and self.search_agent:

            related_topics_response = await self.search_agent.run(
                task=f"Suggest 3 related research topics for '{query}'"
            )

            related_topics = (
                related_topics_response.messages[-1]
                .content
                .split("\n")
            )

            for topic in related_topics:
                topic = topic.strip()
                if topic and len(papers) < 5:
                    new_papers = search_arxiv(topic)
                    papers.extend(new_papers)
                    papers = papers[:5]

        return papers

    def fetch_google_scholar_papers(self, query):
        """
            Fetches top 5 research papers from Google Scholar.
            Returns:
                list: A list of dictionaries containing paper details (title, summary, link)
        """
        papers = []
        try:
            search_results = scholarly.search_pubs(query)
            for i, paper in enumerate(search_results):
                if i >= 5:
                    break
                bib = paper.get("bib", {})
                title = bib.get("title", "").strip()
                abstract = (
                    bib.get("abstract")
                    or bib.get("pub_year")
                    or ""
                )
                if not title:
                    continue
                if not abstract:
                    continue
                papers.append({
                    "title": title,
                    "summary": str(abstract)[:3000],
                    "link": paper.get(
                        "pub_url",
                        "No link available"
                    )
                })
        except Exception as e:
            print("Scholar Error:", e)
        return papers
    
    

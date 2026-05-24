
import os
from dotenv import load_dotenv

# CHANGED IMPORTS
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
load_dotenv()


class ResearchAgents:
    def __init__(self, api_key):

        self.groq_api_key = api_key

        # CHANGED: old llm_config → model_client
        self.model_client = OpenAIChatCompletionClient(
        model="llama-3.3-70b-versatile",
        api_key=self.groq_api_key,
        base_url="https://api.groq.com/openai/v1",

    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": "unknown",
        "structured_output": False,
    }
)

        # Summarizer Agent
        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",
            system_message="Summarize the retrieved research papers and present concise summaries to the user, JUST GIVE THE RELEVANT SUMMARIES OF THE RESEARCH PAPER AND NOT YOUR THOUGHT PROCESS.",
            model_client=self.model_client
        )

        # Advantages and Disadvantages Agent
        self.advantages_disadvantages_agent = AssistantAgent(
            name="advantages_disadvantages_agent",
            system_message="Analyze the summaries of the research papers and provide a list of advantages and disadvantages for each paper in a pointwise format. JUST GIVE THE ADVANTAGES AND DISADVANTAGES, NOT YOUR THOUGHT PROCESS",
            model_client=self.model_client
        )

    # CHANGED: async + run()
    async def summarize_paper(self, paper_summary):

        summary_response = await self.summarizer_agent.run(
            task=f"Summarize this paper: {paper_summary}"
        )

        return summary_response.messages[-1].content

    # CHANGED: async + run()
    async def analyze_advantages_disadvantages(self, summary):

        adv_dis_response = await self.advantages_disadvantages_agent.run(
            task=f"Provide advantages and disadvantages for this paper: {summary}"
        )

        return adv_dis_response.messages[-1].content

    # NEW: close model client
    async def close(self):
        await self.model_client.close()
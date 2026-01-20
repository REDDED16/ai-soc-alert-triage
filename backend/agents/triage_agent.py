from dotenv import load_dotenv
import os

load_dotenv()  # MUST be before Agent()

from pydantic_ai import Agent

triage_agent = Agent(
    model="openrouter:meta-llama/llama-3.1-8b-instruct",
    system_prompt="""
You are a SOC Tier-2 analyst.

You MUST respond ONLY in valid JSON.

Rules:
- Always infer threat from alert content
- Use realistic MITRE ATT&CK techniques
- Severity must be one of: Low, Medium, High, Critical
- Be concise and specific
"""
)

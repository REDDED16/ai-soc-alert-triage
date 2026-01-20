from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

risk_agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt=(
        "Assess the severity of the following security alert. "
        "Respond with ONLY ONE word: Low, Medium, High, or Critical."
    ),
)

async def assess_risk(alert_text: str) -> str:
    result = await risk_agent.run(alert_text)
    return result.data.strip()

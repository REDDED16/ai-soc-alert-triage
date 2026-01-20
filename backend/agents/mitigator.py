from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

mitigation_agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt=(
        "You are a SOC analyst. "
        "Provide 3–5 concise mitigation steps for the given attack type. "
        "Respond as a bullet list."
    ),
)

async def suggest_mitigation(threat_type: str) -> list[str]:
    result = await mitigation_agent.run(threat_type)

    # Ensure list output
    if isinstance(result.data, list):
        return result.data

    # Fallback: split text into bullets
    return [
        step.strip("- ").strip()
        for step in result.data.split("\n")
        if step.strip()
    ]

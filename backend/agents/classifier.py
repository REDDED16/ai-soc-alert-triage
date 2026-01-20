from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

classifier_agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt=(
        "You are a senior SOC analyst. "
        "Classify the following security alert into ONE clear attack category. "
        "Choose ONLY from: "
        "Port Scanning, Brute Force, Phishing, Malware, Privilege Escalation, "
        "Data Exfiltration, Command and Control. "
        "Respond with ONLY the category name."
    ),
)

async def classify_alert(alert_text: str) -> str:
    result = await classifier_agent.run(alert_text)
    return result.data.strip()

from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

mitre_agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt=(
        "Map the given attack category to the MOST RELEVANT MITRE ATT&CK technique. "
        "Use the format: TXXXX - Technique Name. "
        "Examples:\n"
        "Port Scanning → T1046 - Network Service Scanning\n"
        "Brute Force → T1110 - Brute Force\n"
        "Phishing → T1566 - Phishing\n"
        "Malware → T1059 - Command and Scripting Interpreter\n"
        "Respond with ONLY the technique ID and name."
    ),
)

async def map_to_mitre(threat_type: str) -> str:
    result = await mitre_agent.run(threat_type)
    return result.data.strip()

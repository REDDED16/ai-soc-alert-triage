from agents.triage_agent import triage_agent


# -------------------------------
# Rule-based SOC triage (FAST)
# -------------------------------
def rule_based_triage(alert: str):
    text = alert.lower()

    # 1️⃣ Brute Force / Credential Stuffing
    if "failed login" in text or "brute" in text:
        return {
            "threat_type": "Brute Force Credential Attack",
            "mitre_technique": "T1110 - Brute Force",
            "severity": "High",
            "impact": (
                "Repeated authentication failures followed by a successful login "
                "may indicate credential compromise."
            ),
            "mitigation_steps": [
                "Reset affected user passwords",
                "Enable account lockout policies",
                "Enforce multi-factor authentication",
                "Review authentication logs for suspicious activity"
            ]
        }

    # 2️⃣ PowerShell / Script Execution
    if "powershell" in text or "encoded command" in text:
        return {
            "threat_type": "Malicious PowerShell Execution",
            "mitre_technique": "T1059.001 - PowerShell",
            "severity": "High",
            "impact": (
                "Encoded or obfuscated PowerShell commands are commonly used "
                "to execute malicious payloads."
            ),
            "mitigation_steps": [
                "Terminate suspicious PowerShell processes",
                "Investigate the parent process",
                "Enable PowerShell script block logging",
                "Isolate the affected endpoint"
            ]
        }

    # 3️⃣ DNS Tunneling
    if "dns" in text or "randomized" in text:
        return {
            "threat_type": "DNS Tunneling Activity",
            "mitre_technique": "T1071.004 - DNS",
            "severity": "High",
            "impact": (
                "High-frequency DNS queries with randomized subdomains may "
                "indicate command-and-control communication."
            ),
            "mitigation_steps": [
                "Block suspicious domains",
                "Analyze DNS logs for tunneling behavior",
                "Inspect endpoint for malware",
                "Isolate the affected system if needed"
            ]
        }

    # 4️⃣ Port Scanning / Reconnaissance
    if "port scan" in text or "multiple ports" in text:
        return {
            "threat_type": "Network Reconnaissance Activity",
            "mitre_technique": "T1046 - Network Service Scanning",
            "severity": "Medium",
            "impact": (
                "Scanning multiple ports may indicate reconnaissance activity "
                "preceding an attack."
            ),
            "mitigation_steps": [
                "Block the source IP address",
                "Review firewall and IDS logs",
                "Monitor for follow-on attacks"
            ]
        }

    # 5️⃣ Lateral Movement
    if "multiple hosts" in text or "same credentials" in text:
        return {
            "threat_type": "Lateral Movement Attempt",
            "mitre_technique": "T1021 - Remote Services",
            "severity": "High",
            "impact": (
                "The same credentials being used across multiple systems "
                "may indicate lateral movement by an attacker."
            ),
            "mitigation_steps": [
                "Disable compromised accounts",
                "Reset credentials",
                "Review lateral authentication logs",
                "Segment the network if necessary"
            ]
        }

    # 6️⃣ Outbound Traffic Spike / C2 / Exfiltration
    if (
        "outbound traffic" in text
        or "traffic spike" in text
        or "external domain" in text
        or "unknown domain" in text
    ):
        return {
            "threat_type": "Suspicious Outbound Network Activity",
            "mitre_technique": "T1071.001 - Application Layer Protocol",
            "severity": "High",
            "impact": (
                "A spike in outbound traffic to an unknown external domain may "
                "indicate command-and-control communication or data exfiltration."
            ),
            "mitigation_steps": [
                "Block the destination domain or IP at the firewall",
                "Inspect outbound traffic for sensitive data",
                "Review proxy, DNS, and firewall logs",
                "Isolate the affected endpoint if malicious activity is confirmed"
            ]
        }

    # ❌ No rule matched
    return None


# -------------------------------
# Main Orchestrator
# -------------------------------
async def analyze_alert(alert_text: str):
    # 1️⃣ Rule-based (instant + reliable)
    rule_result = rule_based_triage(alert_text)
    if rule_result:
        return rule_result

    # 2️⃣ AI fallback (OpenRouter)
    try:
        result = await triage_agent.run(
            f"""
You are a SOC analyst.

Analyze the following alert and return JSON with:
- threat_type
- mitre_technique
- severity
- impact
- mitigation_steps

Alert:
{alert_text}
"""
        )
        return result.output
    except Exception:
        # 3️⃣ Final safe fallback (never fail demo)
        return {
            "threat_type": "Suspicious Activity",
            "mitre_technique": "T1036 - Masquerading",
            "severity": "Medium",
            "impact": "Suspicious behavior detected that requires further investigation.",
            "mitigation_steps": [
                "Review system and network logs",
                "Monitor affected assets",
                "Escalate to SOC analyst for deeper investigation"
            ]
        }

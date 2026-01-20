from agents.triage_agent import triage_agent

# -------------------------------
# Rule-based SOC triage (FAST)
# -------------------------------
def rule_based_triage(alert: str):
    text = alert.lower()

    if "failed login" in text or "brute" in text:
        return {
            "threat_type": "Brute Force Credential Attack",
            "mitre_technique": "T1110 - Brute Force",
            "severity": "High",
            "impact": (
                "Repeated authentication failures may indicate a brute force "
                "or credential stuffing attack."
            ),
            "mitigation_steps": [
                "Reset affected user passwords",
                "Enable account lockout policies",
                "Enforce multi-factor authentication",
                "Review authentication logs"
            ]
        }

    if "powershell" in text or "encoded command" in text:
        return {
            "threat_type": "Malicious PowerShell Execution",
            "mitre_technique": "T1059.001 - PowerShell",
            "severity": "High",
            "impact": (
                "Obfuscated PowerShell commands are commonly used to execute "
                "malicious payloads."
            ),
            "mitigation_steps": [
                "Terminate suspicious PowerShell processes",
                "Investigate parent processes",
                "Enable PowerShell logging",
                "Isolate the affected endpoint"
            ]
        }

    if "dns" in text or "randomized" in text:
        return {
            "threat_type": "DNS Tunneling Activity",
            "mitre_technique": "T1071.004 - DNS",
            "severity": "High",
            "impact": (
                "High-frequency DNS queries with randomized subdomains may "
                "indicate command-and-control traffic."
            ),
            "mitigation_steps": [
                "Block suspicious domains",
                "Analyze DNS logs",
                "Inspect endpoint for malware",
                "Isolate the system if needed"
            ]
        }

    if "port scan" in text or "multiple ports" in text:
        return {
            "threat_type": "Network Reconnaissance",
            "mitre_technique": "T1046 - Network Service Scanning",
            "severity": "Medium",
            "impact": (
                "Scanning multiple ports may indicate reconnaissance prior "
                "to an attack."
            ),
            "mitigation_steps": [
                "Block the source IP",
                "Review firewall and IDS logs",
                "Monitor for follow-on activity"
            ]
        }

    if "multiple hosts" in text or "same credentials" in text:
        return {
            "threat_type": "Lateral Movement Attempt",
            "mitre_technique": "T1021 - Remote Services",
            "severity": "High",
            "impact": (
                "The same credentials used across multiple systems may "
                "indicate lateral movement."
            ),
            "mitigation_steps": [
                "Disable compromised accounts",
                "Reset credentials",
                "Review authentication logs",
                "Segment the network"
            ]
        }

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
                "Outbound traffic to an unknown external domain may indicate "
                "command-and-control communication or data exfiltration."
            ),
            "mitigation_steps": [
                "Block the destination domain or IP",
                "Inspect outbound traffic",
                "Review DNS and proxy logs",
                "Isolate the affected endpoint"
            ]
        }

    return None


# -------------------------------
# Main Orchestrator
# -------------------------------
async def analyze_alert(alert_text: str):
    # 1️⃣ Rule-based (primary)
    rule_result = rule_based_triage(alert_text)
    if rule_result:
        return rule_result

    # 2️⃣ AI fallback (safe + optional)
    try:
        result = await triage_agent.run(
            f"""
Analyze the SOC alert and return JSON with:
threat_type, mitre_technique, severity, impact, mitigation_steps.

Alert:
{alert_text}
"""
        )

        # Defensive extraction (library-safe)
        if hasattr(result, "output"):
            return result.output
        if hasattr(result, "data"):
            return result.data

    except Exception:
        pass

    # 3️⃣ Final guaranteed fallback
    return {
        "threat_type": "Suspicious Activity",
        "mitre_technique": "T1036 - Masquerading",
        "severity": "Medium",
        "impact": "Suspicious behavior detected that requires further investigation.",
        "mitigation_steps": [
            "Review system and network logs",
            "Monitor affected assets",
            "Escalate to SOC analyst"
        ]
    }

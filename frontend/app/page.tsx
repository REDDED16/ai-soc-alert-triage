"use client";

import { useState } from "react";

type AnalysisResult = {
  threat_type: string;
  mitre_technique: string;
  severity: string;
  impact: string;
  mitigation_steps: string[];
};

export default function Home() {
  const [alertText, setAlertText] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);

  // ✅ HARD-CODED BACKEND URL (IMPORTANT)
  const API_URL =
    "https://ai-soc-alert-triage-production.up.railway.app";

  const analyzeAlert = async () => {
    if (!alertText.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          alert_text: alertText,
        }),
      });

      if (!res.ok) {
        throw new Error("API request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("API error:", err);
      alert("Backend request failed. Check console.");
    } finally {
      setLoading(false);
    }
  };

  const severityColor = (sev: string) => {
    if (sev === "High") return "bg-red-600";
    if (sev === "Medium") return "bg-yellow-500";
    return "bg-green-600";
  };

  const samples = [
    "Multiple failed SSH login attempts detected from a single IP",
    "Suspicious PowerShell execution with encoded command",
    "Outbound traffic spike to an unknown external domain detected",
  ];

  return (
    <div className="min-h-screen bg-black text-white px-8 py-10">
      <div className="max-w-4xl mx-auto space-y-8">

        {/* Header */}
        <div className="flex justify-between items-center">
          <h1 className="text-3xl font-bold">AI SOC Alert Triage</h1>
          <span className="px-3 py-1 rounded-full bg-green-700 text-sm">
            System Online
          </span>
        </div>

        {/* Input */}
        <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
          <textarea
            rows={4}
            value={alertText}
            onChange={(e) => setAlertText(e.target.value)}
            placeholder="Paste SOC alert here…"
            className="w-full bg-black border border-zinc-700 rounded-md p-4"
          />

          <div className="flex gap-2 flex-wrap">
            {samples.map((s, i) => (
              <button
                key={i}
                onClick={() => setAlertText(s)}
                className="px-3 py-1 text-sm bg-zinc-700 rounded hover:bg-zinc-600"
              >
                Sample {i + 1}
              </button>
            ))}
          </div>

          <button
            onClick={analyzeAlert}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 rounded hover:bg-blue-500 disabled:opacity-50"
          >
            {loading ? "Analyzing…" : "Analyze Alert"}
          </button>
        </div>

        {/* Loading */}
        {loading && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 animate-pulse">
            <div className="h-3 bg-zinc-700 w-2/3 mb-2" />
            <div className="h-3 bg-zinc-700 w-1/2" />
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Threat Analysis</h2>
              <span
                className={`px-3 py-1 rounded text-sm ${severityColor(
                  result.severity
                )}`}
              >
                {result.severity}
              </span>
            </div>

            <p><b>Threat Type:</b> {result.threat_type}</p>
            <p><b>MITRE ATT&CK:</b> {result.mitre_technique}</p>
            <p><b>Impact:</b> {result.impact}</p>

            <div>
              <p className="font-semibold">Mitigation Steps:</p>
              <ul className="list-disc list-inside">
                {result.mitigation_steps.map((m, i) => (
                  <li key={i}>{m}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

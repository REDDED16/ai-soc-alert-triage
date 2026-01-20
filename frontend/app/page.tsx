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
  const [showResult, setShowResult] = useState(false);
  const [history, setHistory] = useState<
    { input: string; output: AnalysisResult }[]
  >([]);

  const analyzeAlert = async () => {
    if (!alertText.trim()) return;

    setLoading(true);
    setResult(null);
    setShowResult(false);

    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ alert_text: alertText }),
      });

      const data = await res.json();

      // ⏳ Intentional delay for smooth UX
      setTimeout(() => {
        setResult(data);
        setShowResult(true);
        setHistory((prev) => [{ input: alertText, output: data }, ...prev]);
        setLoading(false);
      }, 600);
    } catch {
      setLoading(false);
    }
  };

  const severityColor = (sev: string) => {
    if (sev === "Critical") return "bg-red-600";
    if (sev === "High") return "bg-orange-500";
    if (sev === "Medium") return "bg-yellow-500";
    return "bg-green-600";
  };

  const samples = [
    "Multiple failed login attempts followed by a successful login from a new IP address",
    "Suspicious PowerShell execution detected with encoded command",
    "Outbound traffic spike to an unknown external domain detected",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-black to-zinc-900 text-white px-8 py-10">
      <div className="max-w-5xl mx-auto space-y-10">

        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold">AI SOC Alert Triage</h1>
            <p className="text-zinc-400 mt-1">
              Automated Tier-1 Security Analysis
            </p>
          </div>
          <span className="px-4 py-1 text-sm rounded-full bg-green-700">
            System Online
          </span>
        </div>

        {/* Input */}
        <div className="bg-zinc-900/70 backdrop-blur border border-zinc-800 rounded-xl p-6 space-y-4">
          <textarea
            rows={4}
            value={alertText}
            onChange={(e) => setAlertText(e.target.value)}
            placeholder="Paste SOC alert, SIEM log, or EDR finding here…"
            className="w-full bg-black border border-zinc-700 rounded-md p-4 focus:outline-none"
          />

          <div className="flex flex-wrap gap-2">
            {samples.map((s, i) => (
              <button
                key={i}
                onClick={() => setAlertText(s)}
                className="text-sm px-3 py-1 rounded-full bg-zinc-700 hover:bg-zinc-600"
              >
                Sample {i + 1}
              </button>
            ))}
          </div>

          <button
            onClick={analyzeAlert}
            disabled={loading}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded-md disabled:opacity-50 transition"
          >
            {loading ? "Analyzing…" : "Analyze Alert"}
          </button>
        </div>

        {/* Loading Skeleton */}
        {loading && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4 animate-pulse">
            <p className="text-sm text-zinc-400">Analyzing alert…</p>
            <div className="h-3 bg-zinc-700 rounded w-2/3" />
            <div className="h-3 bg-zinc-700 rounded w-1/2" />
            <div className="h-3 bg-zinc-700 rounded w-1/3" />
          </div>
        )}

        {/* Result */}
        {result && showResult && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 space-y-4 transition-all duration-500 ease-out animate-fade-in">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-semibold">Threat Analysis</h2>
              <span
                className={`px-3 py-1 rounded-full text-sm ${severityColor(
                  result.severity
                )}`}
              >
                {result.severity}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-zinc-400">Threat Type</p>
                <p className="font-medium">{result.threat_type}</p>
              </div>
              <div>
                <p className="text-zinc-400">MITRE ATT&CK</p>
                <p className="font-medium">{result.mitre_technique}</p>
              </div>
            </div>

            <div>
              <p className="text-zinc-400">Impact</p>
              <p>{result.impact}</p>
            </div>

            <div>
              <p className="text-zinc-400">Mitigation Steps</p>
              <ul className="list-disc list-inside mt-2 space-y-1">
                {result.mitigation_steps.map((step, i) => (
                  <li key={i}>{step}</li>
                ))}
              </ul>
            </div>
          </div>
        )}

        {/* History */}
        {history.length > 0 && (
          <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">Analysis History</h2>
            <div className="space-y-3">
              {history.map((h, i) => (
                <div
                  key={i}
                  className="border border-zinc-700 rounded-md p-4 text-sm"
                >
                  <p className="text-zinc-400">Alert</p>
                  <p className="mb-2">{h.input}</p>
                  <span
                    className={`inline-block px-2 py-1 text-xs rounded ${severityColor(
                      h.output.severity
                    )}`}
                  >
                    {h.output.severity}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export async function analyzeAlert(alertText: string) {
  const response = await fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ alert_text: alertText }),
  });

  if (!response.ok) {
    throw new Error("Failed to analyze alert");
  }

  return response.json();
}

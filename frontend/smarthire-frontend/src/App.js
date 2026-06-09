import { useState } from "react";

const API = "https://kit-colin-reductions-organisation.trycloudflare.com";
function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState("python,fastapi,react,html,css,javascript,java,sql,spring,aws,kubernetes");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const screenResume = async () => {
    if (!file) return alert("Resume file select cheyyi!");
    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("required_skills", skills);
    const res = await fetch(`${API}/screen`, {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: 600, margin: "40px auto", fontFamily: "Arial", padding: 20 }}>
      <h1 style={{ color: "#2563eb" }}>SmartHire AI</h1>
      <p style={{ color: "#666" }}>Intelligent Resume Screening System</p>

      <div style={{ background: "#f8fafc", padding: 20, borderRadius: 8, marginTop: 20 }}>
        <h3>Upload Resume</h3>
        <input
          type="file"
          accept=".txt,.pdf"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginBottom: 16, display: "block" }}
        />
        <label>Required Skills (comma separated):</label>
        <input
          type="text"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          style={{ width: "100%", padding: 8, marginTop: 8, marginBottom: 16, borderRadius: 4, border: "1px solid #ddd" }}
        />
        <button
          onClick={screenResume}
          style={{ background: "#2563eb", color: "white", padding: "10px 24px", border: "none", borderRadius: 6, cursor: "pointer", fontSize: 16 }}
        >
          {loading ? "Screening..." : "Screen Resume"}
        </button>
      </div>

      {result && (
        <div style={{ background: "#f0fdf4", padding: 20, borderRadius: 8, marginTop: 20, border: "1px solid #86efac" }}>
          <h3>Results for: {result.filename}</h3>
          <p style={{ fontSize: 32, fontWeight: "bold", color: "#16a34a" }}>{result.score}%</p>
          <p><strong>Recommendation:</strong> {result.recommendation}</p>
          <p><strong>Found Skills:</strong> {result.found_skills.join(", ") || "None"}</p>
          <p><strong>Missing Skills:</strong> {result.missing_skills.join(", ") || "None"}</p>
        </div>
      )}
    </div>
  );
}

export default App;

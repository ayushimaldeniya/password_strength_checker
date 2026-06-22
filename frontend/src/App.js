import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import shieldImg from './images/shield.png';
import lockImg from './images/lock.png';
import userImg from './images/user.png';
import chartImg from './images/chart.png';
import AIBrainImg from './images/brain.png';
import keyImg from './images/key.png';
import safeImg from './images/safe.png';
import warningImg from './images/warning.png';
import warning2Img from './images/warning2.png';

function App() {
  const [password, setPassword] = useState('');
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!password) return;

    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await axios.post('http://localhost:8000/api/analyze', {
        password: password
      });
      setAnalysis(response.data);
    } catch (err) {
      console.error(err);
      setError("Failed to establish a network handshake with the AI Defense Backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="security-dashboard">
      <header className="dashboard-header">
        <h1><img src={shieldImg} className="icon-img" alt="Shield" /> Smart Password Security Center</h1>
        <p>An intelligent system using AI and encryption to keep accounts safe.</p>
      </header>

      {/* TOP ROW: MAIN WORKSPACE GRID */}
      <div className="main-grid">
        
        {/* CARD 1: TESTER PANEL */}
        <div className="defense-card shadow-glow">
          <h2><img src={lockImg} className="icon-img" alt="Lock" /> Test Your Password Strength</h2>
          <form onSubmit={handleAnalyze}>
            <div className="input-group">
              <input
                type="text"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Type a password here to test..."
                autoComplete="off"
              />
            </div>
            <button type="submit" disabled={loading || !password}>
              {loading ? "Checking Pattern..." : "Check Password Safety"}
            </button>
          </form>

          {error && <div className="network-error-alert">{error}</div>}
        </div>

        {/* CARD 2: ANALYSIS RESULTS AREA */}
        {analysis ? (
          <div className="defense-card metrics-card animate-fade">
            <h2><img src={chartImg} className="icon-img" alt="Chart" /> Security Analysis Results</h2>
            
            <div className="risk-badge-container">
              <span className={`risk-badge ${analysis.summary.overall_risk_assessment.replace(' ', '-')}`} style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                {analysis.summary.overall_risk_assessment === 'LOW RISK' && (
                  <img src={safeImg} className="icon-img" alt="Safe" />
                )}
                {analysis.summary.overall_risk_assessment === 'HIGH RISK' && (
                  <img src={warningImg} className="icon-img" alt="Alert" />
                )}
                <span>{analysis.summary.overall_risk_assessment}</span>
              </span>
            </div>

            <div className="metric-row">
              <strong>Company Password Rules:</strong> 
              <span className={analysis.summary.policy_compliant ? "text-success" : "text-danger"}>
                {analysis.summary.policy_compliant ? "PASSED" : "FAILED"}
              </span>
            </div>

            {/* COMPLIANCE NOTES */}
            {analysis.rule_analysis.vulnerability_notes.length > 0 && (
              <div className="vulnerability-box">
                <h4><img src={warning2Img} className="icon-img" alt="Warning" /> Why it failed our rules:</h4>
                <ul>
                  {analysis.rule_analysis.vulnerability_notes.map((note, idx) => {
                    let simpleNote = note;
                    if (note.includes("minimal length")) simpleNote = "Must be at least 8 characters long.";
                    if (note.includes("case diversification")) simpleNote = "Should mix uppercase and lowercase letters.";
                    if (note.includes("numerical complexity")) simpleNote = "Should include at least one number (0-9).";
                    if (note.includes("special character")) simpleNote = "Should include a symbol (like !, @, #, $).";
                    if (note.includes("structural redundancy")) simpleNote = "Too many repeating characters (like 'aaaa').";
                    return <li key={idx}>{simpleNote}</li>;
                  })}
                </ul>
              </div>
            )}

            <hr />

            <h3><img src={AIBrainImg} className="icon-img" alt="AIBrain" /> AI Pattern Scan</h3>
            <div className="metric-row">
              <strong>AI Safety Verdict:</strong> 
              <span className={analysis.ai_analysis.pattern_verdict === 'secure' ? "text-success" : "text-danger"}>
                {analysis.ai_analysis.pattern_verdict === 'secure' ? "SAFE PATTERN" : "UNSAFE PATTERN"}
              </span>
            </div>
            <div className="metric-row">
              <strong>AI Model Confidence:</strong> 
              <span>{analysis.ai_analysis.confidence_score}%</span>
            </div>

            {/* CRYPTOGRAPHIC DETAILS */}
            {analysis.cryptographic_payload && (
              <div className="cryptographic-box">
                <h4><img src={keyImg} className="icon-img" alt="Key" /> Secure Database Encryption Payload</h4>
                <div className="crypto-snippet">
                  <strong>Method:</strong> <span>{analysis.cryptographic_payload.hashing_algorithm}</span>
                </div>
                <div className="crypto-snippet text-truncate">
                  <strong>Your Unique Salt:</strong> <code>{analysis.cryptographic_payload.salt_token}</code>
                </div>
                <div className="crypto-snippet text-truncate">
                  <strong>Final Encrypted Hash:</strong> <code>{analysis.cryptographic_payload.generated_hash}</code>
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Placeholder card shown before running a test to keep grid clean */
          <div className="defense-card shadow-glow" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#8b949e', borderStyle: 'dashed' }}>
            <p style={{ textAlign: 'center' }}><img src={chartImg} className="icon-img" alt="" style={{opacity: 0.5}} /> Enter a password to display the security matrix logs here.</p>
          </div>
        )}

      </div>

      {/* BOTTOM ROW: IDENTITY VAULT REGISTRATION */}
      <div className="defense-card shadow-glow" style={{ marginTop: '30px' }}>
        <h2><img src={userImg} className="icon-img" alt="User" /> Create Secure Identity Vault</h2>
        <form onSubmit={async (e) => {
          e.preventDefault();
          const uname = e.target.username.value;
          const pword = e.target.password.value;
          
          try {
            const res = await axios.post('http://localhost:8000/api/register', {
              username: uname, password: pword
            });
            alert(res.data.message);
            if(res.data.success) e.target.reset();
          } catch (err) {
            alert("Database link offline.");
          }
        }}>
          <div className="input-group" style={{ display: 'flex', gap: '15px' }}>
            <input type="text" name="username" placeholder="Enter desired username..." required autoComplete="off" style={{ flex: 1 }} />
            <input type="password" name="password" placeholder="Enter high-defense password..." required style={{ flex: 1 }} />
          </div>
          <button type="submit" style={{ backgroundColor: '#1f6feb', marginTop: '15px', width: '100%' }}>Commit Account to Database</button>
        </form>
      </div>

    </div>
  );
}

export default App;
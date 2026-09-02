import { useState } from "react";
import "./App.css";


function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const askQuestion = async () => {
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query: query,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response from the backend.");
      }

      const data = await response.json();

      setAnswer(data.answer);
      setSources(data.sources);
    } catch (error) {
      console.error(error);

      setError(
        "Unable to connect to the FastAPI backend. Please make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="container">

        <h1>AWS Documentation Assistant</h1>

        <p className="description">
          Ask questions about AWS documentation.
        </p>

        <div className="question-section">

          <textarea
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Ask a question about AWS..."
            rows="4"
          />

          <button
            onClick={askQuestion}
            disabled={loading}
          >
            {loading ? "Searching..." : "Ask"}
          </button>

        </div>

        {error && (
          <div className="error">
            {error}
          </div>
        )}

        {answer && (
          <div className="result">

            <h2>Answer</h2>

            <p>{answer}</p>

            <h2>Sources</h2>

            <ul>
              {sources.map((source, index) => (
                <li key={index}>
                  {source}
                </li>
              ))}
            </ul>

          </div>
        )}

      </div>
    </div>
  );
}

export default App;
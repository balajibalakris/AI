  import { useState } from 'react';
  import axios from 'axios';
  import './App.css';
  

  function App() {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
      e.preventDefault();
      setLoading(true);
      setResponse('');
      try {
        const res = await axios.post('http://localhost:8000/query', {
          question: query
        });
        setResponse(res.data.result);
      } catch (err) {
        setResponse('❌ Error connecting to backend.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    return (
      <div className="app-container">
        <h1> 〈/〉Migration AI Assistant 💡</h1>
        <form onSubmit={handleSubmit}>
          <textarea
            rows="6"
            placeholder="Describe your error or migration issue..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Thinking...' : 'Find Solutions'}
          </button>
        </form>
        {response && (
          <div className="response">
            <strong>💡 Solutions:</strong>
            <pre>{response}</pre>
          </div>
        )}
      </div>
    );
  }

  export default App;

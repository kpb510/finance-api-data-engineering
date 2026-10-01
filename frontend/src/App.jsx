import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function App() {
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState(null);
  const [priceData, setPriceData] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/tickers')
      .then(response => {
        if (!response.ok) throw new Error(`Server responded with ${response.status}`);
        return response.json();
      })
      .then(data => setTickers(data.tickers))
      .catch(err => setError(err.message));
  }, []);

  useEffect(() => {
    if (!selectedTicker) return;

    fetch(`http://localhost:8000/api/tickers/${selectedTicker}/analytics`)
      .then(response => {
        if (!response.ok) throw new Error(`Server responded with ${response.status}`);
        return response.json();
      })
      .then(data => setPriceData(data))
      .catch(err => setError(err.message));
  }, [selectedTicker]);

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <h1>Stock Dashboard</h1>

      <select onChange={(e) => setSelectedTicker(e.target.value)} defaultValue="">
        <option value="" disabled>Select a ticker</option>
        {tickers.map(ticker => (
          <option key={ticker} value={ticker}>{ticker}</option>
        ))}
      </select>

      {selectedTicker && priceData.length > 0 && (
        <div style={{ marginTop: '2rem', width: '100%', height: 400 }}>
          <h2>{selectedTicker} — Close Price & 7-Day Moving Average</h2>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={priceData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis domain={['auto', 'auto']} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="close" stroke="#2563eb" dot={false} />
              <Line type="monotone" dataKey="moving_avg_7d" stroke="#dc2626" dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}

export default App;
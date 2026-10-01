import { useState, useEffect } from 'react';

function App() {
  const [tickers, setTickers] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState(null);
  const [priceData, setPriceData] = useState([]);
  const [error, setError] = useState(null);

  // Fetch the list of available tickers once, when the component first loads
  useEffect(() => {
    fetch('http://localhost:8000/api/tickers')
      .then(response => {
        if (!response.ok) throw new Error(`Server responded with ${response.status}`);
        return response.json();
      })
      .then(data => setTickers(data.tickers))
      .catch(err => setError(err.message));
  }, []);

  // Fetch price data whenever the selected ticker changes
  useEffect(() => {
    if (!selectedTicker) return;

    fetch(`http://localhost:8000/api/tickers/${selectedTicker}`)
    .then(response => {
      if (!response.ok) throw new Error(`Server responded with ${response.status}`);
      return response.json();
    })
    .then(data => setPriceData(data))
    .catch(err => setError(err.message));
  }, [selectedTicker]);

  if (error) {
    return <div>Error: {error}</div>
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

      {selectedTicker && (
        <div style={{ marginTop: '1rem' }}>
          <h2>{selectedTicker}</h2>
          <p>{priceData.length} rows loaded</p>
          <pre>{JSON.stringify(priceData.slice(0, 3), null, 2)}</pre>
        </div>
      )}
    </div>  
  );
}

export default App; 
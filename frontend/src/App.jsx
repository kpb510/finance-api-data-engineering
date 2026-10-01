import { useState, useEffect } from 'react';
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell
} from 'recharts';

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

  // Shared tooltip formatter: rounds values and labels them clearly
  const priceTooltipFormatter = (value, name) => {
    if (value === null) return ['N/A', name];
    const rounded = Number(value).toFixed(2);
    const label = name === 'close' ? 'Close ($)' : '7-Day Moving Avg ($)';
    return [`$${rounded}`, label];
  };

  const pctTooltipFormatter = (value) => {
    if (value === null) return ['N/A', 'Daily Change'];
    return [`${Number(value).toFixed(2)}%`, 'Daily Change'];
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: 900, margin: '0 auto' }}>
      <h1>Stock Dashboard</h1>

      <select onChange={(e) => setSelectedTicker(e.target.value)} defaultValue="">
        <option value="" disabled>Select a ticker</option>
        {tickers.map(ticker => (
          <option key={ticker} value={ticker}>{ticker}</option>
        ))}
      </select>

      {selectedTicker && priceData.length > 0 && (
        <>
          <div style={{ marginTop: '2rem' }}>
            <h2>{selectedTicker} — Close Price & 7-Day Moving Average</h2>
            <p style={{ color: '#555', fontSize: '0.9rem', maxWidth: 650 }}>
              The blue line shows the daily closing price. The red line smooths that
              out into a 7-day moving average, which filters out day-to-day noise so
              the underlying trend is easier to see. The moving average only starts
              after 7 days of data are available.
            </p>
            <div style={{ width: '100%', height: 400 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={priceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={['auto', 'auto']} />
                  <Tooltip formatter={priceTooltipFormatter} />
                  <Legend formatter={(value) =>
                    value === 'close' ? 'Close Price' : '7-Day Moving Avg'
                  } />
                  <Line type="monotone" dataKey="close" stroke="#2563eb" dot={false} />
                  <Line type="monotone" dataKey="moving_avg_7d" stroke="#dc2626" dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div style={{ marginTop: '3rem' }}>
            <h2>{selectedTicker} — Daily % Change</h2>
            <p style={{ color: '#555', fontSize: '0.9rem', maxWidth: 650 }}>
              Each bar shows the percentage change in closing price from the previous
              day. Green bars mean the price rose that day; red bars mean it fell.
            </p>
            <div style={{ width: '100%', height: 250 }}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={priceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={['auto', 'auto']} />
                  <Tooltip formatter={pctTooltipFormatter} />
                  <Bar dataKey="daily_pct_change">
                    {priceData.map((entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={entry.daily_pct_change >= 0 ? '#16a34a' : '#dc2626'}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default App;
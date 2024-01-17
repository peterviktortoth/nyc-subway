import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [transitData, setTransitData] = useState([]);

  const fetchData = () => {
    fetch('/refresh')
      .then(response => response.json())
      .then(data => {
        setTransitData(data);
      })
      .catch(error => console.error('Error:', error));
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 60000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      <h1>Lexington Ave - 59th St</h1>
      <div id="data-container">
        {transitData.map((item, index) => {
          const parts = item.message.split(' ');
          const trainLine = parts[1]; // Assuming the train line is always the second word
          const modifiedMessage = (
            <>
              {parts[0]} <span className="train-line-indicator">{trainLine}</span> {parts.slice(2).join(' ')}
            </>
          );

          return <p key={index}>{modifiedMessage}</p>;
        })}
      </div>
    </div>
  );
}

export default App;

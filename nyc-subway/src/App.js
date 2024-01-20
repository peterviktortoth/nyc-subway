import React, { useState, useEffect } from 'react';
import './App.css';
import TransitDataItem from './transitDataItem'


function App() {
  const [transitData, setTransitData] = useState([]);
  const [directionFilter, setDirectionFilter] = useState('all');

  const handleDirectionChange = (event) => {
    setDirectionFilter(event.target.value);
  };


  const fetchData = () => {
    fetch('/refresh')
      .then(response => response.json())
      .then(data => {
        console.log(data);
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
    <div>
      <header className="header">
        <h2>Lexington Avenue - 59th Street</h2>
        {/* Any additional header content */}
      </header>
      <div className="tabs-container">
        <div className="tabs">
          {/* Tab radio buttons and labels */}
          <input type="radio" id="radio-1" name="tab" value="all" checked={directionFilter === 'all'} onChange={handleDirectionChange} />
          <label htmlFor="radio-1" className="tab">All</label>
  
          <input type="radio" id="radio-2" name="tab" value="uptown" checked={directionFilter === 'uptown'} onChange={handleDirectionChange} />
          <label htmlFor="radio-2" className="tab">Uptown</label>
  
          <input type="radio" id="radio-3" name="tab" value="downtown" checked={directionFilter === 'downtown'} onChange={handleDirectionChange} />
          <label htmlFor="radio-3" className="tab">Downtown</label>
          <div className="glider"></div>
        </div>
      </div>
      <div className="data-container">
        {transitData
          .filter(item => 
            (directionFilter === 'all' || item.message.toLowerCase().includes(directionFilter.toLowerCase())) &&
            item.minutes_until_arrival >= 0
          )
          .map((item, index) => (
            <TransitDataItem key={index} item={item} /> // Corrected component usage
          ))
        }
      </div>
    </div>
  );
}

export default App;

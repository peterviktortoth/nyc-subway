import React, { useState, useEffect } from 'react';
import './App.css';
import TransitDataItem from './transitDataItem'
import SettingsModal from './SettingsModal';


function App() {
  const [transitData, setTransitData] = useState([]);
  const [directionFilter, setDirectionFilter] = useState('all');

  const handleDirectionChange = (event) => {
    setDirectionFilter(event.target.value);
  };

  const [showModal, setShowModal] = useState(false); // State to control modal visibility
  const [walkTime, setWalkTime] = useState(0); // Add this state



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
        <h1>Lexington Avenue - 59th Street</h1>
        <button className="settings-button" onClick={() => setShowModal(true)}>⚙️</button>
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
            item.minutes_until_arrival > walkTime
          )
          .map((item, index) => (
            <TransitDataItem key={index} item={item} /> // Corrected component usage
          ))
        }
      </div>
      {showModal && <SettingsModal walkTime={walkTime} setWalkTime={setWalkTime} closeModal={() => setShowModal(false)} />}
    </div>
  );
}

export default App;

import React from 'react';

function SettingsModal({ walkTime, setWalkTime, closeModal }) {

  const incrementWalkTime = () => {
    setWalkTime(prevWalkTime => prevWalkTime + 1);
  };

  const decrementWalkTime = () => {
    setWalkTime(prevWalkTime => Math.max(0, prevWalkTime - 1));
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <span className="close-button" onClick={closeModal}>&times;</span>
        <h2>Set Walk Time to Station</h2>
        <div className="walk-time-settings">
          <button onClick={decrementWalkTime}>-</button>
          <span>{walkTime} minutes</span>
          <button onClick={incrementWalkTime}>+</button>
        </div>
      </div>
    </div>
  );
}

export default SettingsModal;

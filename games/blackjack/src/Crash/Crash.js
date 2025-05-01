// src/Crash/Crash.js
import React, { useState, useEffect, useRef } from 'react';
import BetForm from '../components/BetForm';
import './crash.css';

export default function Crash({ balance, onBet, showModal }) {
  const [bet, setBet] = useState(null);
  const [multiplier, setMultiplier] = useState(1.0);
  const [crashed, setCrashed] = useState(false);
  const [cashedOut, setCashedOut] = useState(false);
  const intervalRef = useRef(null);

  // start a new round
  const start = amt => {
    onBet(amt);
    setBet(amt);
    setMultiplier(1.0);
    setCrashed(false);
    setCashedOut(false);
  };

  // grow multiplier by +0.01 every 50ms, with a 6% chance to crash each step
  useEffect(() => {
    if (bet == null) return;
    intervalRef.current = setInterval(() => {
      setMultiplier(prev => {
        const next = parseFloat((prev + 0.01).toFixed(2));
        return next;
      });
      if (Math.random() < 0.06) {
        clearInterval(intervalRef.current);
        setCrashed(true);
      }
    }, 50);

    return () => clearInterval(intervalRef.current);
  }, [bet]);

  // cash out before crash
  const cashOut = () => {
    if (crashed || cashedOut) return;
    clearInterval(intervalRef.current);
    setCashedOut(true);
    const payout = Math.ceil(bet * multiplier);
    onBet(-payout);
    showModal(`Cashed out at ×${multiplier.toFixed(2)} for $${payout}`);
  };

  // reset for replay
  const reset = () => {
    clearInterval(intervalRef.current);
    setBet(null);
    setMultiplier(1.0);
    setCrashed(false);
    setCashedOut(false);
  };

  return (
    <div className="crash-container">
      <h2 className="crash-title">Crash</h2>

      {!bet ? (
        <BetForm balance={balance} onBet={start} showModal={showModal} />
      ) : (
        <div className="crash-game">
          <div className={`crash-display ${crashed ? 'crashed' : ''}`}>
            {multiplier.toFixed(2)}×
          </div>

          {(!crashed && !cashedOut) ? (
            <button
              className="crash-cashout"
              onClick={cashOut}
            >
              Cash Out
            </button>
          ) : (
            <button
              className="crash-replay"
              onClick={reset}
            >
              Replay
            </button>
          )}
        </div>
      )}
    </div>
  );
}

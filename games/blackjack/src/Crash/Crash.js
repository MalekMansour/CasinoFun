import React, { useState, useEffect, useRef } from 'react';
import BetForm from '../components/BetForm';
import './crash.css';

export default function Crash({ balance, onBet, showModal }) {
  const [bet, setBet] = useState(null);
  const [multiplier, setMultiplier] = useState(0);
  const [crashAt, setCrashAt] = useState(null);
  const [crashed, setCrashed] = useState(false);
  const [cashedOut, setCashedOut] = useState(false);
  const intervalRef = useRef(null);

  // start round
  const start = amt => {
    onBet(amt);
    setBet(amt);
    setMultiplier(0);
    setCrashed(false);
    setCashedOut(false);
    // pick a crash point between 1× and 5000×
    setCrashAt(Math.random() * (5000 - 1) + 1);
  };

  // drive multiplier upward until crash
  useEffect(() => {
    if (bet == null) return;
    intervalRef.current = setInterval(() => {
      setMultiplier(prev => {
        const next = prev === 0 ? 1.0 : parseFloat((prev + 0.1).toFixed(1));
        if (next >= crashAt) {
          clearInterval(intervalRef.current);
          setCrashed(true);
        }
        return next;
      });
    }, 200);
    return () => clearInterval(intervalRef.current);
  }, [bet, crashAt]);

  // cash out early
  const cashOut = () => {
    if (crashed || cashedOut) return;
    clearInterval(intervalRef.current);
    setCashedOut(true);
    const payout = Math.ceil(bet * multiplier);
    onBet(-payout);
    showModal(`Cashed out at ×${multiplier.toFixed(1)} for $${payout}`);
  };

  // reset for next round
  const reset = () => {
    clearInterval(intervalRef.current);
    setBet(null);
    setMultiplier(0);
    setCrashAt(null);
    setCrashed(false);
    setCashedOut(false);
  };

  return (
    <div className="crash-container">
      {!bet ? (
        <BetForm balance={balance} onBet={start} showModal={showModal} />
      ) : (
        <div className="crash-game">
          <div className={`crash-display ${crashed ? 'crashed' : ''}`}>
            {multiplier.toFixed(1)}×
          </div>
          {crashed ? (
            <button className="crash-reset" onClick={reset}>
              Play Again
            </button>
          ) : (
            <button
              className="crash-cashout"
              onClick={cashOut}
              disabled={cashedOut}
            >
              Cash Out
            </button>
          )}
        </div>
      )}
    </div>
  );
}

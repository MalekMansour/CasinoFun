import React, { useState, useEffect, useRef } from 'react';
import BetForm from '../components/BetForm';
import './crash.css';

export default function Crash({ balance, onBet, showModal }) {
  const [bet, setBet] = useState(null);
  const [multiplier, setMultiplier] = useState(1.0);
  const [crashed, setCrashed] = useState(false);
  const [crashPoint, setCrashPoint] = useState(null);
  const [cashedOut, setCashedOut] = useState(false);
  const intervalRef = useRef(null);

  const start = amt => {
    onBet(amt);
    setBet(amt);
    setMultiplier(1.0);
    setCrashed(false);
    setCrashPoint(null);
    setCashedOut(false);
  };

  useEffect(() => {
    if (bet == null) return;

    intervalRef.current = setInterval(() => {
      setMultiplier(prev => {
        let crashChance;
        if (prev < 1.20)         crashChance = 0.02;    // 2%
        else if (prev < 2.00)    crashChance = 0.005;   // 0.5%
        else if (prev < 4.00)    crashChance = 0.002;   // 0.2%
        else if (prev < 10.0)    crashChance = 0.0008;  // 0.08%
        else if (prev < 50.0)    crashChance = 0.0002;  // 0.02%
        else                     crashChance = 0.00005;// 0.005%

        // crash?
        if (Math.random() < crashChance) {
          clearInterval(intervalRef.current);
          setCrashed(true);
          setCrashPoint(prev);
          return prev; 
        }

        return parseFloat((prev + 0.01).toFixed(2));
      });
    }, 50);

    return () => clearInterval(intervalRef.current);
  }, [bet]);

  const cashOut = () => {
    if (crashed || cashedOut) return;
    clearInterval(intervalRef.current);
    setCashedOut(true);
    const payout = Math.ceil(bet * multiplier);
    onBet(-payout);
    showModal(`Cashed out at ×${multiplier.toFixed(2)} for $${payout}`);
  };

  const reset = () => {
    clearInterval(intervalRef.current);
    setBet(null);
    setMultiplier(1.0);
    setCrashed(false);
    setCrashPoint(null);
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
            {crashed
              ? `CRASHED at ×${crashPoint.toFixed(2)}`
              : `${multiplier.toFixed(2)}×`}
          </div>

          {!crashed && !cashedOut ? (
            <button className="crash-cashout" onClick={cashOut}>
              Cash Out
            </button>
          ) : (
            <button className="crash-replay" onClick={reset}>
              Replay
            </button>
          )}
        </div>
      )}
    </div>
  );
}

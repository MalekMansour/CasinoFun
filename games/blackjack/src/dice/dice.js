import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './dice.css';

export default function DiceGame({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [pick, setPick] = useState(2);
  const [roll, setRoll] = useState(null);
  const [multiplier, setMultiplier] = useState(null);

  const handleBet = amt => {
    setBetAmount(amt);
    setRoll(null);
    setMultiplier(null);
    onBet(amt); // deduct stake

    // simulate dice roll
    setTimeout(() => {
      const d1 = Math.ceil(Math.random() * 6);
      const d2 = Math.ceil(Math.random() * 6);
      const sum = d1 + d2;
      setRoll(sum);

      const margin = sum - pick;
      const mult = margin < 0 ? 0 : margin + 2;  // 0 if under, =2 when exact, higher for bigger margin
      setMultiplier(mult);
      onBet(-(amt * mult)); // credit winnings immediately
    }, 500);
  };

  const reset = () => {
    setBetAmount(null);
    setRoll(null);
    setMultiplier(null);
  };

  return (
    <div className="dice-container">
      {!betAmount ? (
        <>
          <div className="dice-pick">
            <label>Pick a number:</label>
            <select
              value={pick}
              onChange={e => setPick(+e.target.value)}
            >
              {Array.from({ length: 11 }, (_, i) => i + 2).map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
          <BetForm balance={balance} onBet={handleBet} showModal={showModal} />
        </>
      ) : roll == null ? (
        <p className="dice-rolling">Rolling the dice…</p>
      ) : (
        <div className="dice-result">
          <p>Dice sum: <strong>{roll}</strong></p>
          {multiplier > 0
            ? <p>You win ×{multiplier}!</p>
            : <p>You lost your bet.</p>
          }
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

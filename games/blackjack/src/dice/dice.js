import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import {
  FaDiceOne,
  FaDiceTwo,
  FaDiceThree,
  FaDiceFour,
  FaDiceFive,
  FaDiceSix
} from 'react-icons/fa';
import './dice.css';

export default function DiceGame({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [pick, setPick] = useState(2);
  const [roll, setRoll] = useState(null);       
  const [multiplier, setMultiplier] = useState(null);

  function getDiceIcon(n) {
    switch (n) {
      case 1: return <FaDiceOne />;
      case 2: return <FaDiceTwo />;
      case 3: return <FaDiceThree />;
      case 4: return <FaDiceFour />;
      case 5: return <FaDiceFive />;
      case 6: return <FaDiceSix />;
      default: return null;
    }
  }

  const handleBet = amt => {
    setBetAmount(amt);
    setRoll(null);
    setMultiplier(null);
    onBet(amt); // deduct stake immediately

    setTimeout(() => {
      const d1 = Math.ceil(Math.random() * 6);
      const d2 = Math.ceil(Math.random() * 6);
      const sum = d1 + d2;
      setRoll({ d1, d2, sum });

      const diff = Math.abs(sum - pick);
      let mult;
      if (diff === 0) {
        mult = 2;         // exact match
      } else if (diff === 1) {
        mult = 1;         // within 1
      } else if (diff === 2) {
        mult = 0.5;       // within 2
      } else if (diff === 3) {
        mult = 0.2;       // within 3
      } else {
        mult = 0;         // 4 or more away
      }

      setMultiplier(mult.toFixed(2));
      if (mult > 0) {
        const winnings = Math.ceil(amt * mult);
        onBet(-winnings);  // credit payout
      }
    }, 500);
  };

  const reset = () => {
    setBetAmount(null);
    setRoll(null);
    setMultiplier(null);
  };

  return (
    <div className="dice-container">
            <h2 className="dice-title">Dice</h2>

      {!betAmount ? (
        <>
          <div className="dice-pick">
            <label>Pick a number:</label>
            <select value={pick} onChange={e => setPick(+e.target.value)}>
              {Array.from({ length: 11 }, (_, i) => i + 2).map(n => (
                <option key={n} value={n}>{n}</option>
              ))}
            </select>
          </div>
          <BetForm balance={balance} onBet={handleBet} showModal={showModal} />
        </>
      ) : !roll ? (
        <p className="dice-rolling">Rolling the dice…</p>
      ) : (
        <div className="dice-result">
          <div className="dice-icons">
            {getDiceIcon(roll.d1)}
            {getDiceIcon(roll.d2)}
          </div>
          <p>Sum: <strong>{roll.sum}</strong></p>
          <p>Your multiplier: <strong>×{multiplier}</strong></p>
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

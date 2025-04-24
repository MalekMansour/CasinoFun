import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './Plinko.css';

export default function Plinko({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [resultMultiplier, setResultMultiplier] = useState(null);

  // when BetForm calls onBet, we capture the bet and start the drop
  const handleBet = amt => {
    setBetAmount(amt);
    onBet(amt);
    // TODO: trigger ball-drop animation & random multiplier
    const multipliers = [0.2, 0.5, 1, 2, 3, 5, 10];
    const weights =   [  5,   5, 20, 20, 15, 15, 20]; // adjust odds
    // simple weighted pick:
    let total = weights.reduce((a,b)=>a+b,0);
    let r = Math.random() * total;
    let acc = 0;
    let pick;
    for (let i=0; i<weights.length; i++) {
      acc += weights[i];
      if (r <= acc) { pick = multipliers[i]; break; }
    }
    setTimeout(() => setResultMultiplier(pick), 1500);  // simulate drop delay
  };

  const reset = () => {
    setBetAmount(null);
    setResultMultiplier(null);
  };

  return (
    <div className="plinko-container">
      {!betAmount ? (
        <BetForm balance={balance} onBet={handleBet} showModal={showModal} />
      ) : resultMultiplier == null ? (
        <div className="plinko-board">
          {/* TODO: your pegs + animated ball */}
          <p>Dropping the ball…</p>
        </div>
      ) : (
        <div className="plinko-result">
          <p>You landed on <strong>x{resultMultiplier}</strong>!</p>
          <button onClick={() => {
            onBet(betAmount * resultMultiplier * -1); // credit winnings
            reset();
          }}>Collect</button>
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './HeadsAndTails.css';

export default function HeadsAndTails({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [choice, setChoice] = useState('heads');
  const [result, setResult] = useState(null); 
  const [winChance, setWinChance] = useState(0.5);

  const handleFlip = amt => {
    if (!choice) return showModal('Please select Heads or Tails.');
    setBetAmount(amt);
    setResult(null);
    onBet(amt);

    setTimeout(() => {
      const won = Math.random() < winChance;
      if (won) {
        setResult('win');
        onBet(-(amt * 2));              
        setWinChance(c => Math.max(0, c - 0.02)); 
      } else {
        setResult('lose');
        setWinChance(c => Math.min(1, c + 0.02)); 
      }
    }, 500);
  };

  const reset = () => {
    setBetAmount(null);
    setResult(null);
  };

  return (
    <div className="ht-container">
            <h2 className="headsandtails-title">Heads Or Tails</h2>

      <div className="choice-container">
        <label>
          <input
            type="radio"
            value="heads"
            checked={choice==='heads'}
            onChange={() => setChoice('heads')}
          /> Heads
        </label>
        <label>
          <input
            type="radio"
            value="tails"
            checked={choice==='tails'}
            onChange={() => setChoice('tails')}
          /> Tails
        </label>
      </div>

      {/* Bet form */}
      {!betAmount && (
        <BetForm
          balance={balance}
          onBet={handleFlip}
          showModal={showModal}
        />
      )}

      {/* Flipping indicator */}
      {betAmount && result === null && (
        <p className="flip-msg">
          Flipping the coin… (Win chance: {Math.round(winChance*100)}%)
        </p>
      )}

      {/* Result & Play Again */}
      {result && (
        <div className="result-container">
          <p>
            You {result === 'win' ? 'won' : 'lost'}! The coin showed{' '}
            <strong>
              {result === 'win' ? choice : (choice === 'heads' ? 'tails' : 'heads')}
            </strong>.
          </p>
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

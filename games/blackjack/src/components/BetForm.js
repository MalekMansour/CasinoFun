import React, { useState } from 'react';

export default function BetForm({ balance, onBet, showModal }) {
    const [amt, setAmt] = useState('');
    const place = () => {
      const b = parseInt(amt, 10);
      if (!b || b <= 0) return showModal('Enter a valid bet.');
      if (b > balance) return showModal('Bet exceeds balance.');
      onBet(b);
      setAmt('');
    };
    return (
      <div className="bet-form">
        <input
          type="number"
          placeholder="Bet"
          value={amt}
          onChange={e => setAmt(e.target.value)}
          min="1"
          max={balance}
          className="bet-input"
        />
        <button className="btn-deal" onClick={place}>Deal</button>
      </div>
    );
  }
  
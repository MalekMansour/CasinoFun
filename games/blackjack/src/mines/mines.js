// src/mines/mines.js
import React, { useState, useMemo } from 'react';
import BetForm from '../components/BetForm';
import './mines.css';

function comb(n, k) {
  if (k < 0 || k > n) return 0;
  k = Math.min(k, n - k);
  let res = 1;
  for (let i = 1; i <= k; i++) {
    res = res * (n - k + i) / i;
  }
  return res;
}

export default function Mines({ balance, onBet, showModal }) {
  const [bet, setBet] = useState(0);
  const [mines, setMines] = useState(3);
  const [mineSet, setMineSet] = useState(new Set());
  const [revealedSet, setRevealedSet] = useState(new Set());
  const [detonated, setDetonated] = useState(null);

  const startGame = amt => {
    setBet(amt);
    onBet(amt); // deduct stake
    const m = new Set();
    while (m.size < mines) {
      m.add(Math.floor(Math.random() * 25));
    }
    setMineSet(m);
    setRevealedSet(new Set());
    setDetonated(null);
  };

  const handleClick = idx => {
    if (detonated !== null || revealedSet.has(idx) || bet === 0) return;
    if (mineSet.has(idx)) {
      setDetonated(idx);
      showModal('💥 BOOM! You hit a mine and lost your bet.');
    } else {
      setRevealedSet(s => new Set(s).add(idx));
    }
  };

  const safeCount = 25 - mines;
  const revealedCount = revealedSet.size;

  const multiplier = useMemo(() => {
    const k = revealedCount;
    if (k === 0) return 1.0;
    return comb(25, k) / comb(safeCount, k);
  }, [revealedCount, safeCount]);

  const cashOut = () => {
    const win = Math.ceil(bet * multiplier);
    onBet(-win);
    showModal(`Cashed out ×${multiplier.toFixed(2)} for $${win}!`);
    reset();
  };

  const reset = () => {
    setBet(0);
    setMineSet(new Set());
    setRevealedSet(new Set());
    setDetonated(null);
  };

  return (
    <div className="mines-container">
      <div className="mines-controls">
        <label>
          Mines:
          <select
            value={mines}
            onChange={e => setMines(+e.target.value)}
            disabled={bet > 0 && detonated === null}
          >
            {Array.from({ length: 24 }, (_, i) => i + 1).map(n => (
              <option key={n} value={n}>{n}</option>
            ))}
          </select>
        </label>
      </div>

      <BetForm
        balance={balance}
        onBet={startGame}
        showModal={showModal}
        disabled={bet > 0 && detonated === null}
      />

      <div className="mines-grid">
        {Array.from({ length: 25 }).map((_, idx) => {
          let cls = 'cell hidden';
          let label = '';
          if (detonated === idx) {
            cls = 'cell detonated';
            label = '💣';
          } else if (revealedSet.has(idx)) {
            cls = 'cell safe';
            label = '💎';
          }
          return (
            <button
              key={idx}
              className={cls}
              onClick={() => handleClick(idx)}
            >
              {label}
            </button>
          );
        })}
      </div>

      {bet > 0 && (
        <>
          <div className="mines-info">
            <p>Revealed: {revealedCount}</p>
            <p>Multiplier: ×{multiplier.toFixed(2)}</p>
          </div>
          <div className="mines-actions">
            {!detonated && <button onClick={cashOut}>Cash Out</button>}
            <button onClick={reset}>Reset</button>
          </div>
        </>
      )}
    </div>
  );
}

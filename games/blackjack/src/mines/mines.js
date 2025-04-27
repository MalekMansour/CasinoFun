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
  const [bet, setBet] = useState(null);
  const [mines, setMines] = useState(3);
  const [grid, setGrid] = useState([]); // will be array of 25 items: 'hidden' | 'safe' | 'mine'
  const [revealedCount, setRevealedCount] = useState(0);
  const [gameOver, setGameOver] = useState(false);

  // initialize grid when bet placed
  const startGame = amt => {
    setBet(amt);
    onBet(amt); // deduct stake
    // build an array of length 25 with 'mine' x m and 'hidden' else
    const cells = Array(25).fill('hidden');
    // randomly place mines
    let placed = 0;
    while (placed < mines) {
      const idx = Math.floor(Math.random() * 25);
      if (cells[idx] !== 'mine') {
        cells[idx] = 'mine';
        placed++;
      }
    }
    setGrid(cells);
    setRevealedCount(0);
    setGameOver(false);
  };

  const handleClick = idx => {
    if (gameOver || grid[idx] !== 'hidden') return;
    const newGrid = [...grid];
    if (grid[idx] === 'mine') {
      newGrid[idx] = 'mine';
      setGrid(newGrid);
      setGameOver(true);
      showModal('💥 Boom! You hit a mine and lost your bet.');
    } else {
      newGrid[idx] = 'safe';
      setGrid(newGrid);
      setRevealedCount(c => c + 1);
    }
  };

  const safeCells = 25 - mines;
  const payoutMult = useMemo(() => {
    const k = revealedCount;
    if (k === 0) return 1.0;
    // fair multiplier = C(25, k) / C(safeCells, k)
    return comb(25, k) / comb(safeCells, k);
  }, [revealedCount, safeCells]);

  const cashOut = () => {
    const winnings = Math.ceil(bet * payoutMult);
    onBet(-winnings);
    showModal(`You cashed out ×${payoutMult.toFixed(2)} and won $${winnings}!`);
    reset();
  };

  const reset = () => {
    setBet(null);
    setGrid([]);
    setRevealedCount(0);
    setGameOver(false);
  };

  return (
    <div className="mines-container">
      {!bet ? (
        <>
          <div className="mines-controls">
            <label>
              Mines:
              <select value={mines} onChange={e => setMines(+e.target.value)}>
                {Array.from({length:24},(_,i)=>i+1).map(n=>(
                  <option key={n} value={n}>{n}</option>
                ))}
              </select>
            </label>
          </div>
          <BetForm balance={balance} onBet={startGame} showModal={showModal} />
        </>
      ) : (
        <>
          <div className="mines-grid">
            {grid.map((cell, idx) => (
              <button
                key={idx}
                className={`cell ${cell}`}
                onClick={() => handleClick(idx)}
              >
                {cell === 'safe' && '💎'}
                {cell === 'mine' && (gameOver ? '💣' : '')}
              </button>
            ))}
          </div>
          <div className="mines-info">
            <p>Revealed: {revealedCount}</p>
            <p>Multiplier: ×{payoutMult.toFixed(2)}</p>
          </div>
          <div className="mines-actions">
            {!gameOver && (
              <button onClick={cashOut}>Cash Out</button>
            )}
            <button onClick={reset}>Reset</button>
          </div>
        </>
      )}
    </div>
  );
}

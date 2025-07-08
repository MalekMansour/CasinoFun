import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './plinko.css';

export default function Plinko({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [resultMultiplier, setResultMultiplier] = useState(null);
  const [ballPos, setBallPos] = useState({ left: 50, top: 0 });

  const multipliers = [10,5,2,1,0.5,0.2,0.5,1,2,5,10];
  const weights     = [1,1.5,2.5,10,15,40,15,10,2.5,1.5,1];
  const binCount    = multipliers.length;
  const binWidthPct = 100 / binCount;
  const rows        = binCount - 1;
  const rowSpacing  = 100 / (rows + 1);
  const stepDur     = 150; 

  const handleBet = amt => {
    setBetAmount(amt);
    setResultMultiplier(null);
    setBallPos({ left: 50, top: 0 });
    onBet(amt); 

    const totalW = weights.reduce((a,b)=>a+b, 0);
    let r = Math.random() * totalW, acc = 0, pickIdx = 0;
    for (let i = 0; i < weights.length; i++) {
      acc += weights[i];
      if (r <= acc) { pickIdx = i; break; }
    }
    const pick = multipliers[pickIdx];
    const finalX = pickIdx * binWidthPct + binWidthPct / 2;

    const path = [];
    for (let i = 0; i < rows; i++) {
      const t = (i + 1) / (rows + 1);
      let x = 50 + (finalX - 50) * t;
      x += (Math.random() * binWidthPct / 4 - binWidthPct / 8);
      x = Math.min(Math.max(x, 0), 100);
      path.push({ left: x, top: (i + 1) * rowSpacing });
    }
    path.push({ left: finalX, top: 100 });

    path.forEach((pos, i) => {
      setTimeout(() => setBallPos(pos), (i + 1) * stepDur);
    });

    setTimeout(() => {
      setResultMultiplier(pick);
      onBet(-(amt * pick)); 
    }, (path.length + 1) * stepDur);
  };

  const reset = () => {
    setBetAmount(null);
    setResultMultiplier(null);
    setBallPos({ left: 50, top: 0 });
  };

  return (
    <div className="plinko-container">
            <h2 className="plinko-title">Plinko</h2>

      <div className="plinko-board">
        {multipliers.map((m, i) => (
          <div
            key={i}
            className="bin"
            style={{ left: `${i * binWidthPct}%`, width: `${binWidthPct}%` }}
          >
            <span className="bin-label">{m}×</span>
          </div>
        ))}

        {Array.from({ length: rows }).flatMap((_, ri) => {
          const offset = ri % 2 === 0 ? binWidthPct / 2 : 0;
          return Array.from({ length: binCount - 1 }).map((__, pj) => {
            const left = offset + pj * binWidthPct;
            const top = (ri + 1) * rowSpacing;
            return (
              <div
                key={`${ri}-${pj}`}
                className="peg"
                style={{ left: `${left}%`, top: `${top}%` }}
              />
            );
          });
        })}

        {betAmount != null && (
          <div
            className="ball"
            style={{ left: `${ballPos.left}%`, top: `${ballPos.top}%` }}
          />
        )}
      </div>

      {betAmount == null && (
        <BetForm balance={balance} onBet={handleBet} showModal={showModal} />
      )}

      {betAmount != null && resultMultiplier == null && (
        <p className="plinko-dropping">Dropping the ball…</p>
      )}

      {resultMultiplier != null && (
        <div className="plinko-result">
          <p>You landed on <strong>{resultMultiplier}×</strong>!</p>
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './plinko.css';

export default function Plinko({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [resultMultiplier, setResultMultiplier] = useState(null);
  const [ballPos, setBallPos] = useState({ left: 50, top: 0 });

  const multipliers = [0.2, 0.5, 1, 2, 3, 5, 10];
  const binCount = multipliers.length;
  const binWidthPct = 100 / binCount;
  const rows = binCount - 1;
  const rowSpacingPct = 100 / (rows + 1);
  const stepDuration = 300; 

  const handleBet = amt => {
    setBetAmount(amt);
    setResultMultiplier(null);
    setBallPos({ left: 50, top: 0 });
    onBet(amt);

    // pick a multiplier by weight
    const weights = [5,5,20,20,15,15,20];
    let total = weights.reduce((a,b)=>a+b,0);
    let r = Math.random() * total, acc=0, pick=multipliers[0];
    for (let i=0;i<weights.length;i++){
      acc+=weights[i];
      if(r<=acc){ pick=multipliers[i]; break; }
    }

    // build the path
    let x=50;
    const path = [];
    for(let i=0;i<rows;i++){
      const dir = Math.random()<0.5 ? -1 : 1;
      x = Math.min(Math.max(x + dir*(binWidthPct/2), 0), 100 - binWidthPct);
      const y = (i+1)*rowSpacingPct;
      path.push({ left: x, top: y });
    }
    path.push({ left: x, top: 100 }); // final bin

    // animate through the path
    path.forEach((pos,i)=>{
      setTimeout(()=> setBallPos(pos), (i+1)*stepDuration);
    });

    // show result once done
    setTimeout(()=> setResultMultiplier(pick),
      (path.length+1)*stepDuration);
  };

  const reset = () => {
    setBetAmount(null);
    setResultMultiplier(null);
    setBallPos({ left:50, top:0 });
  };

  return (
    <div className="plinko-container">
      {/* Always show the board */}
      <div className="plinko-board">
        {/* bins */}
        {multipliers.map((m,i)=>(
          <div
            key={i}
            className="bin"
            style={{ left:`${i*binWidthPct}%`, width:`${binWidthPct}%` }}
          >
            <span className="bin-label">×{m}</span>
          </div>
        ))}

        {/* pegs */}
        {Array.from({ length: rows }).flatMap((_, rowIdx) => {
          const offset = rowIdx % 2 === 0 ? binWidthPct/2 : 0;
          return Array.from({ length: binCount - 1 }).map((__, pegIdx) => {
            const left = offset + pegIdx * binWidthPct;
            const top = (rowIdx + 1) * rowSpacingPct;
            return (
              <div
                key={`peg-${rowIdx}-${pegIdx}`}
                className="peg"
                style={{ left:`${left}%`, top:`${top}%` }}
              />
            );
          });
        })}

        {/* ball */}
        {betAmount != null && (
          <div
            className="ball"
            style={{ left:`${ballPos.left}%`, top:`${ballPos.top}%` }}
          />
        )}
      </div>

      {/* BetForm only before dropping */}
      {betAmount == null && (
        <BetForm balance={balance} onBet={handleBet} showModal={showModal} />
      )}

      {/* Dropping state */}
      {betAmount != null && resultMultiplier == null && (
        <p className="plinko-dropping">Dropping the ball…</p>
      )}

      {/* Result overlay, board still visible underneath */}
      {resultMultiplier != null && (
        <div className="plinko-result">
          <p>You landed on <strong>×{resultMultiplier}</strong>!</p>
          <button onClick={()=>{
            onBet(-(betAmount * resultMultiplier));
            reset();
          }}>Collect</button>
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './plinko.css';

export default function Plinko({ balance, onBet, showModal }) {
  const [betAmount, setBetAmount] = useState(null);
  const [resultMultiplier, setResultMultiplier] = useState(null);
  const [ballPos, setBallPos] = useState({ left: 50, top: 0 });

  // 11 bins: [10,5,2,1,0.5,0.2,0.5,1,2,5,10]
  const multipliers = [10,5,2,1,0.5,0.2,0.5,1,2,5,10];
  const weights     = [1,1.5,2.5,10,15,40,15,10,2.5,1.5,1]; // percentages
  const binCount    = multipliers.length;
  const binWidthPct = 100 / binCount;
  const rows        = binCount - 1;
  const rowSpacing  = 100 / (rows + 1);
  const stepDur     = 300; // ms

  const handleBet = amt => {
    setBetAmount(amt);
    setResultMultiplier(null);
    setBallPos({ left: 50, top: 0 });
    onBet(amt);

    // pick weighted multiplier
    let total = weights.reduce((a,b)=>a+b,0);
    let r = Math.random()*total, acc=0, pick=multipliers[0];
    for (let i=0; i<weights.length; i++){
      acc += weights[i];
      if (r <= acc) { pick = multipliers[i]; break; }
    }

    // build random “bounce” path
    let x = 50, path = [];
    for (let i=0; i<rows; i++){
      const dir = Math.random()<0.5 ? -1 : 1;
      x = Math.min(Math.max(x + dir*(binWidthPct/2), 0), 100-binWidthPct);
      path.push({ left: x, top: (i+1)*rowSpacing });
    }
    path.push({ left: x, top: 100 });

    // animate ball
    path.forEach((pos,i)=>{
      setTimeout(()=> setBallPos(pos), (i+1)*stepDur);
    });
    // reveal result
    setTimeout(()=> setResultMultiplier(pick), (path.length+1)*stepDur);
  };

  const reset = () => {
    setBetAmount(null);
    setResultMultiplier(null);
    setBallPos({ left:50, top:0 });
  };

  return (
    <div className="plinko-container">
      {/* always render board */}
      <div className="plinko-board">
        {multipliers.map((m,i)=>(
          <div
            key={i}
            className="bin"
            style={{ left:`${i*binWidthPct}%`, width:`${binWidthPct}%` }}
          >
            <span className="bin-label">{m}×</span>
          </div>
        ))}

        {/* pegs */}
        {Array.from({ length: rows }).flatMap((_,ri)=>{
          const offset = ri % 2 === 0 ? binWidthPct/2 : 0;
          return Array.from({ length: binCount-1 }).map((__,pj)=>{
            const left = offset + pj*binWidthPct;
            const top  = (ri+1)*rowSpacing;
            return <div key={`${ri}-${pj}`} className="peg" style={{ left:`${left}%`, top:`${top}%` }} />;
          });
        })}

        {/* ball */}
        {betAmount!=null && (
          <div className="ball" style={{ left:`${ballPos.left}%`, top:`${ballPos.top}%` }} />
        )}
      </div>

      {/* pre-drop BetForm */}
      {betAmount==null && (
        <BetForm balance={balance} onBet={handleBet} showModal={showModal} />
      )}

      {/* dropping indicator */}
      {betAmount!=null && resultMultiplier==null && (
        <p className="plinko-dropping">Dropping the ball…</p>
      )}

      {/* result overlay */}
      {resultMultiplier!=null && (
        <div className="plinko-result">
          <p>You landed on <strong>{resultMultiplier}×</strong>!</p>
          <button onClick={()=>{
            onBet(-(betAmount*resultMultiplier));
            reset();
          }}>Collect</button>
          <button onClick={reset}>Play Again</button>
        </div>
      )}
    </div>
  );
}

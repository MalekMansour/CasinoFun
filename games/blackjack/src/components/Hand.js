import React from 'react';
import Card from './Card';
import { getHandValue } from '../utils/game';

export default function Hand({ cards, title, hideHoleCard = false }) {
  const displayValue = hideHoleCard ? '?' : getHandValue(cards);
  return (
    <div className="hand">
      <h2>{title} ({displayValue})</h2>
      <div className="cards">
        {cards.map((c, i) => (
          <div key={i}>
            {i === 1 && hideHoleCard
              ? <div className="card back"></div>
              : <Card card={c} />}
          </div>
        ))}
      </div>
    </div>
  );
}

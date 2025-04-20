import React from 'react';

export default function Card({ card }) {
  const color = card.suit === '♥' || card.suit === '♦' ? 'red' : 'black';
  return (
    <div className="card" style={{ color }}>
      <div className="corner">
        {card.rank}{card.suit}
      </div>
      <div className="center">
        <span>{card.suit}</span>
      </div>
      <div className="corner flip">
        {card.rank}{card.suit}
      </div>
    </div>
  );
}

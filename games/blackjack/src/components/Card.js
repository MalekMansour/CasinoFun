// src/components/Card.js
import React from 'react'

export default function Card({ card }) {
  // red for hearts & diamonds, black otherwise
  const color = card.suit === '♥' || card.suit === '♦' ? 'red' : 'black'

  return (
    <div className="card" style={{ color }}>
      <div className="corner">
        <span>{card.rank}{card.suit}</span>
      </div>
      <div className="center">
        <span style={{ fontSize: '1.5rem' }}>{card.suit}</span>
      </div>
      <div className="corner flip">
        <span>{card.rank}{card.suit}</span>
      </div>
    </div>
  )
}
X
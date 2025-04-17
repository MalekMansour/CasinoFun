import React from 'react'
import Card from './Card'

export default function Hand({ cards, title, hideHoleCard=false }){
  return (
    <div className='hand'>
      <h2>{title} ({hideHoleCard ? '?' : cards.map(c=>c).length})</h2>
      <div className='cards'>
        {cards.map((c,i)=>(
          <div key={i}>
            {i===1 && hideHoleCard
              ? <div className='card back'></div>
              : <Card card={c}/>
            }
          </div>
        ))}
      </div>
    </div>
  )
}

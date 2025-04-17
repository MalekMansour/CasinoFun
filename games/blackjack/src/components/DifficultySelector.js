import React from 'react'

export default function DifficultySelector({ difficulty, setDifficulty }){
  return (
    <div className='difficulty'>
      <label>
        <input 
          type='radio' 
          name='diff' 
          value='easy' 
          checked={difficulty==='easy'} 
          onChange={e=>setDifficulty(e.target.value)}
        /> Easy
      </label>
      <label>
        <input 
          type='radio' 
          name='diff' 
          value='medium' 
          checked={difficulty==='medium'} 
          onChange={e=>setDifficulty(e.target.value)}
        /> Medium
      </label>
      <label>
        <input 
          type='radio' 
          name='diff' 
          value='hard' 
          checked={difficulty==='hard'} 
          onChange={e=>setDifficulty(e.target.value)}
        /> Hard
      </label>
    </div>
  )
}

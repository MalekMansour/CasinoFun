import React, { useState, useEffect } from 'react'
import {
  dealInitialHands,
  getHandValue,
  shouldDealerHit
} from './utils/game'
import DifficultySelector from './components/DifficultySelector'
import Hand from './components/Hand'
import Controls from './components/Controls'
import './index.css'

export default function App(){
  const [deck, setDeck] = useState([])
  const [playerHand, setPlayerHand] = useState([])
  const [dealerHand, setDealerHand] = useState([])
  const [diff, setDiff] = useState('medium')
  const [message, setMessage] = useState('')
  const [over, setOver] = useState(false)

  useEffect(()=>{
    startGame()
  },[diff])

  function startGame(){
    const { deck, playerHand, dealerHand } = dealInitialHands()
    setDeck(deck)
    setPlayerHand(playerHand)
    setDealerHand(dealerHand)
    setOver(false)
    setMessage('')
  }

  function handleHit(){
    if(over) return
    const card = deck[0]
    setDeck(d=>d.slice(1))
    const newHand = [...playerHand, card]
    setPlayerHand(newHand)
    if(getHandValue(newHand)>21){
      setMessage('Busted! Dealer wins.')
      setOver(true)
    }
  }

  function handleStand(){
    if(over) return
    let d = [...dealerHand]
    let newDeck = [...deck]
    while( shouldDealerHit(d, playerHand, diff, newDeck) ){
      const c = newDeck.shift()
      d.push(c)
    }
    setDealerHand(d)
    setDeck(newDeck)

    const pVal = getHandValue(playerHand)
    const dVal = getHandValue(d)
    let result = ''
    if(dVal>21 || pVal>dVal) result='Player wins!'
    else if(pVal===dVal) result='Push!'
    else result='Dealer wins!'
    setMessage(result)
    setOver(true)
  }

  return (
    <div className='game'>
      <h1>♣ React Blackjack ♠</h1>
      <DifficultySelector difficulty={diff} setDifficulty={setDiff}/>
      <div className='tables'>
        <Hand cards={playerHand} title='Player'/>
        <Hand cards={dealerHand} title='Dealer' hideHoleCard={!over}/>
      </div>
      <Controls onHit={handleHit} onStand={handleStand} disabled={over}/>
      {message && <h2 className='msg'>{message}</h2>}
      <button onClick={startGame} className='new'>New Game</button>
    </div>
  )
}

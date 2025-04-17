import React, { useState, useEffect } from 'react';
import {
  dealInitialHands,
  getHandValue,
  shouldDealerHit
} from './utils/game';
import DifficultySelector from './components/DifficultySelector';
import Hand from './components/Hand';
import Controls from './components/Controls';
import './index.css';

export default function App() {
  const [deck, setDeck] = useState([]);
  const [playerHand, setPlayerHand] = useState([]);
  const [dealerHand, setDealerHand] = useState([]);
  const [diff, setDiff] = useState('medium');
  const [message, setMessage] = useState('');
  const [over, setOver] = useState(false);

  useEffect(() => {
    startGame();
  }, [diff]);

  function startGame() {
    const { deck: newDeck, playerHand, dealerHand } = dealInitialHands();
    setDeck(newDeck);
    setPlayerHand(playerHand);
    setDealerHand(dealerHand);
    setOver(false);
    setMessage('');
  }

  function handleHit() {
    if (over) return;
    const [card, ...rest] = deck;
    const newHand = [...playerHand, card];
    setDeck(rest);
    setPlayerHand(newHand);
    if (getHandValue(newHand) > 21) {
      setMessage('Busted! Dealer wins.');
      setOver(true);
    }
  }

  function handleStand() {
    if (over) return;
    let d = [...dealerHand];
    let dDeck = [...deck];
    while (shouldDealerHit(d, playerHand, diff, dDeck)) {
      const [card, ...rest] = dDeck;
      d.push(card);
      dDeck = rest;
    }
    setDealerHand(d);
    setDeck(dDeck);

    const pVal = getHandValue(playerHand);
    const dVal = getHandValue(d);
    let result;
    if (dVal > 21 || pVal > dVal) result = 'Player wins!';
    else if (pVal === dVal) result = 'Push!';
    else result = 'Dealer wins!';
    setMessage(result);
    setOver(true);
  }

  return (
    <div className="game">
      <h1>♣ React Blackjack ♠</h1>
      <DifficultySelector difficulty={diff} setDifficulty={setDiff} />
      <div className="tables">
        <Hand cards={playerHand} title="Player" />
        <Hand cards={dealerHand} title="Dealer" hideHoleCard={!over} />
      </div>
      <Controls onHit={handleHit} onStand={handleStand} disabled={over} />
      {message && <h2 className="msg">{message}</h2>}
      <button onClick={startGame} className="new">New Game</button>

      <section className="rules">
        <h2>Blackjack Rules</h2>
        <ul>
          <li>Goal: get closer to 21 than the dealer without busting (going over 21).</li>
          <li>Number cards are worth their face value; J/Q/K = 10; Ace = 1 or 11.</li>
          <li>You may “Hit” to draw a card or “Stand” to end your turn.</li>
          <li>If your hand exceeds 21, you bust and lose immediately.</li>
          <li>The dealer must hit until reaching at least 17, then stand.</li>
          <li>If you and the dealer tie, it’s a “Push” (nobody wins).</li>
        </ul>
      </section>
    </div>
  );
}

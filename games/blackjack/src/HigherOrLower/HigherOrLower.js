import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import './higherorlower.css';

const cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'];
const cardValue = c => (typeof c === 'number' ? c : { J: 11, Q: 12, K: 13, A: 14 }[c]);

export default function HigherOrLower({ balance, onBet, showModal }) {
  const [bet, setBet] = useState(null);
  const [currentCard, setCurrentCard] = useState(null);
  const [nextCard, setNextCard] = useState(null);
  const [multiplier, setMultiplier] = useState(1.1);
  const [history, setHistory] = useState([]);
  const [lost, setLost] = useState(false);

  const drawCard = () => cards[Math.floor(Math.random() * cards.length)];

  const startGame = amt => {
    onBet(amt);
    const card = drawCard();
    setBet(amt);
    setCurrentCard(card);
    setNextCard(null);
    setMultiplier(1.1);
    setHistory([card]);
    setLost(false);
  };

  const guess = dir => {
    const next = drawCard();
    setNextCard(next);
    const win =
      (dir === 'higher' && cardValue(next) > cardValue(currentCard)) ||
      (dir === 'lower' && cardValue(next) < cardValue(currentCard));

    if (win) {
      setMultiplier(m => parseFloat((m + 0.2).toFixed(2)));
      setCurrentCard(next);
      setHistory(h => [...h, next]);
    } else {
      setLost(true);
      showModal('You lost! 💥');
    }
  };

  const cashOut = () => {
    const winnings = Math.ceil(bet * multiplier);
    onBet(-winnings);
    showModal(`You cashed out ×${multiplier.toFixed(2)} = $${winnings}`);
    reset();
  };

  const reset = () => {
    setBet(null);
    setCurrentCard(null);
    setNextCard(null);
    setMultiplier(1.1);
    setHistory([]);
    setLost(false);
  };

  return (
    <div className="hol-container">
      {!bet ? (
        <BetForm balance={balance} onBet={startGame} showModal={showModal} />
      ) : (
        <div className="hol-game">
          <p>Current Card: <strong>{currentCard}</strong></p>
          <div className="hol-buttons">
            <button onClick={() => guess('higher')} disabled={lost}>
              Higher
            </button>
            <button onClick={() => guess('lower')} disabled={lost}>
              Lower
            </button>
          </div>
          {nextCard !== null && (
            <p>Next Card: <strong>{nextCard}</strong></p>
          )}
          <p>Multiplier: ×{multiplier.toFixed(2)}</p>
          {lost ? (
            <button onClick={reset}>Try Again</button>
          ) : (
            <button onClick={cashOut}>Cash Out</button>
          )}
          <div className="hol-history">
            History: {history.join(' → ')}
          </div>
        </div>
      )}
    </div>
  );
}

import React, { useState } from 'react';
import BetForm from '../components/BetForm';
import Card from '../components/Card';
import './HigherOrLower.css';

// Ranks and suits
const RANKS = [2,3,4,5,6,7,8,9,10,'J','Q','K','A'];
const SUITS = ['♠','♥','♦','♣'];

const cardValue = c =>
  typeof c.rank === 'number'
    ? c.rank
    : { J:11, Q:12, K:13, A:14 }[c.rank];

function drawCard() {
  const rank = RANKS[Math.floor(Math.random() * RANKS.length)];
  const suit = SUITS[Math.floor(Math.random() * SUITS.length)];
  return { rank, suit };
}

export default function HigherOrLower({ balance, onBet, showModal }) {
  const [bet, setBet] = useState(null);
  const [currentCard, setCurrentCard] = useState(null);
  const [nextCard, setNextCard] = useState(null);
  const [multiplier, setMultiplier] = useState(1.1);
  const [history, setHistory] = useState([]);
  const [lost, setLost] = useState(false);

  const startGame = amt => {
    onBet(amt);
    const first = drawCard();
    setBet(amt);
    setCurrentCard(first);
    setNextCard(null);
    setMultiplier(1.1);
    setHistory([first]);
    setLost(false);
  };

  const guess = dir => {
    const next = drawCard();
    setNextCard(next);

    const win =
      (dir === 'higher' && cardValue(next) >  cardValue(currentCard)) ||
      (dir === 'lower'  && cardValue(next) <  cardValue(currentCard));

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
            <h2 className="hol-title">Higher Or Lower</h2>

      {!bet ? (
        <BetForm balance={balance} onBet={startGame} showModal={showModal} />
      ) : (
        <div className="hol-game">
          <div className="hol-current">
            <p>Current Card:</p>
            <Card card={currentCard} />
          </div>

          <div className="hol-buttons">
            <button onClick={() => guess('higher')} disabled={lost}>
              Higher
            </button>
            <button onClick={() => guess('lower')}  disabled={lost}>
              Lower
            </button>
          </div>

          {nextCard && (
            <div className="hol-next">
              <p>Next Card:</p>
              <Card card={nextCard} />
            </div>
          )}

          <p className="hol-mult">Multiplier: ×{multiplier.toFixed(2)}</p>

          {lost ? (
            <button className="hol-action" onClick={reset}>
              Try Again
            </button>
          ) : (
            <button className="hol-action" onClick={cashOut}>
              Cash Out
            </button>
          )}

          <div className="hol-history">
            History:&nbsp;
            {history.map((c, i) => (
              <React.Fragment key={i}>
                <Card card={c} />
                {i < history.length - 1 && ' → '}
              </React.Fragment>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

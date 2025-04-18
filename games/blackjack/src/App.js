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

  const [balance, setBalance] = useState(100);
  const [bet, setBet] = useState('');
  const [betPlaced, setBetPlaced] = useState(false);

  // Whenever a bet is placed (or difficulty changes), start a new round
  useEffect(() => {
    if (betPlaced) startGame();
  }, [betPlaced, diff]);

  function addFunds() {
    const input = prompt('Enter amount to add to your balance:');
    const amt = parseInt(input, 10);
    if (isNaN(amt) || amt <= 0) {
      alert('Invalid amount.');
      return;
    }
    setBalance(bal => bal + amt);
  }

  function placeBet() {
    const b = parseInt(bet, 10);
    if (isNaN(b) || b <= 0) {
      alert('Please enter a valid bet greater than 0.');
      return;
    }
    if (b > balance) {
      alert('Bet exceeds your balance.');
      return;
    }
    setBetPlaced(true);
  }

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
      const result = 'Dealer wins!';
      setMessage('Busted! Dealer wins.');
      setOver(true);
      endRound(result);
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
    endRound(result);
  }

  function endRound(result) {
    if (result === 'Player wins!') {
      setBalance(bal => bal + parseInt(bet, 10));
    } else if (result === 'Dealer wins!') {
      setBalance(bal => bal - parseInt(bet, 10));
    }
    // Push = no change
    setBetPlaced(false);
    setBet('');
  }

  return (
    <div className="game">
      <h1>♣ React Blackjack ♠</h1>

      <div className="bank">
        <p>Balance: ${balance}</p>
        <button onClick={addFunds}>Add Funds</button>
      </div>

      {!betPlaced ? (
        <div className="bank">
          <input
            type="number"
            placeholder="Bet amount"
            value={bet}
            onChange={e => setBet(e.target.value)}
            min="1"
            max={balance}
          />
          <button onClick={placeBet}>Place Bet</button>
        </div>
      ) : (
        <p>Current Bet: ${bet}</p>
      )}

      <DifficultySelector difficulty={diff} setDifficulty={setDiff} />

      <div className="tables">
        <Hand cards={playerHand} title="Player" />
        <Hand cards={dealerHand} title="Dealer" hideHoleCard={!over} />
      </div>

      <Controls
        onHit={handleHit}
        onStand={handleStand}
        disabled={over || !betPlaced}
      />

      {message && <h2 className="msg">{message}</h2>}

      <button
        onClick={() => betPlaced && startGame()}
        className="new"
        disabled={!betPlaced}
      >
        New Round
      </button>

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

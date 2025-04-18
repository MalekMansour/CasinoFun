import React, { useState } from 'react';
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
  const [over, setOver] = useState(true);       // true means no round in progress
  const [balance, setBalance] = useState(100);
  const [bet, setBet] = useState('');
  const [betPlaced, setBetPlaced] = useState(false);

  const inProgress = betPlaced && !over;

  function addFunds() {
    const input = prompt('Enter amount to add:');
    const amt = parseInt(input, 10);
    if (!amt || amt <= 0) return alert('Invalid amount.');
    setBalance(b => b + amt);
  }

  function placeBet() {
    const b = parseInt(bet, 10);
    if (!b || b <= 0) return alert('Enter a valid bet.');
    if (b > balance) return alert('Bet exceeds balance.');
    setBetPlaced(true);
    setOver(false);
    setMessage('');
    // deal
    const { deck, playerHand, dealerHand } = dealInitialHands();
    setDeck(deck);
    setPlayerHand(playerHand);
    setDealerHand(dealerHand);
  }

  function handleHit() {
    if (!inProgress) return;
    const [card, ...rest] = deck;
    const newHand = [...playerHand, card];
    setDeck(rest);
    setPlayerHand(newHand);

    if (getHandValue(newHand) > 21) {
      setMessage('Busted! Dealer wins.');
      endRound('Dealer wins!');
    }
  }

  function handleStand() {
    if (!inProgress) return;
    let d = [...dealerHand], dDeck = [...deck];
    while (shouldDealerHit(d, playerHand, diff, dDeck)) {
      const [card, ...rest] = dDeck;
      d.push(card);
      dDeck = rest;
    }
    setDealerHand(d);
    setDeck(dDeck);

    const pVal = getHandValue(playerHand),
          dVal = getHandValue(d);
    let result;
    if (dVal > 21 || pVal > dVal) result = 'Player wins!';
    else if (pVal === dVal) result = 'Push!';
    else result = 'Dealer wins!';
    setMessage(result);
    endRound(result);
  }

  function endRound(result) {
    // adjust balance
    const b = parseInt(bet, 10);
    if (result === 'Player wins!') setBalance(bal => bal + b);
    else if (result === 'Dealer wins!') setBalance(bal => bal - b);
    // finish round
    setOver(true);
    setBetPlaced(false);
  }

  return (
    <div className="game">
      <h1>♣ Blackjack ♠</h1>

      <div className="bank">
        <p><strong>Balance:</strong> ${balance}</p>
        <button onClick={addFunds}>Add Funds</button>
      </div>

      {!inProgress ? (
        <div className="bank">
          <input
            type="number"
            placeholder="Your bet"
            value={bet}
            onChange={e => setBet(e.target.value)}
            min="1"
            max={balance}
          />
          <button onClick={placeBet}>Place Bet & Deal</button>
        </div>
      ) : (
        <p><strong>Current Bet:</strong> ${bet}</p>
      )}

      <DifficultySelector difficulty={diff} setDifficulty={setDiff} />

      <div className="tables">
        <Hand cards={playerHand} title="Player" />
        <Hand cards={dealerHand} title="Dealer" hideHoleCard={!over} />
      </div>

      <Controls
        onHit={handleHit}
        onStand={handleStand}
        disabled={!inProgress}
      />

      {message && <h2 className="msg">{message}</h2>}
    </div>
  );
}

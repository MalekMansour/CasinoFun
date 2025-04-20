import React, { useState, useEffect } from 'react';
import { FaSun, FaMoon } from 'react-icons/fa';
import {
  dealInitialHands,
  getHandValue,
  shouldDealerHit
} from './utils/game';
import DifficultySelector from './components/DifficultySelector';
import Hand from './components/Hand';
import Controls from './components/Controls';
import './index.css';

// Generic modal for messages
function Modal({ message, onClose }) {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <p>{message}</p>
        <button onClick={onClose}>OK</button>
      </div>
    </div>
  );
}

function MainMenu({ onLoad, showModal }) {
  const [usernameInput, setUsernameInput] = useState('');
  const [saves, setSaves] = useState([]);

  useEffect(() => {
    const keys = Object.keys(localStorage)
      .filter(k => k.startsWith('Save_File_'))
      .sort((a, b) => {
        const na = +a.split('_').pop(),
              nb = +b.split('_').pop();
        return na - nb;
      });
    setSaves(keys);
  }, []);

  const createSave = () => {
    const name = usernameInput.trim();
    if (!name) return showModal('Enter a username.');
    const indices = saves.map(k => +k.split('_').pop());
    const next = indices.length ? Math.max(...indices) + 1 : 1;
    const key = `Save_File_${next}`;
    const data = { username: name, balance: 1000 };
    localStorage.setItem(key, JSON.stringify(data));
    onLoad(key, data);
  };

  const loadSave = key => {
    const data = JSON.parse(localStorage.getItem(key));
    onLoad(key, data);
  };

  const deleteSave = key => {
    localStorage.removeItem(key);
    setSaves(saves.filter(s => s !== key));
    showModal(`Deleted ${key}.`);
  };

  return (
    <div className="main-menu">
      <h1>♣ Blackjack ♠</h1>

      <div className="bank">
        <h2>Create New Save</h2>
        <input
          type="text"
          placeholder="Username"
          value={usernameInput}
          onChange={e => setUsernameInput(e.target.value)}
        />
        <button onClick={createSave}>Create</button>
      </div>

      <div className="bank">
        <h2>Load Save</h2>
        {saves.length ? (
          saves.map(k => {
            const d = JSON.parse(localStorage.getItem(k));
            return (
              <div key={k} className="save-entry">
                <button onClick={() => loadSave(k)}>
                  {k} ({d.username}, ${d.balance})
                </button>
                <button
                  className="delete-btn"
                  onClick={() => deleteSave(k)}
                >
                  Delete
                </button>
              </div>
            );
          })
        ) : (
          <p>No saves found.</p>
        )}
      </div>
    </div>
  );
}

function BetForm({ balance, onBet, showModal }) {
  const [amt, setAmt] = useState('');
  const place = () => {
    const b = parseInt(amt, 10);
    if (!b || b <= 0) return showModal('Enter a valid bet.');
    if (b > balance) return showModal('Bet exceeds balance.');
    onBet(b);
    setAmt('');
  };
  return (
    <>
      <input
        type="number"
        placeholder="Bet"
        value={amt}
        onChange={e => setAmt(e.target.value)}
        min="1"
        max={balance}
      />
      <button onClick={place}>Deal</button>
    </>
  );
}

export default function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [currentSave, setCurrentSave] = useState(null);
  const [username, setUsername] = useState('');
  const [balance, setBalance] = useState(0);

  const [deck, setDeck] = useState([]);
  const [playerHand, setPlayerHand] = useState([]);
  const [dealerHand, setDealerHand] = useState([]);
  const [diff, setDiff] = useState('medium');
  const [message, setMessage] = useState('');
  const [over, setOver] = useState(true);

  const [currentBet, setCurrentBet] = useState(0);
  const [modalMessage, setModalMessage] = useState('');

  const showModal = msg => setModalMessage(msg);

  // Theme toggle
  useEffect(() => {
    document.body.classList.toggle('light-mode', !darkMode);
  }, [darkMode]);

  // Auto-save on balance/username change
  useEffect(() => {
    if (currentSave) {
      localStorage.setItem(
        currentSave,
        JSON.stringify({ username, balance })
      );
    }
  }, [username, balance, currentSave]);

  // Place/save loaded
  if (!currentSave) {
    return (
      <>
        <MainMenu
          onLoad={(key, data) => {
            setCurrentSave(key);
            setUsername(data.username);
            setBalance(data.balance);
            setOver(true);
            setMessage('');
          }}
          showModal={showModal}
        />
        {modalMessage && (
          <Modal
            message={modalMessage}
            onClose={() => setModalMessage('')}
          />
        )}
      </>
    );
  }

  const inProgress = !over;

  const placeBet = betAmt => {
    setCurrentBet(betAmt);
    setBalance(b => b - betAmt);
    const { deck, playerHand, dealerHand } = dealInitialHands();
    setDeck(deck);
    setPlayerHand(playerHand);
    setDealerHand(dealerHand);
    setOver(false);
    setMessage('');
  };

  const finishRound = result => {
    if (result === 'Player wins!') {
      setBalance(b => b + currentBet * 2);
    } else if (result === 'Dealer wins!') {
      // refill only if bankrupt
      if (balance <= 0) {
        showModal("You went bankrupt! Here's $1,000 to continue.");
        setBalance(1000);
      }
    } else if (result === 'Tie') {
      setBalance(b => b + currentBet);
    }
    setOver(true);
  };

  const handleHit = () => {
    if (!inProgress) return;
    const [card, ...rest] = deck;
    const newHand = [...playerHand, card];
    setDeck(rest);
    setPlayerHand(newHand);
    if (getHandValue(newHand) > 21) {
      setMessage('Busted! Dealer wins.');
      finishRound('Dealer wins!');
    }
  };

  const handleStand = () => {
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
    let result =
      dVal > 21 || pVal > dVal
        ? 'Player wins!'
        : pVal === dVal
        ? 'Tie'
        : 'Dealer wins!';

    setMessage(result);
    finishRound(result);
  };

  return (
    <>
      {modalMessage && (
        <Modal
          message={modalMessage}
          onClose={() => setModalMessage('')}
        />
      )}
      <div className="game">
        <button
          className="theme-toggle"
          onClick={() => setDarkMode(d => !d)}
          aria-label="Toggle theme"
        >
          {darkMode ? <FaSun /> : <FaMoon />}
        </button>

        <h1>♣ React Blackjack ♠</h1>
        <p><strong>User:</strong> {username}</p>
        <p><strong>Balance:</strong> ${balance}</p>

        {!inProgress ? (
          <div className="bank">
            <h2>Place your bet</h2>
            <BetForm
              balance={balance}
              onBet={placeBet}
              showModal={showModal}
            />
          </div>
        ) : (
          <p><strong>Current Bet:</strong> ${currentBet}</p>
        )}

        <DifficultySelector difficulty={diff} setDifficulty={setDiff} />

        <div className="tables">
          <Hand cards={playerHand} title="Player" />
          <Hand cards={dealerHand} title="Dealer" hideHoleCard={!over} />
        </div>

        <Controls onHit={handleHit} onStand={handleStand} disabled={!inProgress} />

        {message && <h2 className="msg">{message}</h2>}
      </div>
    </>
  );
}

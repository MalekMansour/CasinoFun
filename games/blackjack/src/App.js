// src/App.js
import React, { useState, useEffect, useRef } from 'react';
import { FaSun } from 'react-icons/fa';
import { IoMdMoon } from 'react-icons/io';
import { HiVolumeUp, HiVolumeOff } from 'react-icons/hi';
import bgMusic from './assets/background.mp3';
import {
  dealInitialHands,
  getHandValue,
  shouldDealerHit
} from './utils/game';
import Hand from './components/Hand';
import Controls from './components/Controls';
import BetForm from './components/BetForm';
import MainMenu from './MainMenu';
import Sidebar from './components/sidebar';      // lowercase file
import Plinko from './plinko/plinko';           // lowercase file
import './index.css';

function Modal({ message, onClose }) {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <p>{message}</p>
        <button className="modal-ok" onClick={onClose}>OK</button>
      </div>
    </div>
  );
}

export default function App() {
  const [darkMode, setDarkMode] = useState(true);
  const [musicOn, setMusicOn] = useState(false);
  const audioRef = useRef(new Audio(bgMusic));

  const [currentSave, setCurrentSave] = useState(null);
  const [username, setUsername] = useState('');
  const [balance, setBalance] = useState(0);
  const [deck, setDeck] = useState([]);
  const [playerHand, setPlayerHand] = useState([]);
  const [dealerHand, setDealerHand] = useState([]);
  const [message, setMessage] = useState('');
  const [over, setOver] = useState(true);
  const [currentBet, setCurrentBet] = useState(0);
  const [modalMessage, setModalMessage] = useState('');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const [game, setGame] = useState('blackjack');
  const diff = 'medium';

  useEffect(() => {
    audioRef.current.loop = true;
  }, []);

  const toggleMusic = () => {
    musicOn ? audioRef.current.pause() : audioRef.current.play();
    setMusicOn(on => !on);
  };

  const showModal = msg => setModalMessage(msg);

  useEffect(() => {
    document.body.classList.toggle('light-mode', !darkMode);
  }, [darkMode]);

  useEffect(() => {
    if (currentSave) {
      localStorage.setItem(
        currentSave,
        JSON.stringify({ username, balance })
      );
    }
  }, [username, balance, currentSave]);

  const handleLoad = (key, data) => {
    setCurrentSave(key);
    setUsername(data.username);
    setBalance(data.balance);
    setOver(true);
    setMessage('');
    setGame('blackjack');
  };

  const handleLogout = () => {
    setCurrentSave(null);
    setUsername('');
    setBalance(0);
  };

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
    } else if (result === 'Dealer wins!' && balance <= 0) {
      showModal("You went bankrupt! Here's $1,000 to continue.");
      setBalance(1000);
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
    const result =
      dVal > 21 || pVal > dVal
        ? 'Player wins!'
        : pVal === dVal
          ? 'Tie'
          : 'Dealer wins!';
    setMessage(result);
    finishRound(result);
  };

  const handlePlinkoBet = amt => setBalance(b => b - amt);

  const renderBlackjack = () => (
    <>
      <div className="tables">
        <Hand cards={playerHand} title="Player" />
        <Hand cards={dealerHand} title="Dealer" hideHoleCard={!over} />
      </div>

      {over ? (
        <BetForm balance={balance} onBet={placeBet} showModal={showModal} />
      ) : (
        <div className="controls-container">
          <Controls onHit={handleHit} onStand={handleStand} disabled={!inProgress} />
        </div>
      )}

      {message && <div className="round-msg">{message}</div>}
    </>
  );

  if (!currentSave) {
    return (
      <>
        <MainMenu onLoad={handleLoad} showModal={showModal} />
        {modalMessage && (
          <Modal message={modalMessage} onClose={() => setModalMessage('')} />
        )}
      </>
    );
  }

  return (
    <>
      {modalMessage && (
        <Modal message={modalMessage} onClose={() => setModalMessage('')} />
      )}

      <Sidebar
        username={username}
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(c => !c)}
        onLogout={handleLogout}
        game={game}
        setGame={setGame}
      />

      <div className="main-content">
        <header className="top-banner">
          <div className="balance-container">Balance: ${balance}</div>
          <div className="top-controls">
            <button
              className="theme-toggle"
              onClick={() => setDarkMode(d => !d)}
              aria-label="Toggle theme"
            >
              {darkMode ? <IoMdMoon /> : <FaSun />}
            </button>
            <button
              className="music-toggle"
              onClick={toggleMusic}
              aria-label="Toggle music"
            >
              {musicOn ? <HiVolumeUp /> : <HiVolumeOff />}
            </button>
          </div>
        </header>

        <section className="game-area">
          {game === 'blackjack'
            ? renderBlackjack()
            : <Plinko balance={balance} onBet={handlePlinkoBet} showModal={showModal} />
          }
        </section>
      </div>
    </>
  );
}

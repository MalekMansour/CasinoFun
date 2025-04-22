// src/App.js
import React, { useState, useEffect, useRef } from 'react';
import { FaSun, FaChevronLeft, FaChevronRight, FaGamepad } from 'react-icons/fa';
import { IoMdMoon } from 'react-icons/io';
import { FaVolumeHigh, FaVolumeXmark } from 'react-icons/fa6';
import { HiVolumeUp, HiVolumeOff } from "react-icons/hi";
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

function Sidebar({ username, collapsed, onToggle, onLogout }) {
  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <button className="toggle-btn" onClick={onToggle}>
        {collapsed ? <FaChevronRight/> : <FaChevronLeft/>}
      </button>
      {!collapsed && <div className="sb-user">{username}</div>}
      <nav className="sb-games">
        <button className="sb-item">
          <FaGamepad className="sb-icon"/>
          {!collapsed && 'Blackjack'}
        </button>
      </nav>
      <button className="sb-logout" onClick={onLogout}>
        {!collapsed ? 'Logout' : <FaGamepad/>}
      </button>
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

  const diff = 'medium'; // AI difficulty always medium

  // loop background music
  useEffect(() => {
    audioRef.current.loop = true;
  }, []);

  const toggleMusic = () => {
    if (musicOn) audioRef.current.pause();
    else audioRef.current.play();
    setMusicOn(on => !on);
  };

  const showModal = msg => setModalMessage(msg);

  // dark/light mode
  useEffect(() => {
    document.body.classList.toggle('light-mode', !darkMode);
  }, [darkMode]);

  // persist save metadata
  useEffect(() => {
    if (currentSave) {
      localStorage.setItem(
        currentSave,
        JSON.stringify({ username, balance })
      );
    }
  }, [username, balance, currentSave]);

  // load a save into play
  const handleLoad = (key, data) => {
    setCurrentSave(key);
    setUsername(data.username);
    setBalance(data.balance);
    setOver(true);
    setMessage('');
  };

  // logout back to main menu
  const handleLogout = () => {
    setCurrentSave(null);
    setUsername('');
    setBalance(0);
  };

  // game in-progress flag
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

    const pVal = getHandValue(playerHand), dVal = getHandValue(d);
    const result = dVal > 21 || pVal > dVal
      ? 'Player wins!'
      : pVal === dVal
        ? 'Tie'
        : 'Dealer wins!';
    setMessage(result);
    finishRound(result);
  };

  // show MainMenu when nothing is loaded
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

  // game screen
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
              {darkMode ? <IoMdMoon /> :  <FaSun /> }
            </button>
            <button
              className="music-toggle"
              onClick={toggleMusic}
              aria-label="Toggle music"
            >
              {musicOn ? <HiVolumeUp /> : <HiVolumeOff /> }
            </button>
          </div>
        </header>

        <section className="game-area">
          {!inProgress ? (
            <BetForm balance={balance} onBet={placeBet} showModal={showModal} />
          ) : (
            <div className="current-bet">Bet: ${currentBet}</div>
          )}

          <div className="tables">
            <Hand cards={playerHand} title="Player" />
            <Hand cards={dealerHand} title="Dealer" hideHoleCard={!over} />
          </div>

          <div className="controls-container">
            <Controls onHit={handleHit} onStand={handleStand} disabled={!inProgress} />
          </div>

          {message && <div className="round-msg">{message}</div>}
        </section>
      </div>
    </>
  );
}

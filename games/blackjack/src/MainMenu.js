// src/MainMenu.js
import React, { useState, useEffect } from 'react';
import logo from './assets/logo.png';
import './index.css';

export default function MainMenu({ onLoad, showModal }) {
  const [usernameInput, setUsernameInput] = useState('');
  const [saves, setSaves] = useState([]);
  const [showNew, setShowNew] = useState(false);
  const [showLoad, setShowLoad] = useState(false);

  useEffect(() => {
    const keys = Object.keys(localStorage)
      .filter(k => k.startsWith('Save_File_'))
      .sort((a, b) => {
        const na = +a.split('_').pop(), nb = +b.split('_').pop();
        return na - nb;
      });
    setSaves(keys);
  }, []);

  const openNew = () => {
    setUsernameInput('');
    setShowNew(true);
    setShowLoad(false);
  };
  const openLoad = () => {
    setShowLoad(true);
    setShowNew(false);
  };
  const closePanels = () => {
    setShowNew(false);
    setShowLoad(false);
  };

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
      {/* Logo */}
      <img src={logo} alt="App Logo" className="main-menu-logo" />

      {/* Big pink buttons */}
      <div className="main-menu-buttons">
        <button className="menu-btn" onClick={openNew}>New Game</button>
        <button className="menu-btn" onClick={openLoad}>Load Game</button>
        <button className="menu-btn" onClick={() => window.close()}>Exit</button>
      </div>

      {/* New Game panel */}
      {showNew && (
        <div className="menu-panel">
          <h2>Create New Save</h2>
          <input
            type="text"
            placeholder="Username"
            value={usernameInput}
            onChange={e => setUsernameInput(e.target.value)}
          />
          <div className="panel-buttons">
            <button onClick={createSave}>Create</button>
            <button onClick={closePanels}>Cancel</button>
          </div>
        </div>
      )}

      {/* Load Game panel */}
      {showLoad && (
        <div className="menu-panel">
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
          <div className="panel-buttons">
            <button onClick={closePanels}>Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}

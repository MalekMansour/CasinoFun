// MainMenu.js
import React, { useState, useEffect } from 'react';
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

export default function MainMenu({ onLoad, showModal }) {
  const [usernameInput, setUsernameInput] = useState('');
  const [saves, setSaves] = useState([]);

  useEffect(() => {
    const keys = Object.keys(localStorage)
      .filter(k => k.startsWith('Save_File_'))
      .sort((a, b) => {
        const na = +a.split('_').pop(), nb = +b.split('_').pop();
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

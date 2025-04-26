import React from 'react';
import {
  FaChevronLeft,
  FaChevronRight,
  FaGamepad,
  FaCircle
} from 'react-icons/fa';
import { GiPokerHand } from "react-icons/gi";

export default function Sidebar({
  username,
  collapsed,
  onToggle,
  onLogout,
  game,
  setGame
}) {
  return (
    <div className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <button className="toggle-btn" onClick={onToggle}>
        {collapsed ? <FaChevronRight /> : <FaChevronLeft />}
      </button>

      {!collapsed && <div className="sb-user">{username}</div>}

      <nav className="sb-games">
        <button
          className={`sb-item ${game === 'blackjack' ? 'active' : ''}`}
          onClick={() => setGame('blackjack')}
        >
          <FaGamepad className="sb-icon" />
          {!collapsed && 'Blackjack'}
        </button>
        <button
          className={`sb-item ${game === 'plinko' ? 'active' : ''}`}
          onClick={() => setGame('plinko')}
        >
          <FaCircle className="sb-icon" />
          {!collapsed && 'Plinko'}
        </button>
      </nav>

      <button className="sb-logout" onClick={onLogout}>
        {!collapsed ? 'Logout' : <FaGamepad />}
      </button>
    </div>
  );
}

import React from 'react';
import {
  FaChevronLeft,
  FaChevronRight,
} from 'react-icons/fa';
import { GiPokerHand } from "react-icons/gi";
import { FaRegCircle } from "react-icons/fa";
import { IoIosExit } from "react-icons/io";


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
          <GiPokerHand className="sb-icon" />
          {!collapsed && 'Blackjack'}
        </button>
        <button
          className={`sb-item ${game === 'plinko' ? 'active' : ''}`}
          onClick={() => setGame('plinko')}
        >
          <FaRegCircle className="sb-icon" />
          {!collapsed && 'Plinko'}
        </button>
      </nav>

      <button className="sb-logout" onClick={onLogout}>
        {!collapsed ? 'Logout' : <IoIosExit />}
      </button>
    </div>
  );
}

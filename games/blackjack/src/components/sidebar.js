import React from 'react';
import {
  FaChevronLeft,
  FaChevronRight,
  FaCircle,
  FaDice,
  FaBomb,
  FaSortAmountUp
} from 'react-icons/fa';
import { GiPokerHand, GiTwoCoins } from 'react-icons/gi';
import { IoIosExit } from 'react-icons/io';

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
          <FaCircle className="sb-icon" />
          {!collapsed && 'Plinko'}
        </button>

        <button
          className={`sb-item ${game === 'headsAndTails' ? 'active' : ''}`}
          onClick={() => setGame('headsAndTails')}
        >
          <GiTwoCoins className="sb-icon" />
          {!collapsed && 'Heads & Tails'}
        </button>

        <button
          className={`sb-item ${game === 'dice' ? 'active' : ''}`}
          onClick={() => setGame('dice')}
        >
          <FaDice className="sb-icon" />
          {!collapsed && 'Dice'}
        </button>

        <button
          className={`sb-item ${game === 'mines' ? 'active' : ''}`}
          onClick={() => setGame('mines')}
        >
          <FaBomb className="sb-icon" />
          {!collapsed && 'Mines'}
        </button>

        <button
          className={`sb-item ${game === 'higherOrLower' ? 'active' : ''}`}
          onClick={() => setGame('higherOrLower')}
        >
          <FaSortAmountUp className="sb-icon" />
          {!collapsed && 'Higher/Lower'}
        </button>
      </nav>

      <button className="sb-logout" onClick={onLogout}>
        {!collapsed ? 'Logout' : <IoIosExit />}
      </button>
    </div>
  );
}

import React from 'react';

export default function DifficultySelector({ difficulty, setDifficulty }) {
  return (
    <div className="difficulty">
      {['easy','medium','hard'].map(level => (
        <label key={level}>
          <input
            type="radio"
            name="diff"
            value={level}
            checked={difficulty === level}
            onChange={e => setDifficulty(e.target.value)}
          /> {level.charAt(0).toUpperCase() + level.slice(1)}
        </label>
      ))}
    </div>
  );
}

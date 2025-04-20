export const suits = ['♠','♥','♦','♣'];
export const ranks = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];

export function createShuffledDeck(){
  const deck = [];
  suits.forEach(s => ranks.forEach(r => deck.push({ suit:s, rank:r })));
  for(let i = deck.length - 1; i > 0; i--){
    const j = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[j]] = [deck[j], deck[i]];
  }
  return deck;
}

export function dealInitialHands(){
  const deck = createShuffledDeck();
  return {
    deck,
    playerHand: [deck.shift(), deck.shift()],
    dealerHand: [deck.shift(), deck.shift()]
  };
}

export function getHandValue(hand){
  let total = 0, aces = 0;
  hand.forEach(({ rank }) => {
    if(rank === 'A'){ total += 11; aces++; }
    else if(['J','Q','K'].includes(rank)) total += 10;
    else total += parseInt(rank, 10);
  });
  while(total > 21 && aces > 0){ total -= 10; aces--; }
  return total;
}

export function shouldDealerHit(dealerHand, playerHand, difficulty, deck){
  const dVal = getHandValue(dealerHand);
  const pVal = getHandValue(playerHand);
  if(difficulty === 'easy') {
    return dVal < 17 && Math.random() < 0.5;
  }
  if(difficulty === 'hard') {
    const bustCount = deck.filter(c =>
      getHandValue([...dealerHand, c]) > 21
    ).length;
    const prob = bustCount / deck.length;
    return dVal < 17 && (dVal < pVal || prob < 0.4);
  }
  return dVal < 17; // medium
}

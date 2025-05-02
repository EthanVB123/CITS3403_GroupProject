document.querySelectorAll('.puzzle-card').forEach(card => {
    card.addEventListener('click', () => {
      console.log('Clicked puzzle ID:', card.dataset.puzzleId);
    });
  });
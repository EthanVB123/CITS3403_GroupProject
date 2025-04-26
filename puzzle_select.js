document.querySelectorAll('.puzzle-card').forEach(card => {
    card.addEventListener('click', () => {
      console.log('Clicked puzzle ID:', card.dataset.puzzleId);
    });
  });

document.querySelectorAll('.see-more, .back-button').forEach(btn => {
    btn.addEventListener('click', () => {
      window.location.href = btn.dataset.target;
    });
  });
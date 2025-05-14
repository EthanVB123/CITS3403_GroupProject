document.querySelectorAll('.puzzle-card').forEach(card => {
    card.addEventListener('click', () => {
      const puzzleId = card.dataset.puzzleId;
      window.location.href = `/puzzle/${puzzleId}`;
    });
  });
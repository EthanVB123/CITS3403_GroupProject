let puzzleSize = [5, 5]; // [rows, cols]
let rowClues = [[5],[1],[5],[1],[5]];
let colClues = [[3,1],[1,1,1],[1,1,1],[1,1,1],[1,3]];

document.addEventListener("DOMContentLoaded", () => {
    const puzzle = document.getElementById("puzzle");
    let cellIndex = 0;
    const cells = document.getElementsByClassName("cell");
    for(let cell of cells) {
        cell.id = `cell${cellIndex}`;
        cellIndex++;
    };

    puzzle.addEventListener("click", event => {
        const itemClicked = event.target;
        console.log(`Puzzle element ${itemClicked.id} clicked`);
    });
})
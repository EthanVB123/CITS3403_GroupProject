let puzzleSize = [5, 5]; // [rows, cols]
let rowClues = [[5],[1],[5],[1],[5]];
let colClues = [[3,1],[1,1,1],[1,1,1],[1,1,1],[1,3]];

let shadedCells = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
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
        const itemnum = parseInt(itemClicked.id.substr(4));
        const row = Math.trunc(itemnum/5);
        const col = itemnum % 5;
        if (shadedCells[row][col]) {
            shadedCells[row][col] = 0
        } else {
            shadedCells[row][col] = 1
        }
        itemClicked.classList.toggle("shaded");
    });
})
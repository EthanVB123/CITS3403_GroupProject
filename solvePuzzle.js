let puzzleSize = [5, 5]; // [rows, cols]
let rowClues = [[5],[1],[5],[1],[5]];
let colClues = [[3,1],[1,1,1],[1,1,1],[1,1,1],[1,3]];

let shadedCells = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]

// set up event listeners after DOM has loaded
document.addEventListener("DOMContentLoaded", () => {
    const puzzle = document.getElementById("puzzle");
    let cellIndex = 0;
    const cells = document.getElementsByClassName("cell");
    for(let cell of cells) {
        cell.id = `cell${cellIndex}`;
        cellIndex++;
    };
    // to prevent bloat from having an event listener per cell, just have an event listener for the puzzle 
    // and then detect which item was actually clicked using event.target
    puzzle.addEventListener("click", event => {
        const itemClicked = event.target;
        //console.log(`Puzzle element ${itemClicked.id} clicked`);
        const itemnum = parseInt(itemClicked.id.substr(4));
        const row = Math.trunc(itemnum/5);
        const col = itemnum % 5;
        if (shadedCells[row][col]) {
            shadedCells[row][col] = 0
        } else {
            shadedCells[row][col] = 1
        }
        itemClicked.classList.toggle("shaded");
        if (verifySolution(rowClues, colClues, shadedCells)) {
            console.log("Woo hoo! Puzzle completed!")
        }
    });
})

// Takes input 1d array containing 1s for shaded and 0s for unshaded cells and returns the clue required to generate that pattern
// E.g. Input = [1,1,0,1,0,0,1,1,1,1] has Output = [2, 1, 4]
// Note that [0] is output for empty rows and not [] 
function findClueForLine(line) {
    let clues = [];
    let currentClue = 0;
    for (let cell of line) {
        if (cell) {
            currentClue++;
        } else if (currentClue) {
            clues.push(currentClue);
            currentClue = 0;
        }
    }
    if (currentClue) {
        clues.push(currentClue);
    }
    if (clues.length == 0) {
        return [0]; // instead of empty array, there is a single zero clue
    }
    return clues;
}

// checks to see if two arrays have the same elements in the same order
// required as default array == comparison checks if they are the same object, not their actual elements
function ArraysEqual(arrayA, arrayB) {
    if (arrayA.length != arrayB.length) {
        return false;
    }
    return arrayA.every((element, index) => element == arrayB[index]);
}

// Returns true if pattern created by shadedCells matches rowClues and colClues, false otherwise
function verifySolution(rowClues, colClues, shadedCells) {
    // check rows
    const rowCorrectness = rowClues.every((clue, index) => ArraysEqual(clue, findClueForLine(shadedCells[index])));

    // chatgpt boilerplate code
    shadedCellsTranspose = shadedCells[0].map((_, colIndex) =>
        shadedCells.map(row => row[colIndex])
    );

    // check cols
    const colCorrectness = colClues.every((clue, index) => ArraysEqual(clue, findClueForLine(shadedCellsTranspose[index])));
      
    return rowCorrectness && colCorrectness;
}
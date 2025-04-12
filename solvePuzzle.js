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

    generatePuzzle(puzzleSize, rowClues, colClues);
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
        itemClicked.classList.toggle("hover:bg-zinc-600");
        itemClicked.classList.toggle("bg-zinc-900")
        if (verifySolution(rowClues, colClues, shadedCells)) {
            console.log("Woo hoo! Puzzle completed!")
        }
    });
})

// The following code generates the puzzle in the DOM
function generatePuzzle(size, newRowClues, newColClues) {
    puzzleElement = document.getElementById("puzzle");
    // empty out the existing puzzle
    puzzleElement.innerHTML = "";
    // add the corner element
    cornerElement = document.createElement("div");
    cornerElement.classList.add("topleftbox");
    puzzleElement.appendChild(cornerElement);
    // add the vertical clues
    for (let colnum = 0; colnum < size[1]; colnum++) {
        colElement = document.createElement('div');
        colElement.classList.add("column", "border", "border-zinc-400");
        for (let clue of newColClues[colnum]) {
            clueElement = document.createElement('div');
            clueElement.classList.add("vclue");
            clueElement.classList.add("bg-rose-200");
            clueElement.classList.add("m-0.5", "rounded-lg", "text-4xl");
            clueElement.classList.add("flex", "items-center", "justify-center");
            clueElement.innerHTML = clue;
            colElement.appendChild(clueElement);
        }
        puzzle.appendChild(colElement);
    }
    // add each row
    for (let rownum = 0; rownum < size[0]; rownum++) {
        // add row clue
        rowElement = document.createElement('div');
        rowElement.classList.add("row", "border", "border-zinc-400");
        for (let clue of newRowClues[rownum]) {
            clueElement = document.createElement('div');
            clueElement.classList.add("hclue");
            clueElement.classList.add("bg-rose-200");
            clueElement.classList.add("m-0.5", "rounded-lg", "text-4xl");
            clueElement.classList.add("flex", "items-center", "justify-center");
            clueElement.innerHTML = clue;
            rowElement.appendChild(clueElement);
        }
        puzzle.appendChild(rowElement);
        // add cells
        for (let i = 0; i < size[1]; i++) {
            cell = document.createElement("div");
            cell.classList.add("cell");
            cell.classList.add("border-zinc-400");
            cell.classList.add("border");
            cell.classList.add("hover:bg-zinc-200");
            puzzle.appendChild(cell);
        }
    }

    // assign IDs to cells
    let cellIndex = 0;
    const cells = document.getElementsByClassName("cell");
    for(let cell of cells) {
        cell.id = `cell${cellIndex}`;
        cellIndex++;
    };

    // update global row and col clues and shaded cells to reset the verifier
    rowClues = newRowClues;
    colClues = newColClues;
    shadedCells = Array.from({ length: size[0]}, () => Array(size[1]).fill(0));
}


// The following code is the solution verifier

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
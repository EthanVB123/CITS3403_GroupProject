let puzzleSize = [5, 5]; // [rows, cols]
let rowClues = [[5],[1],[5],[1],[5]];
let colClues = [[3,1],[1,1,1],[1,1,1],[1,1,1],[1,3]];
let startTime = Date.now();
let shadedCells = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
let timerInterval; // defined when puzzle made, but needs to be global
let progressElement; // defined when dom loaded, this element displays updates like % puzzle completion, and if puzzle complete, whether or not there are mistakes
let userStatus = "solver"; // "solver" if trying to solve the puzzle, "editor" if trying to make their own
// set up event listeners after DOM has loaded
document.addEventListener("DOMContentLoaded", () => {
    console.log(requestedPuzzle)
    const puzzle = document.getElementById("puzzle");
    const timerElement = document.getElementById("timer");
    progressElement = document.getElementById("progress");

    if (requestedPuzzle.role == "solver") {
        generatePuzzle(requestedPuzzle.puzzleSize, requestedPuzzle.rowClues, requestedPuzzle.columnClues); // defined inline in solvePuzzle.html
    } else if (requestedPuzzle.role == "editor") {
        initialiseEditorMode(requestedPuzzle.puzzleSize);
    }
    // to prevent bloat from having an event listener per cell, just have an event listener for the puzzle 
    // and then detect which item was actually clicked using event.target
    puzzle.addEventListener("click", event => {
        const itemClicked = event.target;
        //console.log(`Puzzle element ${itemClicked.id} clicked`);
        const itemnum = parseInt(itemClicked.id.substr(4));

        const row = Math.trunc(itemnum/puzzleSize[1]);
        const col = itemnum % puzzleSize[1];
        if (shadedCells[row][col]) {
            shadedCells[row][col] = 0
        } else {
            shadedCells[row][col] = 1
        }
        itemClicked.classList.toggle("shaded");
        itemClicked.classList.toggle("hover:bg-zinc-600");
        itemClicked.classList.toggle("bg-zinc-200");
        if (userStatus == "solver") {
            displayProgress(progressElement);
            if (verifySolution(rowClues, colClues, shadedCells)) {
                console.log("Woo hoo! Puzzle completed!");
                clearInterval(timerInterval);
            }
        } else if (userStatus == "editor") {
            updatePuzzleClues(itemnum);
        }
    });


    let timerInterval = setInterval(displayTime, 200, timerElement);
})

// This function makes the text inside a HTML element the largest size it can be (capping at font-6xl) without overflow
// Required as overflow (which could happen as the box size shrinks as puzzle size grows) could cause the puzzle size to exceed the 80% of screen height it is permitted
// note this function is adapted from chatgpt code
function maximiseFontSize(element) {
    const tailwindSizes = ["text-xs","text-sm","text-base","text-lg","text-xl","text-2xl","text-3xl","text-4xl","text-5xl","text-6xl"];
    const maxWidth = element.clientWidth; // if actual width exceeds this, we get overflow
    const maxHeight = element.clientHeight; // if actual height exceeds this, we get overflow

    let bestFontSize = tailwindSizes[0];
    for (let size of tailwindSizes) {
        element.classList.remove(...tailwindSizes); // easier to just remove every size in case of off by 1 error
        element.classList.add(size); // try the next largest size
        // accept the next largest size if it can fit and keeps iterating, otherwise ends process with current size
        if (element.scrollWidth > maxWidth || element.scrollHeight > maxHeight) { // scrollWidth and scrollHeight are actual width and height used
            break;
        } else {
            bestFontSize = size;
        }
    }
    // makes sure we have the right size equipped
    element.classList.remove(...tailwindSizes);
    element.classList.add(bestFontSize);
}
// calls maximiseFontSize on every clue element
function maximiseAllFontSizes() {
    const horizontalClues = document.getElementsByClassName("hclue");
    const verticalClues = document.getElementsByClassName("vclue");
    for (clue of horizontalClues) {
        maximiseFontSize(clue);
    }
    for (clue of verticalClues) {
        maximiseFontSize(clue);
    }
}
// The following code manages the dynamic elements on the sidebar

// This sets the innerHTML of the timer element to be "mm:ss" since generatePuzzle last called
// if over 60 mins, stops timer at 60:00
// maybe later implement hours with dynamic font size
function displayTime(timerElement) {
    const timeElapsedMs = Date.now() - startTime; // time in milliseconds since generatePuzzle last called
    const secondsTotal = Math.trunc((timeElapsedMs - (timeElapsedMs % 1000)) / 1000); // as above, rounded *down* to nearest second (00:00.9 rounds to 00:00)
    const secondsDisplayed = secondsTotal % 60;
    const minutesTotal = Math.trunc((secondsTotal-secondsDisplayed)/60);
    const minutesDisplayed = minutesTotal % 60;
    const hours = Math.trunc((minutesTotal - minutesDisplayed)/60);
    if (userStatus == "editor") {
        timerElement.innerHTML = "xx:xx"; // timer not required when editing puzzle
    } else if (hours > 0) {
        //timerElement.innerHTML = `${hours}:${String(minutesDisplayed).padStart(2, '0')}:${String(secondsDisplayed).padStart(2, '0')}`; // h:mm:ss with h being as many digits as needed
        timerElement.innerHTML = "60:00"; // temporary remedy until dynamic font sizing fixed.
    } else {
        timerElement.innerHTML = `${String(minutesDisplayed).padStart(2, '0')}:${String(secondsDisplayed).padStart(2, '0')}`; // mm:ss
    }
}

// This manages the text and colour of the progress text on the sidebar
function displayProgress(progressElement) {
    const cells = document.getElementsByClassName("cell");
    const totalCells = puzzleSize[0]*puzzleSize[1];
    let filledCells = 0; // this will increase as the cells are iterated through

    for (let cell of cells) {
        if (cell.classList.contains("shaded")) {
            filledCells++;
        }
    }    
    if (userStatus == "editor") {
        progressElement.innerHTML = "Currently in editor mode."
    } else if (verifySolution(rowClues, colClues, shadedCells)) {
        progressElement.innerHTML = "Puzzle solved!"
    } else if (filledCells < totalCells) {
        progressElement.innerHTML = `Progress ${filledCells}/${totalCells} (${Math.trunc(filledCells*100/totalCells)}%)`
    } else {
        progressElement.innerHTML = "Mistakes Found"
    }
}

// The following code generates the puzzle in the DOM
function generatePuzzle(newSize, newRowClues, newColClues) {
    puzzleElement = document.getElementById("puzzle");
    // empty out the existing puzzle, change the size of the grid to the new size
    puzzleElement.innerHTML = "";
    // note that grid-template-rows is converted to camelCase in JS in next 2 lines as JS can't have attributes with hyphens
    puzzleElement.style.display = "grid";
    puzzleElement.style.gridTemplateRows = gridTemplate(newSize[0], "puzzle");
    puzzleElement.style.gridTemplateColumns = gridTemplate(newSize[1], "puzzle");
    // add the corner element
    cornerElement = document.createElement("div");
    cornerElement.classList.add("topleftbox");
    puzzleElement.appendChild(cornerElement);
    // add the vertical clues (the elements in each column containing the clues (list of numbers) for that column)
    for (let colnum = 0; colnum < newSize[1]; colnum++) {
        colElement = document.createElement('div');
        colElement.classList.add("column", "border", "border-white");
        colElement.style.display = "grid";
        colElement.style.gridTemplateRows = gridTemplate(newSize[0], "col"); // note that newsize[0] is used here as the max number of clues in a *column* is ceil(*numRows*/2)
        colElement.style.gridTemplateColumns = '1fr';
        for (let clue of newColClues[colnum]) { // Add each individual clue number into the 'column' element
            clueElement = document.createElement('div');
            clueElement.classList.add("vclue");
            clueElement.classList.add("bg-zinc-200");
            clueElement.classList.add("text-black");
            clueElement.classList.add("m-0.5", "rounded-lg");
            clueElement.classList.add("flex", "items-center", "justify-center");
            clueElement.innerHTML = clue;
            colElement.appendChild(clueElement);
        }
        puzzle.appendChild(colElement);
    }
    // add each row 
    for (let rownum = 0; rownum < newSize[0]; rownum++) {
        // add row clue (the element in the row containing the clue (list of numbers) for that row)
        rowElement = document.createElement('div');
        rowElement.classList.add("row", "border", "border-white");
        rowElement.style.display = "grid";
        rowElement.style.gridTemplateColumns = gridTemplate(newSize[1], "row"); // note that newsize[1] is used here as the max number of clues in a *row* is ceil(*numCols*/2)
        rowElement.style.gridTemplateRows = '1fr';
        for (let clue of newRowClues[rownum]) { // Add each individual clue number into the 'row' element
            clueElement = document.createElement('div');
            clueElement.classList.add("hclue");
            clueElement.classList.add("bg-zinc-200");
            clueElement.classList.add("text-black");
            clueElement.classList.add("m-0.5", "rounded-lg");
            clueElement.classList.add("flex", "items-center", "justify-center");
            clueElement.innerHTML = clue;
            rowElement.appendChild(clueElement);
        }
        puzzle.appendChild(rowElement);
        // add cells
        for (let i = 0; i < newSize[1]; i++) {
            cell = document.createElement("div");
            cell.classList.add("cell");
            cell.classList.add("border-white");
            cell.classList.add("border");
            cell.classList.add("hover:bg-zinc-600");
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

    // fix font size to prevent overflow
    maximiseAllFontSizes();
    // update global row and col clues and shaded cells to reset the verifier
    rowClues = newRowClues;
    colClues = newColClues;
    puzzleSize = newSize;
    shadedCells = Array.from({ length: puzzleSize[0]}, () => Array(puzzleSize[1]).fill(0));
    // Resets timer
    startTime = Date.now();
    // Resets progress bar indicator
    displayProgress(progressElement);
}

// Generates a string to be grid-template-rows or grid-template-columns based on dimension
// e.g. input 5 gives output "3fr 1fr 1fr 1fr 1fr 1fr", where the 3fr is for the clues and the 1fr is for each cell
function gridTemplate(size, category) {
    const maxPossibleCluesPerCol = Math.ceil(size / 2);
    switch (category) {
        case "puzzle":
            return `${maxPossibleCluesPerCol}fr${" 1fr".repeat(size)}`;
            break;
        case "row":
        case "col":
            return `${"1fr ".repeat(maxPossibleCluesPerCol)}`.trim();
            break;
        default:
            console.error(`Unexpected category given to gridTemplate: ${category}`)
            break; // this default should never be called, this is a just in case
    }
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
    const shadedCellsTranspose = shadedCells[0].map((_, colIndex) =>
        shadedCells.map(row => row[colIndex])
    );

    // check cols
    const colCorrectness = colClues.every((clue, index) => ArraysEqual(clue, findClueForLine(shadedCellsTranspose[index])));
      
    return rowCorrectness && colCorrectness;
}

// The following code refers to the puzzle editor

// this function updates the clue numbers for a single row/column with the correct clues to match what is *currently* in shadedCells
// it changes graphics only, not rowClues or colClues
// isColumn is a bool indicating column (if true) or row (if false), index is col # or row #
function updateClue(index, isColumn) {
    const shadedCellsTranspose = shadedCells[0].map((_, colIndex) =>
        shadedCells.map(row => row[colIndex])
    ); // could be possible to store shadedCellsTranspose in memory as well as shadedCells so this doesn't have to be called every time

    let targetLine;
    let targetElement;
    if (isColumn) {
        targetLine = shadedCellsTranspose[index]; // this stores an array of 0s and 1s, where 1 is shaded and 0 isn't
        targetElement = document.getElementsByClassName("column")[index];
    } else {
        targetLine = shadedCells[index];
        targetElement = document.getElementsByClassName("row")[index];
    }

    const newClues = findClueForLine(targetLine);
    targetElement.innerHTML = "";
    for (clue of newClues) {
        clueElement = document.createElement('div');
        clueElement.classList.add("hclue");
        clueElement.classList.add("bg-rose-200");
        clueElement.classList.add("m-0.5", "rounded-lg");
        clueElement.classList.add("flex", "items-center", "justify-center");
        clueElement.innerHTML = clue;
        targetElement.appendChild(clueElement); // this is a repeat of generatePuzzle, make it its own function?
    }

    maximiseAllFontSizes(); // TODO optimise this, it is the bottleneck on speed here (in 5x5 puzzle takes ~100ms, fast but noticeable)
}

// updates clues in puzzle after user changes the puzzle
function updatePuzzleClues(cellClicked) { // cell clicked is the integer in the cell id, so if we clicked cell "cell24", cellClicked is 24
    const row = Math.trunc(cellClicked/puzzleSize[1]);
    const col = cellClicked % puzzleSize[1];

    updateClue(row, false);
    updateClue(col, true);
}

// Exports puzzle as a list with elements [puzzleSize, rowClues, colClues], which could be made into JSON later for the server
// puzzleSize is Array(2) [#rows, #cols]
// rowClues and colClues are arrays with one element for each row/col, and each of those elements are variable-sized arrays of integers for the individual clue numbers
function exportPuzzle() {
    const shadedCellsTranspose = shadedCells[0].map((_, colIndex) =>
        shadedCells.map(row => row[colIndex])
    );
    const exportRowClues = shadedCells.map(findClueForLine);
    const exportColClues = shadedCellsTranspose.map(findClueForLine);

    // return [puzzleSize, exportRowClues, exportColClues];

    fetch('/submit-puzzle', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({puzzleSize: puzzleSize,
            colClues: exportColClues,
            rowClues: exportRowClues,
            puzzleName: requestedPuzzle.puzzleName
        })
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;  // Manually follow the redirect
        }
    })
}

// Submits a solved puzzle to give the user their points.
function submitPuzzle() {
    // client-side validation done here (there is also server-side validation)
    if (verifySolution(rowClues, colClues, shadedCells)) {
        fetch('/register-solved-puzzle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({puzzleSize: puzzleSize,
                puzzleId: requestedPuzzle.puzzleid,
                userId: 1,
                accuracy: Math.floor(Math.random() * 100) + 1,
                shadedCells: shadedCells
            })
        }).then(response => {
            if (response.ok) {
                window.location.href = response.redirect_url;  // Manually follow the redirect
            }
        })
    }
}


// Initialises puzzle editor mode, initialising a blank puzzle of given size [rows, cols]
function initialiseEditorMode(newPuzzleSize) {
    userStatus = "editor";
    let newRows = new Array(newPuzzleSize[0]).fill(0);
    newRows = Array.from(newRows, () => [0])
    let newCols = new Array(newPuzzleSize[1]).fill(0);
    newCols = Array.from(newCols, () => [0])
    generatePuzzle(newPuzzleSize, newRows, newCols);
}
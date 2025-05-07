# This function takes a row/column of cells (1s meaning shaded and 0s meaning nonshaded) and returns the clues required for this row to be correct
# e.g. [0,1,1,0,0,0,1,0,1] returns [2,1,1]
def generateClues(shadedArray):
    output = []
    currentShadedLength = 0
    # iterate through the array and generate the output list (this is efficient as len(shadedArray) <= 20)
    for clue in shadedArray:
        if clue == 1:
            currentShadedLength += 1
        else:
            if currentShadedLength > 0:
                output.append(currentShadedLength)
                currentShadedLength = 0
    if currentShadedLength > 0:
        output.append(currentShadedLength)
    if len(output) == 0:
        return [0] # instead of []
    return output


# This function takes the row clues and col clues of the puzzle and the user's answer
# and returns True if correctly solved and False otherwise
def verifySolution(rowClues, colClues, shadedCells):
    # Check that dimension size matches to prevent malformed data from being submitted and causing an error
    if len(shadedCells) < 1 or len(rowClues) != len(shadedCells) or len(colClues) != len(shadedCells[0]):
        print("Submitted puzzle is of invalid size.")
        return False
    
    # Check row clues match solution
    for rowIndex in range(len(rowClues)):
        if not (rowClues[rowIndex] == generateClues(shadedCells[rowIndex])):
            # a row is incorrect
            return False
    
    # Check column clues match solution
    transposedCells = [list(row) for row in zip(*shadedCells)]
    for colIndex in range(len(colClues)):
        if not (colClues[colIndex] == generateClues(transposedCells[colIndex])):
            # a column is incorrect
            return False
    
    return True
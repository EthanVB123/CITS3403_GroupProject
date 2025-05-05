
# This function takes the row clues and col clues of the puzzle and the user's answer
# and returns True if correctly solved and False otherwise
def verifySolution(rowClues, colClues, shadedCells):
    # Check that dimension size matches to prevent malformed data from being submitted and causing an error
    if len(shadedCells) < 1 or len(rowClues) != len(shadedCells) or len(colClues) != len(shadedCells[0]):
        print("Submitted puzzle is of invalid size.")
        return False
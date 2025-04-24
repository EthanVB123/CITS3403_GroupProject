import json # in standard library

def getPuzzleAsJSON(id: int):
    samplePuzzles = [ [[2,2],[[1],[1]],[[1],[1]]], [[3,3],[[1],[1],[1]],[[1],[1],[1]]] ]
    jsonAttributeNames = ["puzzleSize", "rowClues", "columnClues"]
    samplePuzzlesDicts = [dict(zip(jsonAttributeNames, puzzle)) for puzzle in samplePuzzles]
    targetPuzzle = samplePuzzlesDicts[id]
    print(json.dumps(targetPuzzle))
    return json.dumps(targetPuzzle)

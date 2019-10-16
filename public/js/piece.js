const CHESS_VALUE = {
    'p' : 10,
    'r' : 50,
    'n' : 30,
    'b' : 30,
    'q' : 90,
    'k' : 900
}

function getAbsolutedValue(type) {
    // console.log("piece type ", type)
    if (!CHESS_VALUE.hasOwnProperty(type))
        return 0

    // console.log("piece value ", CHESS_VALUE[type])
    return CHESS_VALUE[type]
}

function getPieceValue(piece){
    if(piece == null){
        return 0;
    }
    const absValue = getAbsolutedValue(piece.type)
    // console.log("piece color ", piece.color)
    return piece.color === 'w' ? absValue : -absValue
}

function evaluateBoard(board){
    let total = 0;
    for (let i = 0; i < 8; i++){
        for (let j = 0; j < 8; j++ ) {
            total += getPieceValue(board[i][j])
        }
    }

    return total
}
function miniMax(depth, game, isMaximissingPlayer){
	if (depth === 0){
        // console.log("last node: ", evaluateBoard(game.board()))
		return (-1) * evaluateBoard(game.board())
    }
    
    const gameMoves = game.moves()

	if(isMaximissingPlayer){
		let bestMoveValue = -99999
		for (let i = 0; i < gameMoves.length; i++){
			game.move(gameMoves[i])
			bestMoveValue = Math.max(bestMoveValue, miniMax(depth - 1, game, !isMaximissingPlayer))
			game.undo()
		}
		return bestMoveValue
    }
    else {
        let bestMoveValue = 99999
        for (let i = 0; i < gameMoves.length; i++){
            game.move(gameMoves[i])
            bestMoveValue = Math.min(bestMoveValue, miniMax(depth - 1, game, !isMaximissingPlayer))
            game.undo()
        }
        return bestMoveValue
    }
}

function nextMove(depth, game, isMaximissingPlayer){
	let bestMove = null
	let bestMoveValue = -99999

	const gameMoves = game.moves()
	for (let i = 0; i < gameMoves.length; i++){
		game.move(gameMoves[i])
        let predictValue = miniMax(depth - 1, game, !isMaximissingPlayer)
		if (predictValue >= bestMoveValue){
			bestMoveValue = predictValue
			bestMove = gameMoves[i]
		}
		game.undo()
	}
	
	return bestMove
}
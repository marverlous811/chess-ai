const defaultBestValue = 9999
const defaultAlpha = -10000
const defaultBeta = 10000

function miniMax(depth, game, alpha, beta, isMaximissingPlayer){
	if (depth === 0){
        // console.log("last node: ", evaluateBoard(game.board()))
		return (-1) * evaluateBoard(game.board())
    }
    
    const gameMoves = game.moves()

	if(isMaximissingPlayer){
		let bestMoveValue = (-1) * defaultBestValue
		for (let i = 0; i < gameMoves.length; i++){
			game.move(gameMoves[i])
			bestMoveValue = Math.max(bestMoveValue, miniMax(depth - 1, game, !isMaximissingPlayer))
            game.undo()
            alpha = Math.max(alpha, bestMoveValue);
            if (beta <= alpha) {
                return bestMoveValue;
            }
		}
		return bestMoveValue
    }
    else {
        let bestMoveValue = defaultBestValue
        for (let i = 0; i < gameMoves.length; i++){
            game.move(gameMoves[i])
            bestMoveValue = Math.min(bestMoveValue, miniMax(depth - 1, game, !isMaximissingPlayer))
            game.undo()
            beta = Math.min(beta, bestMoveValue);
            if (beta <= alpha) {
                return bestMoveValue;
            }
        }
        return bestMoveValue
    }
}

function nextMove(depth, game, isMaximissingPlayer){
	let bestMove = null
	let bestMoveValue = -defaultBestValue

	const gameMoves = game.moves()
	for (let i = 0; i < gameMoves.length; i++){
		game.move(gameMoves[i])
        let predictValue = miniMax(depth - 1, game, defaultAlpha, defaultBeta , !isMaximissingPlayer)
		if (predictValue >= bestMoveValue){
			bestMoveValue = predictValue
			bestMove = gameMoves[i]
		}
		game.undo()
	}
	
	return bestMove
}
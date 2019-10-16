class ChessBot {
    constructor(game, board, type){
        this.game = game
        this.board = board
        this.type = type
        this.timeThinking = []

        console.log("bot type...",type)
    }

    makeBestMove = () => {

        const start = Date.now()
        let bestMove = this.getBestMove(this.game)
        const end = Date.now()
        const d = end - start
        this.timeThinking.push(d)
        
        renderForAI(bestMove, d)
        this.game.move(bestMove)
        this.board.position(this.game.fen())
        if (this.game.game_over()){
            console.log("game over ", this.timeThinking)
        }
    }

    getBestMove = (game) => {
        if (game.game_over()) {
            alert('Game over');
        }
        return this.calculateBestMove(game);
    }

    calculateBestMove = (game) =>{
        const type = this.type
        switch(type){
            case 'point':
                return this.calculateByPoint(game)
            case 'minimax':
                return this.calculateByMinMax(game)
            default: 
                return game.moves()[Math.floor(Math.random() * game.moves().length)]
        }
    }

    calculateByPoint = (game) => {
        let newGameMoves = game.moves();
        let bestMove = null
        let bestValue = -999999

        for (let i = 0; i < newGameMoves.length; i++){
            const tempMove = newGameMoves[i]
            game.move(tempMove)

            let boardValue = (-1) * evaluateBoard(game.board())
            game.undo()
            if (boardValue > bestValue) {
                bestValue = boardValue
                bestMove = tempMove
            }
        }

        //newGameMoves[Math.floor(Math.random() * newGameMoves.length)] random move
        console.log("best value of move: ", bestValue)
        return bestMove;
    }

    calculateByMinMax = (game) => {
        let bestMove = nextMove(3, game, true)
        console.log("best move: ", bestMove)
        return bestMove
    }
}
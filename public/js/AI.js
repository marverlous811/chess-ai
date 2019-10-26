class ChessBot {
    constructor(listener, type){
        this.game = listener.game
        this.board = listener.board
        this.type = type
        this.timeThinking = []

        console.log("bot type...",type)
    }

    changeSide = (side) => {
        this.side = side !== -1 ? true : false
    }

    getBestMove = () => {
        if (this.game.game_over()) {
            alert('Game over');
            return
        }
        const begin = Date.now()
        const move = this.calculateBestMove(this.game);
        const end = Date.now()
        this.timeThinking.push((end - begin))
        renderForAI((end - begin))
        this.game.move(move)
        return this.game.fen()
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

            let boardValue = this.side ? (-1) * evaluateBoard(game.board()) : evaluateBoard(game.board())
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
        let bestMove = nextMove(3, game, this.side)
        console.log("best move: ", bestMove)
        return bestMove
    }
}
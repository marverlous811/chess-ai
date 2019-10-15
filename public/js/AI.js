class ChessBot {
    constructor(game, board){
        this.game = game
        this.board = board
    }

    makeBestMove = () => {
        let bestMove = this.getBestMove(this.game)
        this.game.move(bestMove)
        this.board.position(this.game.fen())
        if (this.game.game_over()){
            console.log("game over")
        }
    }

    getBestMove = (game) => {
        if (game.game_over()) {
            alert('Game over');
        }
        return this.calculateBestMove(game);
    }

    calculateBestMove = (game) => {
        let newGameMoves = game.moves();

        return newGameMoves[Math.floor(Math.random() * newGameMoves.length)];
    }
}
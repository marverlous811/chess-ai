class ChessBoard{
    constructor(boardDivID, AI){
        this.config = {
            draggable: true,    
            position: 'start',
            onMoveEnd: this.onMoveEnd,
            onDragStart: this.onDragStart,
            onDrop: this.onDrop,
            onSnapEnd: this.onSnapEnd,
        }
        this.boardID = boardDivID
        this.board = Chessboard(this.boardID)
        this.game =  new Chess()
        this.AI = AI
        this.humanSide = -1
        this.nowSide = -1
        this.started = false
    }

    changeSide = (value) => {
        this.AI.changeSide(this.humanSide)
        this.humanSide = value
        if(this.started){
            setTimeout(() => {
                this.makeBestMove()
            }, 500)
        }
    }

    start = () => {
        this.board = Chessboard(this.boardID, this.config)
        this.started = true
        if(this.humanSide !== -1){
            setTimeout(() => {
                this.makeBestMove()
            }, 500)
        }
    }

    onMoveEnd = (oldPos, newPos) => {
        if(this.game.game_over() === true) {
            console.log("game over")
        }

        console.log(this.game.fen())
    }

    onDragStart = (source, piece, position, orientation) => {
        console.log(piece.search(/^b/), piece.search(/^b/) === this.humanSide)
        if(this.game.game_over() === true || !(piece.search(/^b/) === this.humanSide)) {
            return false
        }
    }

    onSnapEnd = () => {
        this.board.position(this.game.fen());
    };

    onDrop = (source, target) => {
        let move = this.game.move({
            from: source,
            to: target,
            promotion: 'q' // NOTE: always promote to a queen for example simplicity
        });

        // If illegal move, snapback
        if (move === null) return 'snapback';

        // Log the move
        console.log(move)
        console.log(this.board.position(this.game.fen()))
        renderForHuman(this.game.history())
        setTimeout(() => {
            if(this.AI) {
                this.makeBestMove()
            }
        }, 500)
    }

    makeBestMove = () => {
        const start = Date.now()
        let bestMove = this.AI.getBestMove(this.game)
        console.log(bestMove)
        const end = Date.now()
        const d = end - start
        
        renderForAI(bestMove, d)
        this.game.move(bestMove)
        this.board.position(this.game.fen())
        if (this.game.game_over()){
            console.log("game over ", this.timeThinking)
        }
    }
}
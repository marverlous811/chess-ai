const SIDE = {
    "WHITE": -1,
    "BLACK": 0
}

class ChessManager{
    constructor(boardDivID){
        this.config = {
            draggable: true,    
            position: 'start',
            onMoveEnd: this.onMoveEnd,
            onDragStart: this.onDragStart,
            onDrop: this.onDrop,
            onSnapEnd: this.onSnapEnd,
        }
        this.divID = boardDivID
        this.board = ChessBoard(this.divID)
        this.game = new Chess()
        this.human = SIDE.WHITE
        this.AISide = SIDE.BLACK
        this.nowSide = SIDE.WHITE
        this.started = false
    }

    setAI = (AI) => {
        this.AI = AI
        this.AI.changeSide(this.AISide)
    }

    start = () =>{
        removeHistory()
        this.board = Chessboard(this.divID, this.config)
        this.started = true
        if(this.human !== -1){
            setTimeout(() => {
                this.AIMove()
            }, 500)
        }

    }

    changeSide = (value) => {
        if(this.AI){
            this.AI.changeSide(this.human)
            setTimeout(() => {
                this.AIMove()
            }, 500)
        }
        this.human = SIDE[value.toUpperCase()]
        console.log("changed side ", this.human)
    }

    onMoveEnd = (oldPos, newPos) => {
        if(this.game.game_over() === true) {
            console.log("game over")
        }

        console.log(this.game.fen())
    }

    onDragStart = (source, piece, position, orientation) => {
        console.log(piece.search(/^b/), piece.search(/^b/) === this.human)
        if(this.game.game_over() === true || !(piece.search(/^b/) === this.human)) {
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
     
        console.log(move)
        this.renderMove()
        this.nowSide = this.AISide
        setTimeout(() => {
            if(this.AI) this.AIMove()
        })
    }

    AIMove = async () =>{
        let bestMove = await this.AI.getBestMove()
        console.log("AI: move", bestMove)
        if(!bestMove) return
        this.board.position(bestMove)

        this.renderMove()
        this.nowSide = this.human
        if (this.game.game_over()){
            console.log("game over")
        }
    }

    renderMove = () => {
        const moves = this.game.history()
        console.log(moves)
        const side = this.nowSide === SIDE.WHITE ? "white" : "black"
        renderMoveHistory(moves[moves.length - 1], side)
    }

}
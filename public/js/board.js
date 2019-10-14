class ChessBoard{
    constructor(){
        this.config = {
            draggable: true,    
            position: 'start',
        }
        this.board = Chessboard('myBoard', this.config)
    }
}

window.board = new ChessBoard()
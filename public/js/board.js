class ChessBoard{
    constructor(boardDivID){
        this.config = {
            draggable: true,    
            position: 'start',
            onMoveEnd: this.onMoveEnd,
            onDragStart: this.onDragStart,
            onDrop: this.onDrop,
            onSnapEnd: this.onSnapEnd,
        }
        this.board = Chessboard(boardDivID, this.config)
        this.game =  new Chess()
    }

    onMoveEnd = (oldPos, newPos) => {
        if(this.game.game_over() === true) {
            console.log("game over")
        }

        console.log(this.game.fen())
    }

    onDragStart = (source, piece, position, orientation) => {
        if(this.game.game_over() === true || piece.search(/^b/) !== -1) {
            return false
        }
    }

    onSnapEnd = () => {
        this.board.position(this.game.fen());
    };

    onDrop = (source, target) => {
        var move = this.game.move({
            from: source,
            to: target,
            promotion: 'q' // NOTE: always promote to a queen for example simplicity
        });

        // If illegal move, snapback
        if (move === null) return 'snapback';

        // Log the move
        console.log(move)
    }
}

window.board = new ChessBoard('myBoard')
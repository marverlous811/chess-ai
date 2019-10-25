const dumbAI = new ChessBot(this.game, this.board, 'minimax', 0)
window.board = new ChessBoard('myBoard', dumbAI)
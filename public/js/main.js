window.board = new ChessManager('myBoard')
const dumbAI = new ChessBot(board, 'minimax')
const nnBot = new NeuralBot(board)
board.setAI(nnBot)
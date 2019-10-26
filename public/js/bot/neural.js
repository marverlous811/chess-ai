const ws = "127.0.0.1:5000"

class NeuralBot{
    constructor(listener){
        this.game = listener.game
        this.timeThinking = []
        this.socket = new WebSocket(`ws://${ws}`)
        this.socket.onopen = this.onOpen
        this.socket.onmessage = this.onMessage
        this.timeThinking = []
    }

    changeSide = (side) => {
        return
    }

    onOpen = () => {
        console.log("websocket Connected")
    }

    onMessage = (e) => {
        console.log(e)
        this.onData(e.data)
    }

    send = (data) => {
        this.socket.send(JSON.stringify(data))
    }

    onData = (data) => {
        if(this.callback) {
            this.callback(data)
        }
    }

    getBestMove = async () => {
        return new Promise(resolve => {
            if (this.game.game_over()){
                alert("Game Over")
                resolve()
            }
            const begin = Date.now()
            this.send({"type": "getMove", "board": this.game.fen()})
            const callback = (data) => {
                this.callback = null
                data = data.slice(0, -1)
                const end = Date.now()
                this.timeThinking.push(end - begin)
                renderForAI((end - begin))
                this.game.load(data)
                resolve(data)
            }
            this.callback = callback
        })

        
    }

}
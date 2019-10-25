const WebsocketServer = require('ws').Server
const HttpServer = require('./server')

class Socket{
    constructor(port){
        this.port = port
        this.server = new HttpServer(port)
        this.listConnection = []
    }

    async start(){
        await this.server.start()
        this.ws = new WebsocketServer({server: this.server.getInstance()})

        this.ws.on('connection', this.onConnection.bind(this) )
    }

    onConnection(ws, req){
        // console.log("onConnection ", req)
        const index = this.listConnection.length
        const client = new SocketClient(ws, index, this)
        this.listConnection.push(client)
    }

    onClose(cliIndex){
        this.listConnection = this.listConnection.filter((value, index) => {
            return index !== cliIndex
        })
        this.listConnection.map((value, index) => {
            value.setIndex(index)
        })
        console.log("onConnectionClose: ", this.listConnection)
    }
}

class SocketClient{
    constructor(socket, index, listener){
        this.socket = socket
        this.index = index
        this.listener = listener

        this.socket.on('close', this.onClose.bind(this))
        this.socket.on('message', this.onMessage.bind(this))
    }

    setIndex(index){
        this.index = index
    }

    onClose(){
        if(this.listener){
            this.listener.onClose(this.index)
        }
    }

    onMessage(msg){

    }
}

module.exports = {
    Socket
}
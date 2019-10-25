const { port } = require('./config')
const { Socket } = require('./socket')

;(async () => {
    const socServer = new Socket(port)
    await socServer.start()
})()
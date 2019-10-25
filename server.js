const express = require('express')
const http = require('http')

class HttpServer{
    constructor(port){
        this.port = port
        this.app = express()
        this.instance = http.createServer(this.app)
    }

    getInstance(){
        return this.instance
    }

    route(){

    }

    middleware(){
        this.app.use(express.static('public'));
    }

    start(){
        return new Promise(resolve => {
            this.middleware()
            this.route()
            this.instance.listen(this.port, () => {
                console.log("server is running in port: ", this.port)
                resolve()
            })
        })
    }
}

module.exports = HttpServer
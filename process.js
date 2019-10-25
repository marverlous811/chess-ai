const { runner, model_url } = require('./config')
const spawn = require("child_process").spawn;

function run(boardString){
    return new Promise(resolve => {
        const process = spawn('python3', [runner, model_url, boardString])
        process.stdout.on('data', function(data){
            process.kill('SIGINT')
            resolve([null, data.toString()])
        })
        process.stderr.on('error', function(err){
            resolve([err])
        })
    })
}

module.exports = {
    run
}
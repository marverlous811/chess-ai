function renderMoveHistory(move, side){
    let historyElement = $('#'+side).find("ul")
    historyElement.append(`<li>${move}</li>`)   
}

function renderForHuman(moves){
    const lastMove = moves[moves.length - 1]
    return renderMoveHistory(lastMove, "human")
}

function renderForAI(move, time){
    $("#time-last-move").html(time/1000)
    return renderMoveHistory(move, "AI")
}

$("input[type=radio][name=side]").change(function(){
    console.log(this.value)
    window.board.changeSide(parseInt(this.value))
})

$("#start-game").click(function(){
    console.log("start_game")
    window.board.start()
})
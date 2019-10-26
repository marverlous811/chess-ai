function renderMoveHistory(move, side){
    return
    console.log("render: ", move, side)
    let historyElement = $('#'+side).find("ul")
    historyElement.append(`<li>${move}</li>`)   
}

function renderForHuman(moves){
    const lastMove = moves[moves.length - 1]
    return renderMoveHistory(lastMove, "human")
}

function removeHistory(){
    $("#black").find("ul").empty()
    $("#white").find("ul").empty()
}

function renderForAI(time){
    $("#time-last-move").html(time/1000)
}

$("input[type=radio][name=side]").change(function(){
    console.log(this.value)
    window.board.changeSide(this.value)
})

$("#start-game").click(function(){
    console.log("start_game")
    window.board.start()
})
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
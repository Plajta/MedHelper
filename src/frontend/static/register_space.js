window.onload = () => {
    var socket = io();

    document.getElementsByClassName("space-registration-but")[0].addEventListener("click", () => {
        var space = document.getElementsByClassName("form2")[0].value
        
        socket.emit("send-space", space)
    })

    document.getElementById("zip-download").addEventListener("click", () => {
        window.location.href = "/download"
    })
}
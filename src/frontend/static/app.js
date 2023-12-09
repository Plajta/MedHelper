//defs
var socket;

/*
INIT APP FUNCS
*/

function changename(){
    console.log("test")
}

/*
APP FUNCS
*/

function home(){
    window.location.href = "/home"
}   
function chat(){
    window.location.href = "/chat"
}
function profile(){
    window.location.href = "/profile"
}

//chat funcs
function send_message(){
    var chat = document.getElementById("chat-input")
<<<<<<< HEAD
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]
    console.log(uuid)
=======
    var loc_url = window.location.href.split("?")[1]
    var user_hash = loc_url.split("=")[1]
>>>>>>> af8df9b (stupid ass routing)

    socket.emit("message-user-send", {
        "message": chat.value,
        "uuid": uuid
    })

    chat.value = ""
}

window.onload = () => {
    socket = io();

}
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
    Continue("/home")
}   
function chat(){
    Continue("/chat")
}
function profile(){
    Continue("/profile")
}

function Continue(dest){
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]

    window.location.href = dest + "?user=" + uuid + "?checked=1"
}

function ContinueAndSend(){
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]

    window.location.href = "/home?user=" + uuid + "?checked=1"
}

//chat funcs
function send_message(){
    var chat = document.getElementById("chat-input")
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]
    console.log(uuid)

    socket.emit("message-user-send", {
        "message": chat.value,
        "uuid": uuid
    })

    chat.value = ""
}

window.onload = () => {
    socket = io();

}
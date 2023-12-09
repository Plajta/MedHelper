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
    window.location.href = "./app_home.html"
}   
function chat(){
    window.location.href = "./app_chat.html"
}
function profile(){
    window.location.href = "./app_user.html"
}

//chat funcs
function send_message(){
    var chat = document.getElementById("chat-input")
    socket.emit("message-user-send", chat.value)

    chat.value = ""
}

window.onload = () => {
    socket = io();

}
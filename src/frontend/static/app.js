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
    var url = window.location.href.split("?")[1]
    var user_hash = url.split("=")[1]
    console.log(user_hash)

    socket.emit("message-user-send", {
        "message": chat.value,
        "user_id": user_hash
    })

    chat.value = ""
}

window.onload = () => {
    socket = io();

}
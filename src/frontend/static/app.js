//defs
var socket;
var selected_idx = -1

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

    window.location.href = dest + "?uuid=" + uuid + "?checked=1"
}

function ContinueAndSend(){
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]

    window.location.href = "/home?uuid=" + uuid + "?checked=1"
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

//questionnare funcs
function change_val(event){
    for (let i = 0; i < event.target.parentElement.parentElement.children.length; i++){
        let spec_elem = event.target.parentElement.parentElement.children[i].getElementsByTagName("I")[0]
        if (spec_elem.classList.contains("selected-sum")){
            spec_elem.classList.remove("selected-sum")
        }
    }

    if (!event.target.classList.contains("selected-sum")){

        console.log(event.target.id)
        event.target.classList.add("selected-sum")

        selected_idx = parseInt(event.target.parentElement.id.slice(3, event.target.parentElement.id.length)) - 1
    }
}

function send_summary(){
    socket.emit("summary-data", selected_idx)
}

window.onload = () => {
    socket = io();

}
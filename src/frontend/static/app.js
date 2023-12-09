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
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]

    socket.emit("summary-data", {
        "data": selected_idx,
        "uuid": uuid
    })
}

window.onload = () => {
    socket = io();

    var chat = document.getElementById("chat-input")
    var url = window.location.href.split("?")[1]
    var uuid = url.split("=")[1]

    socket.emit("load-chat-by-bed", {
            "uuid": uuid,
            "type": "messages"
    })

    socket.on("update-messages", (message_list) => {
        console.log("BallZZZZZ")

        console.log(message_list)

        let chat_div = document.getElementsByClassName("chat_div")[0]

        for (let i = chat_div.children.length - 1; i >= 0; i--){
            chat_div.removeChild(chat_div.children[i])
        }

        //load chat

        //let header = document.getElementById("popup").getElementsByTagName("h3")[0]
        //header.innerHTML = "Chat s uživatelem: " + message_list[0]["name"]
        //header.id = message_list[0]["uuid"]

        for (let i = 0; i < message_list.length ; i++){

            let message = document.createElement("div")

            if (message_list[i]["response"]){
                message.classList.add("their-message")
            }
            else {
                message.classList.add("your-message")
            }
            message.innerHTML = message_list[i]["message"]

            chat_div.appendChild(message)

        }
        chat_div.appendChild(document.createElement("br"))
        chat_div.appendChild(document.createElement("br"))
        chat_div.appendChild(document.createElement("br"))
    })
}
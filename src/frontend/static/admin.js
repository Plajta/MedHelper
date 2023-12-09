var socket = undefined
var selected_user_uuid = undefined

function show_popup(elem, sel){
    //get uuid
    let uuid = undefined

    if (sel == 0){
        //messages

        uuid = elem.parentElement.parentElement.getElementsByClassName("header")[0].id
        socket.emit("load-chat", {
            "uuid": uuid,
            "type": "messages"
        })
    }
    else if (sel == 1){
        //questions

        uuid = elem.parentElement.parentElement.getElementsByClassName("header")[0].id
        socket.emit("load-chat", {
            "uuid": uuid,
            "type": "questions"
        })
    }
    else if (sel == 2){
        //patients

        uuid = elem.parentElement.parentElement.getElementsByClassName("user-header")[0].id
        socket.emit("load-chat", {
            "uuid": uuid,
            "type": "patients"
        })
    }
    selected_user_uuid = uuid

    document.getElementById("popup").style.visibility = "visible"
}

function close_popup(){
    document.getElementById("popup").style.visibility = "hidden"
}

function send_message(){
    var message_data = document.getElementById("chat-input").value
    socket.emit("admin-event", { body: message_data,
                                uuid: selected_user_uuid})
}

window.onload = () => {
    socket = io();

    //socket.io event listeners
    socket.on("connect", () => {
        //fetch all patients (only for admin part)
        socket.emit("admin-event", { command: "send-patients"})
        
    })

    socket.on("patients-data", (data) => {
        console.log("Balls")
        let patients_data = data["patients"]
        let messages_data = data["messages"]
        let questions_data = data["questions"]

        let patients_div = document.getElementById("patient-list")
        let messages_div = document.getElementById("messages")
        let questions_div = document.getElementById("questions")

        for (let i = patients_div.children.length - 1; i >= 0; i--){;
            if (patients_div.children[i].tagName == "DIV"){
                patients_div.removeChild(patients_div.children[i])
            }
        }
        messages_div.innerHTML = ""
        questions_div.innerHTML = ""

        //add patients
        for (let i = 0; i < patients_data.length; i++){
            //create patient record
            let patient = document.createElement("div")
            patient.classList.add("patient")

            let header = document.createElement("h3")
            header.innerHTML = `Jméno: <span>${patients_data[i]["name"]}</span>`
            header.classList.add("user-header")
            header.id = patients_data[i]["id"]

            let description = document.createElement("p")
            description.innerHTML = `Narození: ${patients_data[i]["birth"]}`

            let buttons_div = document.createElement("div")
            buttons_div.classList.add("buttons")

            let button = document.createElement("button")
            button.innerHTML = "Odstranit"
            button.classList.add("but")

            let show = document.createElement("button")
            show.classList.add("message-but")
            show.innerHTML = "Zobrazit konverzaci"
            show.addEventListener("click", (event) => {
                show_popup(event.target, 2)
            })

            patient.appendChild(header)
            patient.appendChild(description)
            buttons_div.appendChild(button)
            buttons_div.appendChild(show)
            patient.appendChild(buttons_div)

            patients_div.appendChild(patient)
        }

        //add messages
        for (let i = 0; i < messages_data.length; i++){
            let message = document.createElement("div")
            message.classList.add("message")

            let header = document.createElement("h4")
            header.innerHTML = messages_data[i]["name"] + ":"
            header.classList.add("header")
            header.id = messages_data[i]["uuid"]

            let message_text = document.createElement("p")
            message_text.innerHTML = messages_data[i]["message"]

            let buttons_div = document.createElement("div")
            buttons_div.classList.add("buttons")

            let show = document.createElement("button")
            show.classList.add("message-but")
            show.innerHTML = "Zobrazit konverzaci"
            show.addEventListener("click", (event) => {
                show_popup(event.target, 0)
            })

            message.appendChild(header)
            message.appendChild(message_text)

            buttons_div.appendChild(show)
            message.appendChild(buttons_div)

            messages_div.appendChild(message)
        }

        //load chat
        for (let i = 0; i < messages_data.length; i++){
            let conv = document.createElement("div")
            conv.id = "conv"

            let header = document.createElement("h3")
            header.innerHTML = "Chat s uživatelem: " + messages_data[i]["name"]
            header.classList.add("header")
            header.id = messages_data[i]["uuid"]

            let message = document.createElement("div")
            if (message_data[i]["response"]){
                message.classList.add("your-message")
            }
            else {
                message.classList.add("their-message")
            }
            let message_text = document.createElement("p")
            message_text.innerHTML = messages_data[i]["message"]

            let buttons_div = document.createElement("div")
            buttons_div.classList.add("buttons")

            conv.appendChild(message)
            message.appendChild(message_text)

            buttons_div.appendChild(show)
            message.appendChild(buttons_div)

            let messages_div = document.getElementById("popup")
            messages_div.appendChild(message)
        }

        //add questions
        for (let i = 0; i < questions_data.length; i++){
            let message = document.createElement("div")
            message.classList.add("message")

            let header = document.createElement("h4")
            header.innerHTML = questions_data[i]["name"] + ":"
            header.classList.add("header")
            header.id = questions_data[i]["uuid"]

            let message_text = document.createElement("p")
            message_text.innerHTML = questions_data[i]["message"]

            let buttons_div = document.createElement("div")
            buttons_div.classList.add("buttons")

            let show_more_but = document.createElement("button")
            show_more_but.classList.add("message-but")
            show_more_but.innerHTML = "Detailní rozbor"
            show_more_but.addEventListener("click", (event) => {
                show_popup(event.target, 1)
            })

            message.appendChild(header)
            message.appendChild(message_text)
            buttons_div.appendChild(show_more_but)
            message.appendChild(buttons_div)

            questions_div.appendChild(message)
        }

        //event listeners
        for (let i = 0; i < patients_div.children.length; i++){
            if (patients_div.children[i].tagName == "DIV"){
                patients_div.children[i].getElementsByClassName("but")[0].addEventListener("click", (event) => {
                    var userid = event.target.parentElement.getElementsByClassName("user-header")[0].id
                    socket.emit("admin-event", { command: "delete-patient", uuid: userid})

                    //get new patients
                    socket.emit("admin-event", { command: "send-patients"})
                })
            }
        }
    })

    //event listeners
    document.querySelector("#confirm-but").addEventListener("click", (event) => {
        let name_var = document.getElementById("name").value
        let birth_var = document.getElementById("birth").value
        socket.emit("admin-event", { command: "patient-data", name: name_var, birth: birth_var})
    })
}
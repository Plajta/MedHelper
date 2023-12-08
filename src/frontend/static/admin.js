window.onload = () => {
    var socket = io();

    //socket.io event listeners
    socket.on("connect", () => {
        //fetch all patients
        socket.emit("admin-event", "send-patients")

    })

    socket.on("patients-data", (data) => {
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
            header.id = patients_data[i]["userid"]

            let description = document.createElement("p")
            description.innerHTML = patients_data[i]["desc"]

            let button = document.createElement("button")
            button.innerHTML = "Odstranit"
            button.classList.add("but")

            patient.appendChild(header)
            patient.appendChild(description)
            patient.appendChild(button)

            patients_div.appendChild(patient)
        }

        //add messages
        for (let i = 0; i < messages_data.length; i++){
            let message = document.createElement("div")
            message.classList.add("message")

            let header = document.createElement("h4")
            header.innerHTML = messages_data[i]["name"] + ":"

            let message_text = document.createElement("p")
            message_text.innerHTML = messages_data[i]["message"]

            let buttons_div = document.createElement("div")
            buttons_div.classList.add("buttons")

            let respond = document.createElement("button")
            respond.classList.add("message-but")
            respond.innerHTML = "Odpovědět"

            let resend = document.createElement("button")
            resend.classList.add("message-but")
            resend.innerHTML = "Přeposlat"

            let show = document.createElement("button")
            show.classList.add("message-but")
            show.innerHTML = "Zobrazit konverzaci"

            message.appendChild(header)
            message.appendChild(message_text)

            buttons_div.appendChild(respond)
            buttons_div.appendChild(resend)
            buttons_div.appendChild(show)
            message.appendChild(buttons_div)

            messages_div.appendChild(message)
        }

        //add questions
        for (let i = 0; i < questions_data.length; i++){
            let message = document.createElement("div")
            message.classList.add("message")

            let header = document.createElement("h4")
            header.innerHTML = questions_data[i]["name"] + ":"

            let message_text = document.createElement("p")
            message_text.innerHTML = questions_data[i]["message"]

            let show_more_but = document.createElement("button")
            show_more_but.classList.add("message-but")
            show_more_but.innerHTML = "Detailní rozbor"

            message.appendChild(header)
            message.appendChild(message_text)
            message.appendChild(show_more_but)

            questions_div.appendChild(message)
        }

        //event listeners
        for (let i = 0; i < patients_div.children.length; i++){
            if (patients_div.children[i].tagName == "DIV"){
                patients_div.children[i].getElementsByClassName("but")[0].addEventListener("click", (event) => {
                    var userid = event.target.parentElement.getElementsByClassName("user-header")[0].id
                    socket.emit("delete-patient", userid)
                })
            }
        }
    })

    //event listeners
    document.querySelector("#confirm-but").addEventListener("click", (event) => {
        document.getElementById("confirm-form").submit()

        //fetch all patients
        socket.emit("admin-event", "send-patients")
    })
}
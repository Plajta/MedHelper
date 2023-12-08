window.onload = () => {
    var socket = io();

    //socket.io event listeners
    socket.on("connect", () => {
        //fetch all patients
        socket.emit("admin-event", "send-patients")

    })

    socket.on("patients-data", (data) => {
        let patients_div = document.getElementById("patient-list")
        
        //delete all patients
        for (let i = patients_div.children.length - 1; i >= 0; i--){
            if (patients_div.children[i].tagName == "DIV"){
                patients_div.removeChild(patients_div.children[i])
            }
        }

        for (let i = 0; i < data["data"].length; i++){
            console.log(data["data"][i])
            //create patient record
            let patient = document.createElement("div")
            patient.classList.add("patient")

            let header = document.createElement("h3")
            header.innerHTML = `Jméno: <span>${data["data"][i]["name"]}</span>`
            header.classList.add("user-header")
            header.id = data["data"][i]["userid"]

            let description = document.createElement("p")
            description.innerHTML = data["data"][i]["desc"]

            let button = document.createElement("button")
            button.innerHTML = "Odstranit"
            button.classList.add("but")

            patient.appendChild(header)
            patient.appendChild(description)
            patient.appendChild(button)

            patients_div.appendChild(patient)
        }

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
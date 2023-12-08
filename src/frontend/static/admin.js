window.onload = () => {
    var socket = io();

    //socket.io event listeners
    socket.on("connect", () => {
        //fetch all patients
        socket.emit("admin-event", "send-patients")

    })

    socket.on("patients-data", (data) => {
        console.log(data)
        let patients_div = document.getElementById("patient-list")

        for (let i = 0; i < data["data"].length; i++){
            console.log(data["data"][i])
            //create patient record
            let patient = document.createElement("div")
            patient.classList.add("patient")

            let header = document.createElement("h3")
            header.innerHTML = `Jméno: <span>${data["data"][i]["name"]}</span>`
            
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
    })

    //event listeners
    document.querySelector("#confirm-but").addEventListener("click", (event) => {
        document.getElementById("confirm-form").submit()

        //fetch all patients
        socket.emit("admin-event", "send-patients")
    })
}
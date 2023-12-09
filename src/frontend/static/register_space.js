window.onload = () => {
    console.log("test1")
    var socket = io();

    socket.on("registration-valid", (data) => {
        console.log(data)
        if (data == "success"){
            
        }
    })

    document.getElementsByClassName("space-registration-but")[0].addEventListener("click", (event) => {
        document.getElementsByClassName("reg-form")[0].submit()
    })
}
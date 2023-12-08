window.onload = () => {
    //event listeners
    document.querySelector("button.login-but").addEventListener("click", (event) => {
        document.getElementById("login-form").submit()
    })
}
window.onload = () => {
    //event listeners
    document.querySelector("confirm-but").addEventListener("click", (event) => {
        document.getElementById("confirm-form").submit()
    })
}
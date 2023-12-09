
var frame_home = document.getElementById("frame_home");
var frame_chat = document.getElementById("frame_chat");
var frame_profile = document.getElementById("frame_profile");
var frame_message = document.getElementById("frame_message");

var homebutton = document.getElementById("home_button");
var chatbutton = document.getElementById("chat_button");
var profilbutton = document.getElementById("profile_button");
homebutton.classList.add("nav_chosen");
chatbutton.classList.remove("nav_chosen");
profilbutton.classList.remove("nav_chosen");


frame_home.style.display = "flex";
frame_chat.style.display = "none";
frame_profile.style.display = "none";
frame_message.style.display = "none";


function Chat(){
    frame_home.style.display = "none";
    frame_chat.style.display = "flex";
    frame_profile.style.display = "none";
    frame_message.style.display = "none";

    homebutton.classList.remove("nav_chosen");
    chatbutton.classList.add("nav_chosen");
    profilbutton.classList.remove("nav_chosen");
}
function Home(){
    frame_home.style.display = "flex";
    frame_chat.style.display = "none";
    frame_profile.style.display = "none";
    frame_message.style.display = "none";

    homebutton.classList.add("nav_chosen");
    chatbutton.classList.remove("nav_chosen");
    profilbutton.classList.remove("nav_chosen");
}
function Profil(){
    frame_home.style.display = "none";
    frame_chat.style.display = "none";
    frame_profile.style.display = "flex";
    frame_message.style.display = "none";

    homebutton.classList.remove("nav_chosen");
    chatbutton.classList.remove("nav_chosen");
    profilbutton.classList.add("nav_chosen");
}

function WriteMsg(){
    frame_home.style.display = "none";
    frame_chat.style.display = "none";
    frame_profile.style.display = "none";
    frame_message.style.display = "flex";

    homebutton.classList.remove("nav_chosen");
    chatbutton.classList.remove("nav_chosen");
    profilbutton.classList.remove("nav_chosen");
}
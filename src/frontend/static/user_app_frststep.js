var firstFrame = document.getElementById("first_frame");
var secondFrame = document.getElementById("second_frame");
var thirdFrame = document.getElementById("third_frame");



firstFrame.style.display = "block";
secondFrame.style.display = "none";
thirdFrame.style.display = "none";

var frame = 1;

function Next(){
    switch (frame) {
        case 1:
            console.log("1");
            firstFrame.style.display = "none";
            secondFrame.style.display = "block";
            thirdFrame.style.display = "none";
            
            frame += 1;
            break;
        case 2:
            console.log("2");
            firstFrame.style.display = "none";
            secondFrame.style.display = "none";
            thirdFrame.style.display = "block";
            frame += 1;
            break;
        case 3:
            console.log("3");
            firstFrame.style.display = "none";
            secondFrame.style.display = "none";
            thirdFrame.style.display = "none";
            frame += 1;
            break;
    }
}

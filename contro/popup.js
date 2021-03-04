
document.addEventListener('DOMContentLoaded', function() {
    var tempButton=document.getElementById("trigger");
    tempButton.addEventListener("click",executeDetection);
});

function executeDetection(){
    var temp=document.getElementById("trigger");
    if(temp.innerText!=='Loading...'){
        temp.innerHTML="<span class=\"spinner-border spinner-border-sm\"></span> \n  Loading...";
        chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
            let url = tabs[0].url;
            console.log(url);
        });
// Once code is done with an answer, the below code must be triggered for reset
        // temp.innerHTML="  <span></span>\n  Analyse";
    }
}


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

			var res = url.split("/");
			res.shift();
			res.shift();
			res.shift(); 
			url=res.join('/');
			
            let link='http://localhost:5000/'+url;
			
            const response = fetch(link, {
                method: 'GET',
                mode:'no-cors',
                headers: {
                  'Content-Type': 'application/json'
                }
            });
            console.log(response);
        });
// Once code is done with an answer, the below code must be triggered for reset
        // temp.innerHTML="  <span></span>\n  Analyse";
    }
}

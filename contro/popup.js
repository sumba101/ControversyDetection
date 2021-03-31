
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
			
            let link='http://localhost:8000/'+url;
			
            fetch(link, {
                method: 'GET',
                headers: {
                  'Content-Type': 'application/json'
                }
            })
            .then(r=>r.text())
            .then(res=>{
                data=JSON.parse(res)["data"]
                var table = document.getElementById("results")
                var row = table.insertRow(0)
                row.insertCell(0).innerHTML="Tweet text";
                row.insertCell(1).innerHTML="Controversial";
                
                for(const [tweetText,contro] of Object.entries(data)){
                    var row = table.insertRow(-1)
                    row.insertCell(0).innerHTML=tweetText;
                    row.insertCell(1).innerHTML=contro;
                
                }
            })
        });
// Once code is done with an answer, the below code must be triggered for reset
        temp.innerHTML="  <span></span>\n  Analyse";
    }
}

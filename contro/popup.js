
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
            var tempo=url.split("//")[1].split('/')

            if (tempo[0]==='twitter.com') {
                tempo.shift();
                url=tempo.join('/');
                
                let link='http://localhost:8000/';
                
                const params = {"url":url};

                fetch(link, {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(params)
                })
                .then(r=>r.text())
                .then(res=>{
                    data=JSON.parse(res)["data"]

                    percent = JSON.parse(res)["percentage"]
                    if(percent!=null){
                    var per = document.getElementById("percentage")
                    per.innerHTML="Controversy :  "+ percent + "%"
                    }

                    var table = document.getElementById("results")
                    var row = table.insertRow(0)
                    row.insertCell(0).innerHTML="Tweet text";
                    row.insertCell(1).innerHTML="Controversial";
                    
                    for(const [tweetText,contro] of Object.entries(data)){
                        var row = table.insertRow(-1)

                        if(contro == true){
                        	temporary = "<span style ='background-color:red;'>"+contro+"</style>"
                        }else{
                        	temporary = "<span style ='background-color:green;'>"+contro+"</style>"
                        }
                        row.insertCell(0).innerHTML=tweetText;
                        row.insertCell(1).innerHTML=temporary;
                    
                       	}
                        temp.innerHTML="  <span></span>\n  Analyse";

                    })
            }
        });
    }
    
}

let connect_status = document.getElementById('sconnect')
let connect_status_rpi = document.getElementById('sconnectrpi')


let yourToken = document.getElementById('token')

let connectBut = document.getElementById('connect')
let racBut = document.getElementById('reverseAutoControl')
let openBut = document.getElementById('open')
let closeBut = document.getElementById('close')

const arduinoSocket = new WebSocket(
    'ws://'+window.location.host+'/ws/arduino/'
);
arduinoSocket.onopen = function(e) {  
    console.log("Соединение открыто...");
};

arduinoSocket.onmessage = function(e) {
    let data = JSON.parse(e.data)
    if(data.target != undefined && data.data != undefined){
        document.getElementById(data.target).innerHTML = data.data
    }
    console.log(data)
};


connectBut.addEventListener('click', ()=>{
    let token = yourToken.value
    arduinoSocket.send(JSON.stringify({"command":"connect", "key":token}));
})
racBut.addEventListener('click', ()=>{
    arduinoSocket.send(JSON.stringify({"command":"send_to_rpi", "data":"3"}));
})
openBut.addEventListener('click', ()=>{
    arduinoSocket.send(JSON.stringify({"command":"send_to_rpi", "data":"1"}));
})
closeBut.addEventListener('click', ()=>{
    arduinoSocket.send(JSON.stringify({"command":"send_to_rpi", "data":"2"}));
})

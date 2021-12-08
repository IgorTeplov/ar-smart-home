let view_terminal = document.getElementById('status')

let startBut = document.getElementById('start')
let stopBut = document.getElementById('stop')

// const roomName = JSON.parse(document.getElementById('room-name').textContent);

// const chatSocket = new WebSocket(
//     'ws://'
//     + window.location.host
//     + '/ws/chat/'
//     + roomName
//     + '/'
// );

// chatSocket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     document.querySelector('#chat-log').value += (data.message + '\n');
// };

// chatSocket.onclose = function(e) {
//     console.error('Chat socket closed unexpectedly');
// };

// document.querySelector('#chat-message-input').focus();
// document.querySelector('#chat-message-input').onkeyup = function(e) {
//     if (e.keyCode === 13) {  // enter, return
//         document.querySelector('#chat-message-submit').click();
//     }
// };

// document.querySelector('#chat-message-submit').onclick = function(e) {
//     const messageInputDom = document.querySelector('#chat-message-input');
//     const message = messageInputDom.value;
//     chatSocket.send();
//     messageInputDom.value = '';
// };


const arduinoSocket = new WebSocket(
    'ws://'+window.location.host+'/ws/arduino/'
);



arduinoSocket.onopen = function(e) {  
	console.log("Соединение открыто...");
};
arduinoSocket.onmessage = function(e) {
    view_terminal.innerHTML = e.data
};

startBut.addEventListener('click', ()=>{
	arduinoSocket.send(JSON.stringify({"command":"connect", "key":'secretkey'}));
})

stopBut.addEventListener('click', ()=>{
	arduinoSocket.send(JSON.stringify({
        'command': 'stop' 
    }))
})

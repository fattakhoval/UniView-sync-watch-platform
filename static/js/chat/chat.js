var chatElementByClass = document.querySelector('.chat');
var chatId = chatElementByClass.id;
const user = document.querySelector('#username').value;

// Установка WebSocket соединения
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + chatId + '/'
);


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.username + ': ' + data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').onkeyup = function(e) {
    const messageInput = document.querySelector('#chat-message-input');
    if (e.keyCode === 13 && messageInput.value.trim() !== '') {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const message = document.querySelector('#chat-message-input').value;

    if (message.trim() !== '') {
        chatSocket.send(JSON.stringify({
            'message': message,
            'user': user
        }));
        document.getElementById('chat-message-input').value = '';
    }
};

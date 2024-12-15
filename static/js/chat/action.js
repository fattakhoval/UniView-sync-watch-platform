const bodyElement = document.querySelector('body');
const roomId = bodyElement.getAttribute('data-room-id');

const actionRoomSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/room_action/' + roomId + '/'
);

document.getElementById('sendVideoButton').addEventListener('click', function() {
    const videoShareUrl = document.getElementById('videoUrl').value;

    if (videoShareUrl) {
        const message = videoShareUrl;

        actionRoomSocket.send(JSON.stringify({
            'action': 'new_link',
            'url': message,
        }));

        // Очищаем поле ввода после отправки
        document.getElementById('videoForm').reset();
    } else {
        alert('Пожалуйста, введите корректный URL.');
    }
});



actionRoomSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.type == 'add_link'){
        const player = document.getElementById('videoPlayer')
            player.src = data.url
    }

    console.log(data)


};

actionRoomSocket.onclose = function(e) {
    console.error('ActionRoom socket closed unexpectedly');
};
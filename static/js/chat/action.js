const bodyElement = document.querySelector('body');
const roomId = bodyElement.getAttribute('data-room-id');
const playButton = document.getElementById('playButton');
const buttonIcon = document.getElementById('buttonIcon');
const playIcon = '<i class="fa-solid fa-play" style="color: #ffffff;"></i>';
const pauseIcon = '<i class="fa-solid fa-pause" style="color: #ffffff;"></i>';

export const actionRoomSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/room_action/' + roomId + '/'
);

let sourceBuffer;
let chunkQueue = [];


const mediaSource = new MediaSource();
const videoPlayer = document.getElementById('videoPlayer');



mediaSource.addEventListener('sourceopen', () => {
    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp9, opus"');
//    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8, vorbis"');
    console.log('MediaSource opened and SourceBuffer created.');
    if (sourceBuffer) {
        sourceBuffer.addEventListener('updateend', () => {
            console.log('Chunk appended to SourceBuffer.');
            processQueue(); // Обрабатываем следующий чанк в очереди
        });
    } else {
        console.error('Failed to create SourceBuffer.');
    }
    processQueue();
});

actionRoomSocket.onmessage = function(e) {
    if (e.data instanceof Blob) {
        if (videoPlayer.src === '') {
            videoPlayer.src = URL.createObjectURL(mediaSource);
            videoPlayerContainer.style.display = "block";
        }

        const reader = new FileReader();
        reader.onload = function(event) {
            const arrayBuffer = event.target.result;
            // Если sourceBuffer занят, добавляем чанк в очередь
            if (sourceBuffer && sourceBuffer.updating) {
                chunkQueue.push(arrayBuffer);
                console.log(`Чанк добавлен в очередь: размер ${arrayBuffer.byteLength}`);
            } else {
                chunkQueue.push(arrayBuffer);
                processQueue(); // Пытаемся обработать очередь
            }
        };
        reader.readAsArrayBuffer(e.data); // Читаем Blob как ArrayBuffer
    } else {
        // Если данные не являются Blob, обрабатываем как JSON
        const data = JSON.parse(e.data);
        if (data.type == 'add_link') {
            const player = document.getElementById('iframePlayer');
            player.src = data.url;
        } else if (data.type == 'action') {
            console.log(data.do_action)
            if (data.do_action == 'play') {
                playButton.innerHTML = pauseIcon;
                videoPlayer.play();

            } else if (data.do_action == 'pause') {
                playButton.innerHTML = playIcon;
                videoPlayer.pause();
            } else if (data.do_action == 'scroll') {
                console.log(data.seek_time)
                videoPlayer.currentTime = data.seek_time
            }
        } else if (data.file === 'END_OF_STREAM') {
            // Если получено сообщение о завершении потока
            mediaSource.endOfStream(); // Завершаем поток
            console.log('Конец потока достигнут.');
        } else {
            console.error('Получены некорректные данные:', data.file);
        }
    }
};


actionRoomSocket.onclose = function(e) {
    console.error('ActionRoom socket closed unexpectedly');
};

function processQueue() {
    if (chunkQueue.length > 0 && sourceBuffer && !sourceBuffer.updating) {
        const nextChunk = chunkQueue.shift(); // Получаем следующий чанк из очереди
        try {
            sourceBuffer.appendBuffer(nextChunk); // Добавляем чанк в SourceBuffer
            console.log(`Appending chunk of size: ${nextChunk.byteLength}`);
        } catch (error) {
            console.error('Error appending chunk to SourceBuffer:', error);
        }
    }
}


// Функция которая отправляет видео чанками по вебсокету
function sendVideoInChunks(videoFile) {
    const chunkSize = 1024 * 1024; // 1 MB
    const totalChunks = Math.ceil(videoFile.size / chunkSize);
    let currentChunk = 0;

    function readNextChunk() {
        const start = currentChunk * chunkSize;
        const end = Math.min(start + chunkSize, videoFile.size);
        const chunk = videoFile.slice(start, end);

        const reader = new FileReader();
        reader.onload = function(event) {

            actionRoomSocket.send(event.target.result);
            console.log(`Envoyé morceau ${currentChunk + 1} de ${totalChunks}`);
            currentChunk++;

            if (currentChunk < totalChunks) {
                readNextChunk();
            } else {

//                actionRoomSocket.send('END_OF_STREAM');
                console.log('send all chunk');
            }
        };

        reader.onerror = function(error) {
            console.error('Error :', error);
        };

        reader.readAsArrayBuffer(chunk);
    }

    readNextChunk();
}

// Ивент для загрузки видео от пользователя или через ссылку
document.getElementById('sendVideoButton').addEventListener('click', function() {
    const videoShareUrl = document.getElementById('videoUrl').value;
    const videoFile = document.getElementById('videoFile').files[0];
    const videoPlayerContainer = document.getElementById('videoPlayerContainer');
    const iframePlayerContainer = document.getElementById('iframePlayerContainer');
    const iframePlayer = document.getElementById('iframePlayer');
    if (videoShareUrl) {


        iframePlayerContainer.style.display = "block";
        videoPlayerContainer.style.display = "none";
         // Очистить содержимое video
        videoPlayer.src = ""; // Удаляем источник видео

        actionRoomSocket.send(JSON.stringify({
            'action': 'new_link',
            'url': videoShareUrl,
        }));
    } else if (videoFile) {

        playButton.innerHTML = playIcon;
        iframePlayer.src = "";
        iframePlayerContainer.style.display = "none";

        sendVideoInChunks(videoFile);

    } else {
        alert('Пожалуйста, введите корректный URL или загрузите видео.');
    }

    document.getElementById('videoForm').reset();
});


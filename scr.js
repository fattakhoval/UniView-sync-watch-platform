const socket = new WebSocket('ws://localhost:8000/ws/video/');
const mediaSource = new MediaSource();
const videoElement = document.getElementById('myVideo');
videoElement.src = URL.createObjectURL(mediaSource);

let sourceBuffer;
let chunkQueue = []; // Очередь для хранения входящих чанков

mediaSource.addEventListener('sourceopen', () => {
//    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp9, opus"');
    sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8, vorbis"');
    console.log('MediaSource opened and SourceBuffer created.');
    videoElement.play();
    processQueue(); // Начинаем обработку очереди, когда SourceBuffer готов
});

// Функция для обработки очереди чанков
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

// Обработка входящих сообщений WebSocket
socket.addEventListener('message', async (event) => {
    if (event.data instanceof Blob) {
        const arrayBuffer = await event.data.arrayBuffer(); // Преобразуем Blob в ArrayBuffer
        chunkQueue.push(arrayBuffer); // Добавляем чанк в очередь
        console.log(`Received chunk of size: ${arrayBuffer.byteLength}`);
        processQueue(); // Пытаемся обработать очередь
    } else if (event.data === 'END_OF_STREAM') {
        // Если получено сообщение о завершении потока
        mediaSource.endOfStream(); // Завершаем поток
        console.log('End of stream reached.');
    } else {
        console.error('Received non-Blob data:', event.data);
    }
});

// Слушаем событие updateend для обработки следующего чанка
sourceBuffer.addEventListener('updateend', () => {
    console.log('Chunk appended to SourceBuffer.');
    processQueue(); // Обрабатываем следующий чанк в очереди
});

socket.addEventListener('close', () => {
    console.log('WebSocket connection closed.');
});

socket.addEventListener('error', (error) => {
    console.error('WebSocket error:', error);
});

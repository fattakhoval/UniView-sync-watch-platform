import m3u8
import ffmpeg
import requests


def get_video():

    url = 'https://river-3-335.rutube.ru/hls-vod/9UVEimcMVXKcA8aj3UYrVA/1734975692/2317/rutube-ds-origin-vs322-1/21ca585aa2b04478aeaafdda793d8036.mp4.m3u8?i=1280x692_889'

        # Fetch the M3U8 playlist
    response =  requests.get(url)
    response.raise_for_status()  # Raise an error if the request fails
    playlist = m3u8.loads(response.text)

    # Get the base URL for resolving relative segment URLs
    base_url = url.rsplit('/', 1)[0] + '/'

    # Iterate over the segments in the playlist
    for segment in playlist.segments:
        segment_url = urljoin(base_url, segment.uri)  # Resolve the full URL of the segment
        print(f"Fetching segment: {segment_url}")

        # Fetch the segment content
        try:
            segment_response = requests.get(segment_url)
            segment_response.raise_for_status()
            yield segment_response.content  # Yield the segment content
        except Exception as e:
            print(f"Failed to fetch segment: {segment_url}, error: {e}")

    # Notify that the stream has ended
    yield 'END_OF_STREAM'


def transcode_segment(segment):

    # Create a process to transcode the input segment
    process = (
        ffmpeg
        .input('pipe:0', format='mp4')  # Input format is MPEG-TS (mpegts)
        .output('pipe:1', format='webm', vcodec='libvpx', acodec='libvorbis')  # Output format is WebM
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)
    )

    # Run the process and send the segment data to stdin
    output, error = process.communicate(input=segment)

    if process.returncode != 0:
        raise RuntimeError(f"FFmpeg error: {error.decode()}")

    return output

def jjk_video():

    chunk_size = 1024 * 1024
    video_file = '/home/letquare/Downloads/Jujutsu Kaisen Season 2「AMV」After Dark x Sweater Weather.mp4'

    with open(video_file, 'rb') as video_file:
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break  # End of file reached

            print(f'send: {len(chunk)}')
            yield chunk

        yield 'END_OF_STREAM'
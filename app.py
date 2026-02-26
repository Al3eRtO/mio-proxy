import logging
import sys
import os
import asyncio
from aiohttp import web

# --- Path Setup ---
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.hls_proxy import HLSProxy
from services.ffmpeg_manager import FFmpegManager
from config import PORT, DVR_ENABLED, RECORDINGS_DIR, MAX_RECORDING_DURATION, RECORDINGS_RETENTION_DAYS

# --- Environment Variables ---
API_KEY_REQUIRED = os.getenv("API_KEY")

if DVR_ENABLED:
    from services.recording_manager import RecordingManager
    from routes.recordings import setup_recording_routes

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

def create_app():
    ffmpeg_manager = FFmpegManager()
    proxy = HLSProxy(ffmpeg_manager=ffmpeg_manager)
    
    # --- Auth Middleware (VERSIONE CORRETTA) ---
    @web.middleware
    async def auth_middleware(request, handler):
        if API_KEY_REQUIRED:
            user_key = request.query.get('api_key') or request.query.get('key')
            if user_key != API_KEY_REQUIRED:
                return web.Response(status=401, text="401 Unauthorized: API Key errata o mancante")
        return await handler(request)

    # Creiamo l'app includendo il middleware correttamente
    app = web.Application(middlewares=[auth_middleware])
    
    app['ffmpeg_manager'] = ffmpeg_manager
    app.ffmpeg_manager = ffmpeg_manager

    if DVR_ENABLED:
        recording_manager = RecordingManager(
            recordings_dir=RECORDINGS_DIR,
            max_duration=MAX_RECORDING_DURATION,
            retention_days=RECORDINGS_RETENTION_DAYS
        )
        app['recording_manager'] = recording_manager
    
    # --- Routes ---
    app.router.add_get('/', proxy.handle_root)
    app.router.add_get('/favicon.ico', proxy.handle_favicon)
    
    static_p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    if not os.path.exists(static_p):
        os.makedirs(static_p)
    app.router.add_static('/static', static_p)
    
    app.router.add_get('/builder', proxy.handle_builder)
    app.router.add_get('/info', proxy.handle_info_page)
    app.router.add_get('/api/info', proxy.handle_api_info)
    app.router.add_get('/key', proxy.handle_key_request)
    app.router.add_get('/proxy/manifest.m3u8', proxy.handle_proxy_request)
    app.router.add_get('/proxy/hls/manifest.m3u8', proxy.handle_proxy_request)
    app.router.add_get('/proxy/mpd/manifest.m3u8', proxy.handle_proxy_request)
    app.router.add_get('/proxy/stream', proxy.handle_proxy_request)
    app.router.add_get('/extractor', proxy.handle_extractor_request)
    app.router.add_get('/extractor/video', proxy.handle_extractor_request)
    app.router.add_get('/proxy/hls/segment.ts', proxy.handle_proxy_request)
    app.router.add_get('/proxy/hls/segment.m4s', proxy.handle_proxy_request)
    app.router.add_get('/proxy/hls/segment.mp4', proxy.handle_proxy_request)
    app.router.add_get('/playlist', proxy.handle_playlist_request)
    app.router.add_get('/segment/{segment}', proxy.handle_ts_segment)
    app.router.add_get('/decrypt/segment.mp4', proxy.handle_decrypt_segment)
    app.router.add_get('/decrypt/segment.ts', proxy.handle_decrypt_segment)
    app.router.add_get('/license', proxy.handle_license_request)
    app.router.add_post('/license', proxy.handle_license_request)
    app.router.add_post('/generate_urls', proxy.handle_generate_urls)
    app.router.add_get('/proxy/ip', proxy.handle_proxy_ip)

    # --- HLS Stream Handler ---
    async def proxy_hls_stream(request):
        stream_id = request.match_info.get('stream_id')
        filename = request.match_info.get('filename')
        base_dir = os.path.abspath("temp_hls")
        file_path = os.path.abspath(os.path.join(base_dir, stream_id, filename))
        
        if not file_path.startswith(base_dir):
            return web.Response(status=403, text="403 Forbidden")

        if not os.path.exists(file_path):
            return web.Response(status=404, text="404 Not Found")
            
        if hasattr(app, 'ffmpeg_manager'):
             app.ffmpeg_manager.touch_stream(stream_id)
        
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Cache-Control": "no-cache, no-store, must-revalidate"
        }

        if filename.endswith('.m3u8'):
            try:
                content = ""
                for _ in range(5):
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if content: break
                    await asyncio.sleep(0.2)
                return web.Response(text=content, content_type='application/vnd.apple.mpegurl', headers=headers)
            except Exception as e:
                return web.Response(status=500, text=f"Error: {str(e)}")
        
        return web.FileResponse(file_path, headers=headers)

    app.router.add_get('/ffmpeg_stream/{stream_id}/{filename}', proxy_hls_stream)

    if DVR_ENABLED:
        setup_recording_routes(app, recording_manager)
    
    app.router.add_route('OPTIONS', '/{tail:.*}', proxy.handle_options)
    
    async def on_startup(app):
        asyncio.create_task(ffmpeg_manager.cleanup_loop())
    app.on_startup.append(on_startup)

    return app

# --- Entry Point ---
app = create_app()

if __name__ == '__main__':
    render_port = int(os.environ.get("PORT", 10000))
    web.run_app(app, host='0.0.0.0', port=render_port)

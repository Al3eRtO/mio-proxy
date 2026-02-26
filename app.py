import logging
import sys
import os
import asyncio
from aiohttp import web

# Aggiungi path corrente per import moduli
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.hls_proxy import HLSProxy
from services.ffmpeg_manager import FFmpegManager
from config import PORT, DVR_ENABLED, RECORDINGS_DIR, MAX_RECORDING_DURATION, RECORDINGS_RETENTION_DAYS

# Recupera la password dalle variabili d'ambiente di Render
API_KEY_REQUIRED = os.getenv("API_KEY")

# Import componenti DVR se abilitati
if DVR_ENABLED:
    from services.recording_manager import RecordingManager
    from routes.recordings import setup_recording_routes

# Configurazione logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# --- Logica di Avvio ---
def create_app():
    """Crea e configura l'applicazione aiohttp."""
    ffmpeg_manager = FFmpegManager()
    proxy = HLSProxy(ffmpeg_manager=ffmpeg_manager)

    app = web.Application()
    
    # --- Middleware di Autenticazione ---
    @web.middleware
    async def auth_middleware(app, handler):
        async def middleware(request):
            if API_KEY_REQUIRED:
                user_key = request.query.get('api_key') or request.query.get('key')
                if user_key != API_KEY_REQUIRED:
                    return web.Response(status=401, text="Accesso Negato: API Key non valida o mancante")
            return await handler(request)
        return middleware

    app.middlewares.append(auth_middleware)

    app['ffmpeg_manager'] = ffmpeg_manager
    app.ffmpeg_manager = ffmpeg_manager

    if DVR_ENABLED:
        recording_manager = RecordingManager(
            recordings_dir=RECORDINGS_DIR,
            max_duration=MAX_RECORDING_DURATION,
            retention_days=RECORDINGS_RETENTION_DAYS
        )
        app['recording_manager'] = recording_manager
    
    # Registra le route
    app.router.add_get('/', proxy.handle_root)
    app.router.add_get('/favicon.ico', proxy.handle_favicon)
    
    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    if not os.path.exists(static_path):
        os.makedirs(static_path)
    app.router.add_static('/static', static_path)
    
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

    async def proxy_hls_stream(request):
        stream_id = request.match_info['stream_id']
        filename = request.match_info['filename']
        file_path = os.path.join("temp_hls", stream_id, filename)
        
        try:
            if not os.path.abspath(file_path).startswith(os.path.abspath("temp_hls")):
                 return web.Response(status=403, text="Access denied")
        except:
            return web.Response(status=403, text="Access denied")

        if not os.path.exists(file_path):
            return web.Response(status=404, text="Segment not found")
            
        if hasattr(app, 'ffmpeg_manager'):
             app.ffmpeg_manager.touch_stream(stream_id)
        
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Connection": "keep-alive"
        }

        if filename.endswith('.m3u8'):
            try:
                content = ""
                for _ in range(3):
                    if os.path.exists(file_path):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if content:
                            break
                    await asyncio.sleep(0.1)
                
                return web.Response(
                    text=content,
                    content_type='application/vnd.apple.mpegurl',
                    headers=headers
                )
            except Exception as e:
                logging.error(f"Error reading playlist {file_path}: {e}")
                return web.Response(status=500, text="Internal Server Error")
        
        if filename.endswith('.ts'):
             return web.FileResponse(file_path

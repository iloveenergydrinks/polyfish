"""
PolyFish Backend Flask application factory.
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings from third-party libraries such as transformers.
# This must be set before all other imports.
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request, send_from_directory
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    project_root = os.path.dirname(backend_root)
    frontend_dist = os.path.join(project_root, 'frontend', 'dist')
    static_folder = frontend_dist if os.path.isdir(frontend_dist) else None

    app = Flask(
        __name__,
        static_folder=static_folder,
        static_url_path=''
    )
    app.config.from_object(config_class)

    # Ensure JSON responses return text directly instead of escaped unicode sequences.
    # Flask >= 2.3 uses app.json.ensure_ascii; older versions use JSON_AS_ASCII.
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False

    # Set up logging.
    logger = setup_logger('polyfish')

    # Only print startup logs in the reloader subprocess to avoid duplicate logs in debug mode.
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process

    if should_log_startup:
        logger.info("=" * 50)
        logger.info("PolyFish Backend is starting...")
        logger.info("=" * 50)

    # Enable CORS.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register simulation process cleanup so all child processes exit on shutdown.
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Registered simulation process cleanup hook")

    # Request logging middleware.
    @app.before_request
    def log_request():
        logger = get_logger('mirofish.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")

    @app.after_request
    def log_response(response):
        logger = get_logger('mirofish.request')
        logger.debug(f"Response: {response.status_code}")
        return response

    # Register blueprints.
    from .api import graph_bp, simulation_bp, report_bp, market_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    app.register_blueprint(market_bp, url_prefix='/api/markets')

    # Health check.
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'PolyFish Backend'}

    if static_folder:
        @app.route('/', defaults={'path': ''})
        @app.route('/<path:path>')
        def serve_frontend(path):
            if path.startswith('api/'):
                return {'success': False, 'error': 'Not found'}, 404

            asset_path = os.path.join(app.static_folder, path)
            if path and os.path.exists(asset_path):
                return send_from_directory(app.static_folder, path)

            return send_from_directory(app.static_folder, 'index.html')

    if should_log_startup:
        logger.info("PolyFish Backend startup completed")

    return app

"""
PolyFish Backend entry point.
"""

import os
import sys

# Avoid Windows console encoding issues by forcing UTF-8 before other imports.
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add the project root to the import path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config


def main():
    """Main entry point."""
    # Validate configuration, but do not block read-only endpoints such as
    # market browsing and health checks when LLM/Zep credentials are absent.
    errors = Config.validate()
    if errors:
        print("Configuration warnings:")
        for err in errors:
            print(f"  - {err}")
        print("\nContinuing startup. Routes that require these services will fail until configured.")

    # Create the app.
    app = create_app()

    # Get runtime configuration.
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5001))
    debug = Config.DEBUG

    # Start the service.
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    main()

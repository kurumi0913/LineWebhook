"""
This script runs the LineWebhook application using a development server.
"""

from os import environ
import os
from LineWebhook import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

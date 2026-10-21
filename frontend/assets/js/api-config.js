// VisionEdge — Centralized API Configuration
// Dynamically selects localhost in development and Render in production.
(function () {
    const hostname = window.location.hostname || '';
    const isLocal = hostname === 'localhost' ||
                    hostname === '127.0.0.1' ||
                    hostname.startsWith('192.168.') ||
                    hostname.startsWith('10.') ||
                    hostname.endsWith('.local') ||
                    window.location.protocol === 'file:';

    window.API_BASE_URL = isLocal
        ? 'http://127.0.0.1:5000/api'
        : 'https://visionedge-opticals.onrender.com/api';
})();

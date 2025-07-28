from flask import Flask, jsonify
from app.utils.extensions import init_app
from app.config import Config
import json
import os

def create_app(config_class=None):
    """Application factory pattern"""
    app = Flask(__name__)

    # Use config parameter or default to Config
    if config_class is None:
        config_class = Config

    app.config.from_object(config_class)

    # Initialize extensions
    init_app(app)

    # Register main blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.account_routes import account_bp
    from app.routes.finance_routes import finance_bp
    from app.routes.transaction_routes import transaction_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(finance_bp)
    app.register_blueprint(transaction_bp)

    # SWAGGER UI ROUTE
    @app.route('/docs')
    def swagger_ui():
        """Swagger UI - Real Implementation"""
        html_content = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>RevoBank API Documentation</title>
            <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui.css" />
            <style>
                html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
                *, *:before, *:after { box-sizing: inherit; }
                body { margin:0; background: #fafafa; }
                .swagger-ui .topbar { display: none; }
            </style>
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-bundle.js"></script>
            <script src="https://unpkg.com/swagger-ui-dist@5.0.0/swagger-ui-standalone-preset.js"></script>
            <script>
                window.onload = function() {
                    const ui = SwaggerUIBundle({
                        url: '/api/v1/swagger.json',
                        dom_id: '#swagger-ui',
                        deepLinking: true,
                        presets: [
                            SwaggerUIBundle.presets.apis,
                            SwaggerUIStandalonePreset
                        ],
                        plugins: [
                            SwaggerUIBundle.plugins.DownloadUrl
                        ],
                        layout: "StandaloneLayout",
                        validatorUrl: null,
                        docExpansion: "list",
                        operationsSorter: "alpha",
                        displayRequestDuration: true,
                        tryItOutEnabled: true
                    });
                };
            </script>
        </body>
        </html>
        '''
        return html_content, 200, {'Content-Type': 'text/html'}

    @app.route('/api/v1/swagger.json')
    def swagger_json():
        """Swagger JSON specification"""
        try:
            # Path ke file swagger_spec.json
            swagger_file_path = os.path.join(app.root_path, 'swagger', 'swagger_spec.json')

            if not os.path.exists(swagger_file_path):
                # Return basic swagger spec jika file tidak ada
                return jsonify({
                    "openapi": "3.0.0",
                    "info": {
                        "title": "RevoBank API",
                        "description": "RevoBank Banking System API Documentation",
                        "version": "1.0.0",
                        "contact": {
                            "name": "RevoBank API Support",
                            "email": "support@revobank.com"
                        }
                    },
                    "servers": [
                        {
                            "url": "http://127.0.0.1:5000",
                            "description": "Development server"
                        }
                    ],
                    "components": {
                        "securitySchemes": {
                            "bearerAuth": {
                                "type": "http",
                                "scheme": "bearer",
                                "bearerFormat": "JWT"
                            }
                        }
                    },
                    "security": [
                        {
                            "bearerAuth": []
                        }
                    ],
                    "paths": {
                        "/": {
                            "get": {
                                "summary": "Health Check",
                                "description": "Check if the API is running",
                                "tags": ["Health"],
                                "responses": {
                                    "200": {
                                        "description": "API is running successfully"
                                    }
                                }
                            }
                        }
                    }
                })

            with open(swagger_file_path, 'r', encoding='utf-8') as f:
                swagger_spec = json.load(f)

            return jsonify(swagger_spec)
        except Exception as e:
            return jsonify({
                'error': f'Error loading swagger specification: {str(e)}',
                'message': 'Using basic spec instead'
            }), 200

    @app.route('/api/v1/health')
    def api_health():
        """API Health check"""
        return jsonify({
            'status': 'OK',
            'message': 'RevoBank API is running',
            'version': '1.0.0',
            'swagger_ui': '/docs',
            'swagger_json': '/api/v1/swagger.json'
        })

    # Health check endpoint
    @app.route('/')
    def health_check():
        return jsonify({
            'status': 'OK',
            'message': 'RevoBank API is running',
            'version': '1.0.0',
            'swagger_ui': '/docs',
            'documentation': 'Access /docs for API documentation'
        })

    return app

# Untuk backward compatibility
app = create_app()

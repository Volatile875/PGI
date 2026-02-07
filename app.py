import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import get_config
import structlog
from pythonjsonlogger import jsonlogger

def setup_logging(app):
    """Configures structured logging for the application."""
    log_level = app.config.get("LOG_LEVEL", "INFO")
    
    # Configure standard logging
    handler = logging.StreamHandler()
    if app.config.get("LOG_FORMAT") == "json":
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    # Configure Structlog
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

def create_app():
    """App factory for the PostgreSQL AI Assistant backend."""
    app = Flask(__name__)
    
    # Load configuration
    config_obj = get_config()
    app.config.from_object(config_obj)
    
    # Initialize infrastructure
    CORS(app)
    setup_logging(app)
    logger = structlog.get_logger(__name__)
    
    # Proactive directory check for logs
    if not os.path.exists(app.config['LOG_DIR']):
        os.makedirs(app.config['LOG_DIR'])

    # Placeholder for blueprints and module imports
    # These will be plugged in as the project grows
    _register_extensions(app)
    _register_blueprints(app)
    _register_error_handlers(app)

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "version": "1.0.0",
            "environment": os.environ.get("FLASK_ENV", "development")
        }), 200

    @app.route('/api/v1/query', methods=['POST'])
    def process_query():
        """
        Central orchestrator endpoint.
        Connects NLP, DB, and Safety modules.
        """
        data = request.get_json()
        user_query = data.get("query")
        
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        logger.info("received_query", query=user_query)

        try:
            # 1. Intent Classification
            from nlp.intent_classifier import classify_intent
            intent = classify_intent(user_query)
            
            # 2. SQL Generation
            from nlp.sql_generator import generate_sql
            generated_sql = generate_sql(intent, user_query)
            
            # 3. SQL Validation (Safety Layer)
            from safety.sql_validator import validate_sql
            is_safe, error_msg = validate_sql(generated_sql)
            if not is_safe:
                logger.warning("unsafe_query_detected", query=generated_sql, reason=error_msg)
                return jsonify({"error": f"Security violation: {error_msg}"}), 403
            
            # 4. Query Execution
            from db.query_executor import execute_query
            results = execute_query(generated_sql)
            
            return jsonify({
                "status": "success",
                "intent": intent,
                "sql": generated_sql,
                "data": results,
                "message": "Query processed successfully through all layers."
            }), 200

        except Exception as e:
            logger.error("query_processing_failed", error=str(e))
            return jsonify({"error": "Query processing failed", "details": str(e)}), 500

    return app

def _register_extensions(app):
    """Register Flask extensions."""
    # Example: db.init_app(app)
    pass

def _register_blueprints(app):
    """Register blueprints for the application."""
    # Future: from routes.chat import chat_bp
    # app.register_blueprint(chat_bp, url_prefix='/api/v1/chat')
    pass

def _register_error_handlers(app):
    """Register custom error handlers."""
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "An internal server error occurred"}), 500

# For running with Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

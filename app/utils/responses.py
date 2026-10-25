from flask import jsonify

def api_response(status="success", message="", data=None, status_code=200):
    """
    Format standar response JSON untuk API FoodRescue
    """
    response_body = {
        "status": status,
        "message": message
    }
    
    if data is not None:
        response_body["data"] = data
        
    return jsonify(response_body), status_code

def error_response(message="Terjadi kesalahan pada server", status_code=400, details=None):
    """
    Format standar response error JSON
    """
    response_body = {
        "status": "error",
        "error": message
    }
    
    if details:
        response_body["details"] = details
        
    return jsonify(response_body), status_code

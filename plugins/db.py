from database import get_session, Record

# MCP metadata
DESCRIPTION = "Database operations for storing and retrieving key-value records"
SCHEMA = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "description": "Database action to perform",
            "enum": ["insert", "query", "delete", "list_all"]
        },
        "key": {
            "type": "string",
            "description": "The key for the record"
        },
        "value": {
            "type": "string",
            "description": "The value for the record (required for insert)"
        },
        "id": {
            "type": "integer",
            "description": "Record ID (required for delete)"
        }
    },
    "required": ["action"]
}

def run(params):
    action = params.get("action", "")
    if not action:
        return {
            "tool": "db",
            "error": "Missing 'action' parameter"
        }

    try:
        session = get_session()
        
        if action == "insert":
            key = params.get("key")
            value = params.get("value")
            
            if not key or not value:
                return {
                    "tool": "db",
                    "error": "Both 'key' and 'value' are required for insert"
                }
            
            record = Record(key=key, value=value)
            session.add(record)
            session.commit()
            return {
                "tool": "db",
                "action": "insert",
                "status": "success",
                "id": record.id,
                "key": key,
                "value": value
            }

        elif action == "query":
            key = params.get("key")
            if not key:
                return {
                    "tool": "db",
                    "error": "'key' parameter required for query"
                }
            
            result = session.query(Record).filter_by(key=key).all()
            return {
                "tool": "db",
                "action": "query",
                "key": key,
                "count": len(result),
                "results": [{"id": r.id, "key": r.key, "value": r.value} for r in result]
            }
        
        elif action == "list_all":
            result = session.query(Record).all()
            return {
                "tool": "db",
                "action": "list_all",
                "count": len(result),
                "results": [{"id": r.id, "key": r.key, "value": r.value} for r in result]
            }
        
        elif action == "delete":
            record_id = params.get("id")
            if not record_id:
                return {
                    "tool": "db",
                    "error": "'id' parameter required for delete"
                }
            
            record = session.query(Record).filter_by(id=record_id).first()
            if record:
                session.delete(record)
                session.commit()
                return {
                    "tool": "db",
                    "action": "delete",
                    "status": "success",
                    "deleted_id": record_id
                }
            else:
                return {
                    "tool": "db",
                    "action": "delete",
                    "error": f"Record with id {record_id} not found"
                }

        else:
            return {
                "tool": "db",
                "error": f"Invalid action '{action}'. Use 'insert', 'query', 'delete', or 'list_all'"
            }
            
    except Exception as e:
        return {
            "tool": "db",
            "error": f"Database error: {str(e)}"
        }
    finally:
        session.close()

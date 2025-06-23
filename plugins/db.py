from database import get_session, Record

def run(params):
    action = params.get("action")

    if action == "insert":
        key = params.get("key")
        value = params.get("value")
        session = get_session()
        record = Record(key=key, value=value)
        session.add(record)
        session.commit()
        return {
            "tool": "db",
            "status": "inserted",
            "id": record.id
        }

    elif action == "query":
        key = params.get("key")
        session = get_session()
        result = session.query(Record).filter_by(key=key).all()
        return {
            "tool": "db",
            "results": [{ "id": r.id, "key": r.key, "value": r.value } for r in result]
        }

    else:
        return {
            "error": "Invalid action. Use 'insert' or 'query'."
        }

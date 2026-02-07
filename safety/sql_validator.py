def validate_sql(sql_query):
    """
    Validates SQL query for safety (e.g., preventing DROP/DELETE if restricted).
    """
    forbidden_keywords = ["drop", "truncate"]
    query_lower = sql_query.lower()
    
    for kw in forbidden_keywords:
        if kw in query_lower:
            return False, f"Keyword '{kw}' is not allowed."
            
    return True, None

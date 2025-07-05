import sqlparse
from typing import Tuple

# Returns (is_valid, error_message)
def validate_sql_syntax(query: str) -> Tuple[bool, str]:
    try:
        parsed = sqlparse.parse(query)
        if not parsed or not parsed[0].tokens:
            return False, "Empty or invalid SQL statement."
        return True, ""
    except Exception as e:
        return False, str(e)

from app.db import db

class GenericService:
    def __init__(self):
        pass

    def execute_procedure(self, procedure_name, params):
        try:
            sql_query = f"CALL {procedure_name}({', '.join(['%s' for _ in params])})"
            result = db.session.execute(sql_query, params)
            db.session.commit()
            return result.fetchall()
        except Exception as e:
            db.session.rollback()
            raise e

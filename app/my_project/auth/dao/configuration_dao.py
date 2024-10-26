from my_project.auth.domain.configuration import Configuration
from db import db

class ConfigurationDAO:
    def __init__(self):
        pass

    def get_all_configurations(self):
        return Configuration.query.all()

    def get_configuration_by_id(self, config_id: int):
        return Configuration.query.get(config_id)

    def add_configuration(self, configuration: Configuration):
        try:
            db.session.add(configuration)
            db.session.commit()
            db.session.refresh(configuration)
            return configuration
        except Exception as e:
            db.session.rollback()
            raise e

    def update_configuration(self, configuration):
        try:
            db.session.commit()
            db.session.refresh(configuration)
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_configuration(self, configuration):
        try:
            db.session.delete(configuration)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

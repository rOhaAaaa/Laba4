from my_project.auth.dao.configuration_dao import ConfigurationDAO

class ConfigurationService:
    def __init__(self):
        self.configuration_dao = ConfigurationDAO()

    def get_all_configurations(self):
        return self.configuration_dao.get_all_configurations()

    def get_configuration_by_id(self, config_id):
        return self.configuration_dao.get_configuration_by_id(config_id)

    def create_configuration(self, data):
        return self.configuration_dao.create_configuration(data)

    def update_configuration(self, config_id, data):
        return self.configuration_dao.update_configuration(config_id, data)

    def delete_configuration(self, config_id):
        return self.configuration_dao.delete_configuration(config_id)

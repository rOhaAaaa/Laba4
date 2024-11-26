from my_project.auth.dao.project_dao import ProjectDAO

class ProjectService:
    def __init__(self):
        self.project_dao = ProjectDAO()

    def get_all_projects(self):
        return self.project_dao.get_all_projects()

    def get_project_by_id(self, project_id):
        return self.project_dao.get_project_by_id(project_id)

    def create_project(self, project):
        return self.project_dao.create_project(project)

    def update_project(self, project):
        return self.project_dao.update_project(project)

    def delete_project(self, project):
        return self.project_dao.delete_project(project)

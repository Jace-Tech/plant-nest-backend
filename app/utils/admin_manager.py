class AdminManager:
    def __init__(self):
        self.admin_session = {"admins": {}}

    def add_admin(self, username, password):
        self.admin_session["admins"][username] = password

    def is_admin(self, username):
        return username in self.admin_session["admins"]


admin_manager = AdminManager()

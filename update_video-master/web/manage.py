#from sql_logic import select_nuke


class Nuke:
    def __init__(self, id, name, ip):
        self.id = id
        self.name = name
        self.ip = ip

    def get_video(self):
        return select_nuke(self.id)


class Video:
    def __init__(self, id, name, ftp_path):
        self.id = id
        self.name = name
        self.ftp_path = ftp_path

    def get_nukes(self):
        pass


class Linking:
    def __init__(self):
        pass

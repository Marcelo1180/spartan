from ansible.playbook import PlayBook

class Despliegue:
    def run(path_file):
        pb = PlayBook(playbook=path_file)
        pb.run()

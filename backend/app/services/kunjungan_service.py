history = []


class KunjunganService:

    @staticmethod
    def add(data):

        history.append(data)

    @staticmethod
    def all():

        return history
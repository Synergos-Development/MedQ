patients = {}


class PendaftaranService:

    @staticmethod
    def create(data):

        pasien = {
            "rm": data["rm"],
            "nama": data["nama"],
            "nik": data["nik"]
        }

        patients[
            data["rm"]
        ] = pasien

        return pasien

    @staticmethod
    def find(rm):

        return patients.get(rm)
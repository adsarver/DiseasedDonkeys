import random
    
class gendb():
    def __init__(self):
        self.ADDRESS = "69 Straight ST" # This is a real address btw
        self.NAMES = []
        self.BUILDINGS = {
            "Downtown":[
                "Armstrong",
                "Brookes",
                "Mountainlair",
                "Clark",
                "White",
                "LSB",
                "Hodges",
                "Library"
                ],
            "HSC":[
                "Ruby"
                ],
            "Evansdale":[
                "ESB",
                "AERB",
                "MRB",
                "ERB",
                "NRCCE",
            ]
        }
        with open("names.txt") as file:
            NAMES = file.readlines(-1)
            
            
    def gen_workers(self):
        return

    def gen_users(self):
        return

    def gen_requests(self):
        return
    
    def gen_rooms(self):
        return
    
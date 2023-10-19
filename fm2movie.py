import uuid

class Movie:

    def __init__(self):
        self.version = 3
        self.emuversion = 0
        self.rerecordcount = 0
        self.palflag = 0
        self.newppu = 0
        self.fds = 0
        self.fourscore = 0
        self.microphone = 0
        self.port0 = 1
        self.port1 = 0
        self.port2 = 0
        self.binery = 0
        self.length = 0

        self.romfilename = ""
        self.romchecksum = ""

        self.guid = str(uuid.uuid4()).upper() # add random uuid

        self.comment = ""
        self.savestate = 0

        self.inputs = []

class Input:

    def __init__(self):
        self.action = "none"
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.start = False
        self.select = False
        self.b = False
        self.a = False
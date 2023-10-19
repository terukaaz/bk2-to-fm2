import os
import shutil
import hashlib
import base64
import zipfile
import fm2movie


def valid_zipfile(file_path) -> bool:
    try:
        with zipfile.ZipFile(file_path, 'r'):
            return True
    except zipfile.BadZipFile:
        return False

input_file = "input.bk2"
folder_name = "temp"

if not valid_zipfile(input_file):
    print("not in zip format, returning...")
    exit(1)

if not os.path.exists(folder_name):
    os.mkdir(folder_name)
else:
    shutil.rmtree(folder_name)
    os.mkdir(folder_name)

with zipfile.ZipFile(input_file, 'r') as f: # extract bk2 contents in temp folder
    f.extractall(folder_name)


movie = fm2movie.Movie()


with open("./" + folder_name + "/Header.txt", 'r') as f:

    for line in f.readlines():

        line = line.replace("\n", "")

        if line == "":
            continue

        s = line.split(" ", 1)

        key = s[0]
        value = s[1]

        if key == "rerecordCount":
            movie.rerecordcount = int(value)
        elif key == "StartsFromSavestate":

            print("Value StartsFromSavestate found. This feature is currently unsupported, so the file won't probably work.")

            movie.savestate = 1

        elif key == "Author":
            movie.comment = "author " + value
        elif key == "GameName":
            movie.romfilename = value
        elif key == "SHA1": # TODO: fix incorrect MD5
            md5_hash = hashlib.md5(value.encode()).hexdigest()
            base64_md5 = base64.b64encode(bytes.fromhex(md5_hash)).decode()

            movie.romchecksum = base64_md5

print(movie.romchecksum)

def check_seq(dot):

    if dot == ".":
        return False
    else:
        return True

started = 0

with open("./" + folder_name + "/Input Log.txt", 'r') as f:

    for line in f.readlines():

        line = line.replace("\n", "")

        if line.startswith("[Input]"):
            started = 1
        elif line.startswith("|"):

            input = fm2movie.Input()

            if started <= 0:
                print("not started but input sequences found????")

            s = line.replace("|", "")

            # print(s)

            for i in range(s.__len__()):

                dot = s[i]

                if i == 0:
                    if check_seq(dot):
                        input.action = "reset"

                if i == 1:
                    if check_seq(dot):
                        input.action = "power"

                if i == 2:
                    if check_seq(dot):
                        input.up = True

                if i == 3:
                    if check_seq(dot):
                        input.down = True

                if i == 4:
                    if check_seq(dot):
                        input.left = True

                if i == 5:
                    if check_seq(dot):
                        input.right = True

                if i == 6:
                    if check_seq(dot):
                        input.start = True

                if i == 7:
                    if check_seq(dot):
                        input.select = True

                if i == 8:
                    if check_seq(dot):
                        input.b = True

                if i == 9:
                    if check_seq(dot):
                        input.a = True

            # print(input.__dict__)
            movie.inputs.append(input)
        elif line.startswith("[/Input]"):
            started = -1
            print("fin")
            break

with open("out.fm2", "w+") as f:

    f.write("version 3\n")
    f.write("emuVersion 20606\n") # not real
    f.write(f"rerecordcount {movie.rerecordcount}\n")
    f.write(f"palFlag {movie.palflag}\n")
    f.write(f"romFilename {movie.romfilename}\n")
    f.write(f"romChecksum base64:{movie.romchecksum}\n")
    f.write(f"guid {movie.guid}\n")
    f.write(f"fourscore {movie.fourscore}\n")
    f.write(f"microphone {movie.microphone}\n")
    f.write(f"port0 {movie.port0}\n")
    f.write(f"port1 {movie.port1}\n")
    f.write(f"port2 {movie.port2}\n")
    f.write(f"FDS {movie.fds}\n")
    f.write(f"NewPPU {movie.newppu}\n")
    f.write(f"RAMInitOption 0\n")
    f.write(f"RAMInitSeed 1\n")
    f.write(f"comment {movie.comment}\n")

    f.write("|0|........|||\n")
    f.write("|0|........|||\n")

    for input in movie.inputs:

        res = "|"

        if input.action == "none":
            res += "0"
        elif input.action == "reset":
            res += "1"
        elif input.action == "power":
            res += "2"
        else:
            print("????")

        res += "|"

        if input.right:
            res += "R"
        else:
            res += "."

        if input.left:
            res += "L"
        else:
            res += "."

        if input.down:
            res += "D"
        else:
            res += "."

        if input.up:
            res += "U"
        else:
            res += "."

        if input.start:
            res += "T"
        else:
            res += "."

        if input.select:
            res += "S"
        else:
            res += "."

        if input.b:
            res += "B"
        else:
            res += "."

        if input.a:
            res += "A"
        else:
            res += "."

        res += "|||"

        f.write(res + "\n")
    f.close()
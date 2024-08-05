print('''
                                    𝙼𝙺 𝚂𝙲𝙾𝚁𝙿𝙸𝙾𝙽
            █▓▒­░⡷⠂🇨 🇦 🇹 🇦 🇱 🇴 🇬  🇦 🇳 🇦 🇱 🇾 🇸 🇪 🇷 ⠐⢾░▒▓█''')
import os
import shutil
import hashlib
import datetime

# List of known malware signatures
malware_signatures = [
    # Worms
    "code_red.exe", "CodeRed",  # Code Red Worm
    "nimda.exe", "nimda.zip", "Nimda",  # Nimda Worm
    "sasser.exe", "Sasser",  # Sasser Worm
    "WannaCry.exe", "WannaCry",  # WannaCry Ransomware
    "Polymorphic",  # General identifier for polymorphic behavior

    # Clop Ransomware Signatures
    ".clop", ".CIop", "ClopReadMe", "CIopReadMe",
    "6d115ae4c32d01a073185df95d3441d51065340ead1eada0efda6975214d1920",
    "6d8d5aac7ffda33caa1addcdc0d4e801de40cb437cf45cface5350710cde2a74",
    "70f42cc9fca43dc1fdfa584b37ecbc81761fb996cb358b6f569d734fa8cce4e3",
    "a5f82f3ad0800bfb9d00a90770c852fb34c82ecb80627be2d950e198d0ad6e8b",
    "85b71784734705f6119cdb59b1122ce721895662a6d98bb01e82de7a4f37a188",
    
    # Common Email Addresses Used in Ransom Notes
    "servicedigilogos@protonmail.com", "managersmaers@tutanota.com",
    "unlock@eqaltech.su", "unlock@royalmail.su",
    "unlock@goldenbay.su", "unlock@graylegion.su",
    "kensgilbomet@protonmail.com",

    # Spyware and Trojans
    "keylogger.exe", "spyware_installer.exe", "adware_setup.exe",
    "zeus.exe", "zbot.exe", "emotet.exe", "ramnit.exe",
    "dridex.exe", "trickbot.exe", "trojan.exe", "backdoor.exe",
    "banking_trojan.exe", "remote_access_trojan.exe",

    # Specific viruses
    "melissa.doc", "LOVE-LETTER-FOR-YOU.TXT.vbs",
    "readme.eml", "readme.hta", "message.txt.vbs", "message.pif",
    
    # Registry keys (for illustrative purposes)
    "HKEY_CURRENT_USER\\Software\\Spyware",
    "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
    "HKEY_CURRENT_USER\\Software\\Virus",
    "HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\\Virus",
    "HKEY_CURRENT_USER\\Software\\VirusDownloader"
]

# Supported file extensions for scanning
supported_extensions = ['.txt', '.jpg', '.jpeg', '.png', '.gif', '.exe', '.dll', '.pdf', '.doc', '.docx', '.xls', '.xlsx']

def scan_folder(folder_path):
    threats_removed = 0
    removed_files = []
    unable_to_decode_files = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_supported_file(file_path):
                if is_malware(file_path):
                    remove_threat(file_path)
                    threats_removed += 1
                    removed_files.append(file_path)
                else:
                    try:
                        with open(file_path, "r", encoding="utf-8") as file:
                            file_content = file.read()
                    except UnicodeDecodeError:
                        unable_to_decode_files += 1
    return threats_removed, removed_files, unable_to_decode_files

def is_supported_file(file_path):
    """Check if the file has a supported extension."""
    return any(file_path.endswith(ext) for ext in supported_extensions)

def is_malware(file_path):
    try:
        # Read file content or calculate hash based on file type
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            for signature in malware_signatures:
                if signature in file_content:
                    return True
    except UnicodeDecodeError:
        pass  # Skip files that cannot be decoded as UTF-8

    try:
        # For binary files, calculate MD5 hash
        with open(file_path, "rb") as file:
            file_hash = hashlib.md5()
            while chunk := file.read(8192):
                file_hash.update(chunk)
        # Check if the calculated hash matches any known signatures
        if file_hash.hexdigest() in malware_signatures:
            return True
        # Also check the file name against known signatures
        if os.path.basename(file_path) in malware_signatures:
            return True

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return False

def remove_threat(file_path):
    backup_path = file_path + ".bak"
    shutil.move(file_path, backup_path)

def main():
    folder_path = input("\nEnter the path of the folder to scan: ")
    start_time = datetime.datetime.now()
    threats_removed, removed_files, unable_to_decode_files = scan_folder(folder_path)
    end_time = datetime.datetime.now()

    # Calculate the time taken for the scan
    time_taken = end_time - start_time

    print(f"Scanned folder: {folder_path}")
    print(f"Scan started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Scan completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Time taken for scan: {time_taken}")

    if threats_removed == 0:
        print("\n No threats found.")
    else:
        print(f"Threats removed: {threats_removed}")
        print("Removed files:")
        for file in removed_files:
            print(f" - {file}")

    if unable_to_decode_files > 0:
        print(f"\n Thread files and offcial files scanned: {unable_to_decode_files}")

if __name__ == "__main__":
    main()

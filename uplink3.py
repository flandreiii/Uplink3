import sys, time, random, json, os
from colorama import Fore, Style, init
init(autoreset=True)

# ============================================================
# COLORS & UTILITIES
# ============================================================

class C:
    R = Fore.RED
    G = Fore.GREEN
    Y = Fore.YELLOW
    C = Fore.CYAN
    M = Fore.MAGENTA
    W = Fore.WHITE
    RESET = Style.RESET_ALL

def slow(text, delay=0.01, color=C.W):
    for c in text:
        sys.stdout.write(color + c + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def progress_bar(value, total, length=20):
    p = int((value / total) * length)
    return "[" + "#" * p + "-" * (length - p) + "]"

# ============================================================
# ASCII ART
# ============================================================

LOGO = C.C + r"""
   __  __     _ _       _      
  |  \/  |___| | |_ _ _(_)_ _  
  | |\/| / -_) |  _| '_| | ' \ 
  |_|  |_\___|_|\__|_| |_|_||_|
      CYBERHACKER RPG v1.0
""" + C.RESET

ICE_ART = C.R + r"""
 ████████
 ██ ICE ██
 ████████
ICE DETECTED
""" + C.RESET

SCAN_ART = C.G + r"""
[ SCAN MODULE ENABLED ]
""" + C.RESET

# ============================================================
# PLAYER / RPG SYSTEM
# ============================================================

SAVE_FILE = "cyberhacker_rpg_save.json"

class Player:
    def __init__(self):
        self.name = "Agent-X"
        self.credits = 50
        self.missions_done = 0
        self.level = 1
        self.exp = 0
        self.skill_points = 0
        # skills: brute, hash, stealth, speed
        self.skills = {"brute":1,"hash":1,"stealth":1,"speed":1}
        self.inventory = ["Basic Exploit"]

    def to_dict(self):
        return {
            "name": self.name,
            "credits": self.credits,
            "missions_done": self.missions_done,
            "level": self.level,
            "exp": self.exp,
            "skill_points": self.skill_points,
            "skills": self.skills,
            "inventory": self.inventory
        }

    def from_dict(self, data):
        self.name = data["name"]
        self.credits = data["credits"]
        self.missions_done = data["missions_done"]
        self.level = data["level"]
        self.exp = data["exp"]
        self.skill_points = data["skill_points"]
        self.skills = data["skills"]
        self.inventory = data["inventory"]

    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= 100:
            self.exp -= 100
            self.level +=1
            self.skill_points +=1
            slow(f"You leveled up! Level {self.level}, +1 skill point!",0.02,C.G)

    def show(self, ui):
        ui.info(f"Name: {self.name}")
        ui.info(f"Level: {self.level} (EXP: {self.exp}/100, Skill points: {self.skill_points})")
        ui.info(f"Credits: {self.credits}")
        ui.info(f"Missions completed: {self.missions_done}")
        ui.info(f"Skills: {self.skills}")
        ui.info(f"Inventory: {self.inventory}")

# ============================================================
# SAVE / LOAD
# ============================================================

def save_game(player):
    with open(SAVE_FILE,"w") as f:
        json.dump(player.to_dict(),f)
    return True

def load_game():
    if not os.path.exists(SAVE_FILE): return None
    with open(SAVE_FILE,"r") as f:
        return json.load(f)

# ============================================================
# UI
# ============================================================

class UI:
    def header(self):
        print(LOGO)

    def menu(self,options):
        print(C.Y+"\n=== MAIN MENU ===")
        for i,o in enumerate(options,1):
            print(f"{C.C}{i}. {C.W}{o}")

    def choose(self):
        while True:
            try: return int(input(C.M+"> "))
            except: self.error("Invalid input.")

    def info(self,text): print(C.C+"[i] "+text)
    def ok(self,text): print(C.G+"[OK] "+text)
    def warn(self,text): print(C.Y+"[WARN] "+text)
    def error(self,text): print(C.R+"[ERROR] "+text)
    def ask(self,text): return input(C.G+text+" -> ")

# ============================================================
# SERVER DATABASE
# ============================================================

SERVERS = {
    "alpha.net": {"security": 1, "files": ["log1.txt","alpha.bin"]},
    "cybercorp.io": {"security": 3, "files": ["contracts.doc","backup.img"]},
    "vault.gov": {"security": 5, "files": ["nuclear.txt","agents.db"]}
}

def scan_networks(ui):
    print(SCAN_ART)
    time.sleep(0.5)
    for s,d in SERVERS.items():
        slow(f"{s} - security level {d['security']}",0.005,C.G)

# ============================================================
# HACKING ENGINE
# ============================================================

class Hacker:
    def __init__(self,ui,player):
        self.ui=ui
        self.player=player
        self.connected=None
        self.trace=0

    def connect(self,server):
        if server not in SERVERS:
            self.ui.error("Server not found.")
            return False
        self.ui.info(f"Connecting to {server}...")
        time.sleep(0.5)
        if random.random()<0.25:
            print(ICE_ART)
            self.ui.warn("ICE detected!")
        self.connected=server
        self.trace=0
        self.ui.ok(f"Connected to {server}")
        return True

    def port_scan(self):
        if not self.connected: self.ui.error("Not connected!"); return False
        self.ui.info("Port scanning...")
        for i in range(1,6):
            slow(f"Port {i*1337}/open",0.02,C.C)
        self.ui.ok("Port scan complete.")
        self.player.gain_exp(5)
        return True

    def crack_hash(self):
        if not self.connected: self.ui.error("Not connected!"); return False
        self.ui.info("Cracking server hash...")
        skill=self.player.skills["hash"]
        success=random.random() < 0.5 + 0.1*skill
        for i in range(20):
            slow(progress_bar(i,20),0.02,C.M)
        if success: self.ui.ok("Hash cracked successfully!"); self.player.gain_exp(15)
        else: self.ui.error("Hash cracking failed!")
        self.trace += 20
        return success

    def brute_force(self):
        if not self.connected: self.ui.error("Not connected!"); return False
        self.ui.info("Running brute-force attack...")
        skill=self.player.skills["brute"]
        success=random.random() < 0.45 + 0.1*skill
        for i in range(10):
            slow(f"Attempt {i+1}/10",0.03,C.Y)
        if success: self.ui.ok("Brute-force successful!"); self.player.gain_exp(15)
        else: self.ui.error("Brute-force failed!")
        self.trace +=15
        return success

    def hack_server(self):
        if not self.connected: self.ui.error("Not connected!"); return False
        sec=SERVERS[self.connected]["security"]
        self.port_scan()
        time.sleep(0.2)
        if sec>=4: 
            if not self.crack_hash(): return False
        if not self.brute_force(): return False
        self.ui.ok("Server security bypassed!")
        self.player.gain_exp(20)
        return True

    def download_file(self,filename):
        if not self.connected: self.ui.error("Not connected!"); return False
        if filename not in SERVERS[self.connected]["files"]:
            self.ui.error("File not found on server."); return False
        self.ui.info(f"Downloading {filename}...")
        for i in range(20): slow(progress_bar(i,20),0.01,C.G)
        success=random.random()<0.9
        if success: 
            self.ui.ok("File downloaded successfully!")
            self.player.credits+=50
            self.trace+=15
        else: self.ui.error("Download failed!")
        return success

    def clear_logs(self):
        if not self.connected: self.ui.error("Not connected!"); return False
        self.ui.info("Clearing server logs...")
        time.sleep(0.5)
        self.ui.ok("Logs cleared!")
        self.trace=max(0,self.trace-25)
        self.player.gain_exp(5)

# ============================================================
# SKILL TREE MENU
# ============================================================

def upgrade_skills(ui,player):
    if player.skill_points<=0:
        ui.info("No skill points available.")
        return
    ui.info(f"You have {player.skill_points} skill points.")
    ui.info("Skills: "+str(player.skills))
    while player.skill_points>0:
        skill=ui.ask("Enter skill to upgrade (brute/hash/stealth/speed) or 'exit'")
        if skill.lower() not in player.skills: break
        player.skills[skill.lower()]+=1
        player.skill_points-=1
        ui.ok(f"{skill} increased! Remaining points: {player.skill_points}")

# ============================================================
# MAIN LOOP
# ============================================================

def main():
    ui=UI()
    ui.header()
    player=Player()
    data=load_game()
    if data:
        if ui.ask("Load previous save? (y/n)").lower()=="y":
            player.from_dict(data)
            ui.ok("Save loaded!")

    hacker=Hacker(ui,player)

    while True:
        ui.menu([
            "Scan networks",
            "Connect to server",
            "Port scan",
            "Crack server hash",
            "Brute-force attack",
            "Hack server",
            "Download file",
            "Clear server logs",
            "Show player status",
            "Upgrade skills",
            "Save game",
            "Exit"
        ])
        choice=ui.choose()

        if choice==1: scan_networks(ui)
        elif choice==2: hacker.connect(ui.ask("Enter server address"))
        elif choice==3: hacker.port_scan()
        elif choice==4: hacker.crack_hash()
        elif choice==5: hacker.brute_force()
        elif choice==6: hacker.hack_server()
        elif choice==7: hacker.download_file(ui.ask("Enter filename"))
        elif choice==8: hacker.clear_logs()
        elif choice==9: player.show(ui); 
        elif choice==10: upgrade_skills(ui,player)
        elif choice==11: save_game(player); ui.ok("Game saved!")
        elif choice==12: ui.info("Exiting game. Goodbye agent."); break

if __name__=="__main__":
    main()

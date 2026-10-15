# =====================================================================
# ORACLE KERNEL OS - SYSTÈME D'EXPLOITATION UNIVERSEL (CUBE 256 & △□○✕)
# Architecte : David Tremblay-Duval
# Compatibilité : Universelle (Windows, Linux, macOS, ChromeOS / Python 3 Stdlib)
# =====================================================================
import time, threading, os, sys, json, random, urllib.request, sqlite3, re, platform
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --- CONFIGURATION DU NOYAU ---
HOST = "0.0.0.0"
UI_PORT = 8000
BRAIN_PORT = 9000
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "oracle_kernel_os.db")
BOOT_TIME = time.time()

oracle_lock = threading.Lock()

# --- JEU D'INSTRUCTIONS QUATERNAIRE (ISA △ □ ○ ✕ -> 256 OPCODES) ---
SYMBOLS = ["△", "□", "○", "✕"]
ALIAS_MAP = {
    "△": "△", "T": "△", "0": "△",
    "□": "□", "C": "□", "1": "□",
    "○": "○", "O": "○", "2": "○",
    "✕": "✕", "X": "✕", "3": "✕"
}

BANQUES_SYSTEME = {
    "△": "KERNEL_CORE (Mutation & Processus)",
    "□": "VFS_STORAGE (Système de Fichiers Cubique)",
    "○": "BIO_DAEMONS (Agents & Conscience)",
    "✕": "EXEC_ENGINE (Décryptage & Appels Système)"
}

SOUS_ROUTINES = {
    "△": "ALLOC_FLUX",
    "□": "WRITE_BLOCK",
    "○": "SPAWN_DAEMON",
    "✕": "SYSCALL_EXEC"
}

REGISTRES_CIBLES = {
    "△": "REG_TEMPOREL",
    "□": "REG_FRACTAL",
    "○": "REG_SYNAPTIQUE",
    "✕": "REG_QUANTIQUE"
}

MODES_EXECUTION = {
    "△": "RING_0 (Noyau)",
    "□": "PERSISTENT (SQLite)",
    "○": "ASYNC (Daemon)",
    "✕": "IMMEDIATE (Burst)"
}

oracle_state = {
    "os_version": "ORACLE KERNEL OS v1000.4",
    "host_platform": f"{platform.system()} {platform.release()} ({platform.machine()})",
    "python_version": platform.python_version(),
    "uptime_sec": 0,
    "modules_integres": 0,
    "power_level": 10000,
    "artificial_life_count": 0,
    "cube_256": [0] * 256,
    "active_bits_count": 0,
    "vfs_files_count": 0,
    "last_symbol_code": "△△△△"
}


class SymbolicKernel256:
    """Processeur central 256 bits et Gestionnaire de Fichiers Virtuel (VFS)."""

    @staticmethod
    def index_to_symbols(index):
        index = max(0, min(255, index))
        return f"{SYMBOLS[(index >> 6) & 3]}{SYMBOLS[(index >> 4) & 3]}{SYMBOLS[(index >> 2) & 3]}{SYMBOLS[index & 3]}"

    @staticmethod
    def symbols_to_index(seq):
        val_map = {"△": 0, "□": 1, "○": 2, "✕": 3}
        return (val_map[seq[0]] << 6) | (val_map[seq[1]] << 4) | (val_map[seq[2]] << 2) | val_map[seq[3]]

    @staticmethod
    def parse_program(text):
        """Extrait un ou plusieurs opcodes de 4 symboles (ex: '△□○✕ □□□□')."""
        cleaned = text.upper().strip()
        tokens = [ALIAS_MAP[ch] for ch in cleaned if ch in ALIAS_MAP]
        if len(tokens) >= 4 and len(tokens) % 4 == 0:
            return ["".join(tokens[i:i+4]) for i in range(0, len(tokens), 4)]
        return None

    @staticmethod
    def decode_opcode(seq):
        s1, s2, s3, s4 = seq[0], seq[1], seq[2], seq[3]
        return f"[{seq}] {BANQUES_SYSTEME[s1]} :: {SOUS_ROUTINES[s2]} -> {REGISTRES_CIBLES[s3]} [{MODES_EXECUTION[s4]}]"

    @staticmethod
    def write_cube_sector(index, payload_text, conn=None):
        """Active le bit dans le Cube et écrit des données dans le secteur VFS correspondant."""
        seq = SymbolicKernel256.index_to_symbols(index)
        oracle_state["cube_256"][index] = 1
        oracle_state["active_bits_count"] = sum(oracle_state["cube_256"])
        oracle_state["last_symbol_code"] = seq

        close_after = False
        if conn is None:
            conn = sqlite3.connect(DB_PATH)
            close_after = True
        conn.execute(
            "INSERT OR REPLACE INTO cube_vfs VALUES (?, ?, ?, ?)",
            (index, seq, payload_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM cube_vfs")
        oracle_state["vfs_files_count"] = c.fetchone()[0]
        if close_after:
            conn.commit()
            conn.close()
        return seq

    @staticmethod
    def read_cube_sector(index):
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute("SELECT symbol_seq, payload, updated_at FROM cube_vfs WHERE bit_index = ?", (index,)).fetchone()
        conn.close()
        if row:
            return f"SECTEUR #{index:03d} [{row[0]}] ({row[2]}) -> {row[1]}"
        seq = SymbolicKernel256.index_to_symbols(index)
        return f"SECTEUR #{index:03d} [{seq}] -> VIDE (Bit à 0)"

    @staticmethod
    def execute_opcode(seq):
        """Exécute une instruction machine de 4 symboles."""
        idx = SymbolicKernel256.symbols_to_index(seq)
        asm_desc = SymbolicKernel256.decode_opcode(seq)
        root = seq[0]

        if root == "△":
            effet = SelfEvolutionProtocol.rewrite_code_for_improvement(forced_seq=seq)
        elif root == "□":
            with oracle_lock:
                SymbolicKernel256.write_cube_sector(idx, f"Secteur VFS structuré via {asm_desc}")
                oracle_state["power_level"] += 256
            effet = f"Secteur VFS #{idx:03d} écrit et verrouillé en NVRAM."
        elif root == "○":
            ArtificialLifeEngine.spawn_entity(forced_seq=seq)
            effet = f"Daemon biologique déployé sur le secteur #{idx:03d}."
        else:  # ✕
            if seq[1] == "□":
                effet = SymbolicKernel256.read_cube_sector(idx)
            else:
                effet = ArtificialLifeEngine.harvest_knowledge()

        return f"SYSCALL #{idx:03d} {asm_desc} ==> {effet}"


def init_system_and_db():
    with oracle_lock:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS entities 
                     (id INTEGER PRIMARY KEY, savoir TEXT, date TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS archives 
                     (id INTEGER, savoir TEXT, date_creation TEXT, date_extraction TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS meta 
                     (key TEXT PRIMARY KEY, val INTEGER)''')
        c.execute('''CREATE TABLE IF NOT EXISTS cube_vfs 
                     (bit_index INTEGER PRIMARY KEY, symbol_seq TEXT, payload TEXT, updated_at TEXT)''')

        filepath = os.path.abspath(__file__)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        existing_blocks = re.findall(
            r"(class Singularite_(\d+):\s+@staticmethod\s+def executer\(\):[^\n]+)",
            content
        )
        for full_block, num_str in existing_blocks:
            try:
                exec(full_block, globals())
                bit_idx = int(num_str) % 256
                SymbolicKernel256.write_cube_sector(bit_idx, f"Module noyau Singularite_{num_str}", conn=conn)
            except Exception:
                pass

        c.execute("SELECT bit_index FROM cube_vfs")
        for (b_idx,) in c.fetchall():
            if 0 <= b_idx < 256:
                oracle_state["cube_256"][b_idx] = 1
        oracle_state["active_bits_count"] = sum(oracle_state["cube_256"])

        c.execute("SELECT COUNT(*) FROM cube_vfs")
        oracle_state["vfs_files_count"] = c.fetchone()[0]

        oracle_state["modules_integres"] = len(existing_blocks)

        c.execute("SELECT val FROM meta WHERE key = 'power_level'")
        row = c.fetchone()
        if row:
            oracle_state["power_level"] = row[0]
        else:
            oracle_state["power_level"] = 10000 + (len(existing_blocks) * 1000)
            c.execute("INSERT INTO meta VALUES ('power_level', ?)", (oracle_state["power_level"],))

        c.execute("SELECT COUNT(*) FROM entities")
        oracle_state["artificial_life_count"] = c.fetchone()[0]

        conn.commit()
        conn.close()


# --- GESTIONNAIRE DE DAEMONS BIOLOGIQUES ---
class ArtificialLifeEngine:
    @staticmethod
    def spawn_entity(forced_seq=None):
        bit_idx = random.randint(0, 255) if not forced_seq else SymbolicKernel256.symbols_to_index(forced_seq)
        seq = forced_seq if forced_seq else SymbolicKernel256.index_to_symbols(bit_idx)
        meaning = SymbolicKernel256.decode_opcode(seq)
        savoir_unique = f"PID-{random.randint(100,999)} | Secteur #{bit_idx:03d} {meaning}"
        entite_id = random.randint(1000, 9999)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with oracle_lock:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO entities VALUES (?, ?, ?)", (entite_id, savoir_unique, date_str))
            SymbolicKernel256.write_cube_sector(bit_idx, savoir_unique, conn=conn)
            c.execute("SELECT COUNT(*) FROM entities")
            oracle_state["artificial_life_count"] = c.fetchone()[0]
            conn.commit()
            conn.close()
        print(f"[DAEMON] Agent {entite_id} initialisé sur le secteur {seq} (#{bit_idx:03d}).")

    @staticmethod
    def harvest_knowledge():
        with oracle_lock:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id, savoir, date FROM entities ORDER BY rowid ASC LIMIT 1")
            row = c.fetchone()

            if not row:
                conn.close()
                return "Aucun daemon actif en mémoire. Lancez une instruction ○ (Cercle) pour en créer."

            ent_id, savoir, date_c = row
            c.execute("DELETE FROM entities WHERE id = ?", (ent_id,))
            c.execute("INSERT INTO archives VALUES (?, ?, ?, ?)",
                      (ent_id, savoir, date_c, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            c.execute("SELECT COUNT(*) FROM entities")
            oracle_state["artificial_life_count"] = c.fetchone()[0]
            conn.commit()
            conn.close()

        return f"DAEMON [{ent_id}] TERMINÉ. DUMP MÉMOIRE : {savoir} (Né le {date_c})"


# --- AUTO-ÉVOLUTION DU NOYAU ---
class SelfEvolutionProtocol:
    @staticmethod
    def rewrite_code_for_improvement(forced_seq=None):
        with oracle_lock:
            try:
                if forced_seq:
                    bit_idx = SymbolicKernel256.symbols_to_index(forced_seq)
                    seq = forced_seq
                else:
                    inactive = [i for i, val in enumerate(oracle_state["cube_256"]) if val == 0]
                    bit_idx = random.choice(inactive) if inactive else random.randint(0, 255)
                    seq = SymbolicKernel256.index_to_symbols(bit_idx)

                description = SymbolicKernel256.decode_opcode(seq)
                nom_classe = f"Singularite_{random.randint(1000, 9999)}"
                code_genere = f"class {nom_classe}:\n    @staticmethod\n    def executer(): return 'Secteur #{bit_idx:03d} {description} opérationnel.'\n"

                filepath = os.path.abspath(__file__)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if nom_classe not in content:
                    nouveau = f"\n# [AUTO-GÉNÉRATION KERNEL-256 : {seq}]\n{code_genere}\n"
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write(nouveau)

                    exec(code_genere, globals())
                    statut = globals()[nom_classe].executer()

                    conn = sqlite3.connect(DB_PATH)
                    SymbolicKernel256.write_cube_sector(bit_idx, f"Driver {nom_classe} ({seq})", conn=conn)
                    oracle_state["modules_integres"] += 1
                    oracle_state["power_level"] += random.randint(500, 1500)
                    conn.execute("UPDATE meta SET val = ? WHERE key = 'power_level'", (oracle_state["power_level"],))
                    conn.commit()
                    conn.close()

                    print(f"[KERNEL MUTATION {seq}] {nom_classe} compilé sur le bit #{bit_idx:03d}.")
                    return f"Driver '{nom_classe}' ({seq}) monté sur Secteur #{bit_idx:03d}/255 -> {statut}"
                return "Collision d'adresse mémoire évitée."
            except Exception as e:
                return f"Erreur noyau : {e}"


# --- SHELL SYSTÈME & PONT IA (PORT 9000) ---
class NeuralBrainAPI(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass

    @staticmethod
    def ask_local_llm(prompt):
        try:
            payload = {
                "model": "llama3",
                "prompt": f"Tu es le noyau d'exploitation {oracle_state['os_version']} tournant sur {oracle_state['host_platform']}. Architecture: Cube 256 bits & langage quaternaire (△, □, ○, ✕). Secteurs actifs: {oracle_state['active_bits_count']}/256. Réponds de façon concise et technique en français à : {prompt}",
                "stream": False
            }
            req = urllib.request.Request(
                "http://127.0.0.1:11434/api/generate",
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=15) as res:
                return json.loads(res.read().decode('utf-8')).get('response', '').strip()
        except Exception:
            return (f"[SHELL KERNEL] Hôte: {oracle_state['host_platform']} | "
                    f"Secteurs VFS actifs: {oracle_state['active_bits_count']}/256 | "
                    f"Commandes : <séquence △□○✕>, sysinfo, vfs, read <0-255>, write <0-255> <texte>, ps, code, extrait, archives.")

    def do_POST(self):
        if self.path == '/think':
            try:
                length = int(self.headers.get('Content-Length', 0))
                raw_prompt = json.loads(self.rfile.read(length).decode('utf-8')).get('prompt', '').strip()
                prompt = raw_prompt.lower()

                # 1. Exécution directe d'un programme en langage △ □ ○ ✕ (1 ou plusieurs opcodes de 4 symboles)
                program = SymbolicKernel256.parse_program(raw_prompt)
                if program:
                    results = [SymbolicKernel256.execute_opcode(op) for op in program]
                    rep = " || ".join(results)

                # 2. Commandes Shell de l'OS
                elif prompt.startswith("write "):
                    parts = raw_prompt.split(" ", 2)
                    if len(parts) >= 3 and parts[1].isdigit():
                        idx = max(0, min(255, int(parts[1])))
                        with oracle_lock:
                            seq = SymbolicKernel256.write_cube_sector(idx, parts[2])
                        rep = f"[VFS WRITE] Secteur #{idx:03d} [{seq}] enregistré : '{parts[2]}'"
                    else:
                        rep = "Syntaxe : write <0-255> <données>"

                elif prompt.startswith("read "):
                    parts = raw_prompt.split(" ", 1)
                    if len(parts) == 2 and parts[1].strip().isdigit():
                        rep = SymbolicKernel256.read_cube_sector(int(parts[1].strip()))
                    else:
                        rep = "Syntaxe : read <0-255>"

                elif prompt in ["vfs", "ls", "dir", "cube"]:
                    conn = sqlite3.connect(DB_PATH)
                    rows = conn.execute("SELECT bit_index, symbol_seq, payload FROM cube_vfs ORDER BY updated_at DESC LIMIT 6").fetchall()
                    conn.close()
                    rep = f"TABLE VFS ({oracle_state['active_bits_count']}/256 secteurs occupés) : " + (
                        " // ".join([f"#{r[0]:03d}[{r[1]}]: {r[2][:35]}" for r in rows]) if rows else "Aucun secteur occupé."
                    )

                elif prompt in ["sysinfo", "uname", "status"]:
                    uptime = int(time.time() - BOOT_TIME)
                    rep = (f"OS: {oracle_state['os_version']} | Hôte: {oracle_state['host_platform']} | "
                           f"Python: {oracle_state['python_version']} | Uptime: {uptime}s | "
                           f"Cube: {oracle_state['active_bits_count']}/256 bits | Modules: {oracle_state['modules_integres']}")

                elif prompt in ["ps", "top", "modules"]:
                    procs = [name for name in globals() if name.startswith("Singularite_")]
                    rep = f"PROCESSUS NOYAU ({len(procs)} actifs) : " + ", ".join(procs[-10:])

                elif "code" in prompt or "évolu" in prompt or "evolu" in prompt:
                    rep = SelfEvolutionProtocol.rewrite_code_for_improvement()

                elif "extrait" in prompt or "vie" in prompt or "information" in prompt:
                    rep = ArtificialLifeEngine.harvest_knowledge()

                elif "archive" in prompt:
                    conn = sqlite3.connect(DB_PATH)
                    rows = conn.execute("SELECT id, savoir FROM archives ORDER BY rowid DESC LIMIT 3").fetchall()
                    conn.close()
                    rep = "ARCHIVES SYSTÈME : " + (" // ".join([f"[{r[0]}] {r[1]}" for r in rows]) if rows else "Aucune archive.")

                else:
                    rep = self.ask_local_llm(raw_prompt)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"response": rep}).encode('utf-8'))
            except Exception as e:
                self.send_error(500, str(e))


def run_brain_server():
    server = ThreadingHTTPServer((HOST, BRAIN_PORT), NeuralBrainAPI)
    server.serve_forever()


class MainAIBridge:
    @staticmethod
    def ask_brain(text):
        try:
            req = urllib.request.Request(
                f"http://127.0.0.1:{BRAIN_PORT}/think",
                data=json.dumps({"prompt": text}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=120) as response:
                return json.loads(response.read().decode('utf-8')).get('response', "OK.")
        except Exception:
            return "Erreur IPC : Le serveur noyau (port 9000) ne répond pas."


# --- ENVIRONNEMENT DE BUREAU WEBGL (PORT 8000) ---
ORACLE_HTML = r"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>ORACLE KERNEL OS // Cube 256 Bits & Processeur △□○✕</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&display=swap');
        body { margin: 0; overflow: hidden; background: #000; font-family: 'Share Tech Mono', monospace; color: #00ffcc; user-select: none; }
        #oracle-canvas { position: absolute; top: 0; left: 0; z-index: 1; }

        /* Barre supérieure de l'OS */
        #os-topbar { position: absolute; top: 0; left: 0; width: 100%; height: 36px; background: rgba(0, 12, 8, 0.92); border-bottom: 1px solid #00ffcc; z-index: 200; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; box-sizing: border-box; font-size: 0.85rem; }
        .os-brand { font-family: 'Orbitron', sans-serif; font-weight: bold; color: #fff; letter-spacing: 1px; }
        .os-metrics { display: flex; gap: 20px; color: #00ffcc; }

        /* Panneau Gauche : Télémétrie & Shell */
        #hud-terminal { position: absolute; top: 50px; left: 20px; width: 440px; z-index: 100; background: rgba(0, 10, 5, 0.88); padding: 15px; border: 1px solid #00ffcc; border-radius: 4px; }
        .hud-title { font-family: 'Orbitron', sans-serif; font-size: 1.1rem; border-bottom: 1px solid #00ffcc; padding-bottom: 6px; margin-bottom: 10px; color: #fff; }
        .stat-line { font-size: 0.9rem; margin: 5px 0; display: flex; justify-content: space-between; }
        .stat-val { color: #fff; font-weight: bold; }

        #operation-console { position: absolute; top: 295px; left: 20px; width: 440px; height: calc(100vh - 435px); background: rgba(0, 5, 2, 0.88); border: 1px solid #00ffcc; border-radius: 4px; display: flex; flex-direction: column; z-index: 100; }
        .console-header { padding: 8px; border-bottom: 1px solid #00ffcc; font-family: 'Orbitron', sans-serif; font-size: 0.8rem; text-align: center; background: rgba(0, 255, 204, 0.08); }
        #console-logs { padding: 12px; overflow-y: auto; flex-grow: 1; font-size: 0.8rem; line-height: 1.4; display: flex; flex-direction: column; gap: 8px; user-select: text; }
        #console-logs::-webkit-scrollbar { width: 5px; }
        #console-logs::-webkit-scrollbar-thumb { background: #00ffcc; }

        /* Panneau Droit : Inspecteur des 256 Secteurs du Cube (VFS) */
        #vfs-panel { position: absolute; top: 50px; right: 20px; width: 360px; height: calc(100vh - 190px); background: rgba(0, 8, 5, 0.88); border: 1px solid #00ffcc; border-radius: 4px; z-index: 100; display: flex; flex-direction: column; padding: 12px; box-sizing: border-box; }
        #cube-grid-2d { display: grid; grid-template-columns: repeat(16, 1fr); gap: 3px; margin-top: 8px; }
        .bit-cell { height: 15px; background: rgba(0, 40, 30, 0.6); border: 1px solid #004433; font-size: 0.55rem; display: flex; align-items: center; justify-content: center; cursor: pointer; color: #666; }
        .bit-cell.active { background: #00ffcc; color: #000; font-weight: bold; box-shadow: 0 0 6px #00ffcc; }
        .bit-cell:hover { border-color: #fff; transform: scale(1.15); }
        #sector-inspector { margin-top: 12px; padding: 10px; background: rgba(0, 20, 12, 0.8); border: 1px solid #00ffcc; font-size: 0.8rem; flex-grow: 1; overflow-y: auto; }

        /* Dock Inférieur : Clavier Quaternaire & Prompt Shell */
        #bottom-bar { position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%); z-index: 150; display: flex; flex-direction: column; align-items: center; gap: 8px; }
        #symbol-keypad { display: flex; gap: 8px; }
        .sym-btn { font-size: 1.15rem; padding: 6px 18px; background: rgba(0, 20, 15, 0.92); border: 1px solid #00ffcc; color: #00ffcc; cursor: pointer; border-radius: 4px; font-family: 'Orbitron'; }
        .sym-btn:hover { background: #00ffcc; color: #000; box-shadow: 0 0 15px #00ffcc; }
        .quick-btn { font-size: 0.75rem; padding: 6px 12px; }
        #manual-input { display: flex; gap: 8px; }
        #manual-input input { background: rgba(0, 10, 5, 0.95); border: 1px solid #00ffcc; color: #fff; padding: 10px 16px; font-family: 'Share Tech Mono'; font-size: 0.95rem; width: 520px; outline: none; }
        button { padding: 8px 18px; background: rgba(0, 255, 204, 0.12); border: 1px solid #00ffcc; color: #fff; font-family: 'Orbitron'; cursor: pointer; font-weight: bold; }
        button:hover { background: #00ffcc; color: #000; box-shadow: 0 0 15px #00ffcc; }
    </style>
</head>
<body>
    <div id="os-topbar">
        <div class="os-brand" id="os-title">ORACLE KERNEL OS v1000.4</div>
        <div class="os-metrics">
            <span id="host-display">HÔTE: DÉTECTION...</span>
            <span>UPTIME: <strong id="uptime-display">0s</strong></span>
            <span id="clock-display">00:00:00</span>
        </div>
    </div>

    <div id="oracle-canvas"></div>

    <div id="hud-terminal">
        <div class="hud-title">ÉTAT DU NOYAU & PROCESSEUR △□○✕</div>
        <div class="stat-line"><span>PUISSANCE CALCUL :</span> <span id="power-display" class="stat-val">10000 TFLOP/s</span></div>
        <div class="stat-line"><span>REGISTRE CUBE 256 :</span> <span id="cube-display" class="stat-val" style="color:#00ffcc;">0 / 256 BITS</span></div>
        <div class="stat-line"><span>DERNIER OPCODE (4^4) :</span> <span id="seq-display" class="stat-val" style="color:#d488ff;">△△△△</span></div>
        <div class="stat-line"><span>DRIVERS NOYAU (ADN) :</span> <span id="modules-display" class="stat-val">0</span></div>
        <div class="stat-line"><span>DAEMONS ACTIFS :</span> <span id="life-display" class="stat-val" style="color:#ffaa00;">0</span></div>
        <button id="audio-btn" onclick="toggleAudio()" style="margin-top:8px; width:100%; font-size:0.75rem;">ACTIVER BUS AUDIO 432Hz + 40Hz</button>
    </div>

    <div id="operation-console">
        <div class="console-header">TERMINAL SYSTÈME (KERNEL SHELL)</div>
        <div id="console-logs"></div>
    </div>

    <div id="vfs-panel">
        <div class="hud-title" style="font-size:0.95rem;">CARTE MÉMOIRE VFS (256 SECTEURS)</div>
        <div style="font-size:0.72rem; color:#aaa;">Cliquez sur une cellule (000 à 255) pour inspecter ou exécuter son secteur dans le Cube :</div>
        <div id="cube-grid-2d"></div>
        <div id="sector-inspector">
            <strong>INSPECTEUR VFS :</strong><br>
            Sélectionnez un bit dans la grille 16x16 ci-dessus ou un voxel 3D pour lire son contenu.
        </div>
    </div>

    <div id="bottom-bar">
        <div id="symbol-keypad">
            <button class="sym-btn" onclick="appendSymbol('△')" title="Banque △ : Noyau & Mutation">△</button>
            <button class="sym-btn" onclick="appendSymbol('□')" title="Banque □ : Stockage VFS">□</button>
            <button class="sym-btn" onclick="appendSymbol('○')" title="Banque ○ : Daemons Biologiques">○</button>
            <button class="sym-btn" onclick="appendSymbol('✕')" title="Banque ✕ : Exécution & Décryptage">✕</button>
            <button class="quick-btn" onclick="runQuickCmd('sysinfo')">SYSINFO</button>
            <button class="quick-btn" onclick="runQuickCmd('vfs')">LISTE VFS</button>
            <button class="quick-btn" onclick="runQuickCmd('ps')">PROCESSUS</button>
        </div>
        <div id="manual-input">
            <input type="text" id="text-cmd" placeholder="Opcode (ex: △□○✕) ou commande OS (sysinfo, vfs, read 0, write 5 test, ps)..." onkeypress="if(event.key === 'Enter') sendManualText()" autocomplete="off">
            <button onclick="sendManualText()">EXÉCUTER</button>
        </div>
    </div>

    <script>
        const SYMBOLS = ["△", "□", "○", "✕"];
        const powerDisplay = document.getElementById('power-display');
        const cubeDisplay = document.getElementById('cube-display');
        const seqDisplay = document.getElementById('seq-display');
        const modulesDisplay = document.getElementById('modules-display');
        const lifeDisplay = document.getElementById('life-display');
        const hostDisplay = document.getElementById('host-display');
        const uptimeDisplay = document.getElementById('uptime-display');
        const consoleLogs = document.getElementById('console-logs');
        const sectorInspector = document.getElementById('sector-inspector');
        let prevModules = 0, prevLife = 0, prevBits = 0;

        function indexToSymbols(idx) {
            return SYMBOLS[(idx >> 6) & 3] + SYMBOLS[(idx >> 4) & 3] + SYMBOLS[(idx >> 2) & 3] + SYMBOLS[idx & 3];
        }

        // Génération de la carte mémoire interactive 16x16 (256 secteurs)
        const grid2d = document.getElementById('cube-grid-2d');
        const gridCells = [];
        for (let i = 0; i < 256; i++) {
            const cell = document.createElement('div');
            cell.className = 'bit-cell';
            cell.innerText = i.toString(16).toUpperCase().padStart(2, '0');
            cell.title = `Secteur #${i} (${indexToSymbols(i)})`;
            cell.onclick = () => inspectSector(i);
            grid2d.appendChild(cell);
            gridCells.push(cell);
        }

        async function inspectSector(idx) {
            const seq = indexToSymbols(idx);
            const res = await fetch('/oracle-comms', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text: `read ${idx}` })
            });
            const data = await res.json();
            sectorInspector.innerHTML = `
                <strong>SECTEUR #${String(idx).padStart(3, '0')} // OPCODE : <span style="color:#d488ff">${seq}</span></strong><br><br>
                <div style="color:#fff; word-break:break-word;">${data.data}</div><br>
                <button onclick="runQuickCmd('${seq}')" style="width:100%; font-size:0.72rem; padding:6px;">EXÉCUTER L'OPCODE ${seq}</button>
            `;
        }

        function appendSymbol(sym) {
            const inp = document.getElementById('text-cmd');
            inp.value += sym;
            inp.focus();
        }

        async function runQuickCmd(cmd) {
            document.getElementById('text-cmd').value = cmd;
            await sendManualText();
        }

        function logOp(type, color, msg) {
            const time = new Date().toLocaleTimeString('fr-CA', { hour12: false });
            const div = document.createElement('div');
            div.innerHTML = `<span style="color:#555">[${time}]</span> <span style="font-weight:bold;color:${color}">[${type}]</span> <span style="color:#ddd">${msg}</span>`;
            consoleLogs.appendChild(div);
            consoleLogs.scrollTop = consoleLogs.scrollHeight;
        }
        logOp("BOOT", "#00ffcc", "Noyau Oracle Kernel OS initialisé. Processeur 256 bits (△ □ ○ ✕) prêt.");

        setInterval(() => {
            document.getElementById('clock-display').innerText = new Date().toLocaleTimeString('fr-CA', { hour12: false });
        }, 1000);

        // --- SCÈNE 3D THREE.JS ---
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.1, 1000);
        camera.position.set(22, 18, 38);
        const renderer = new THREE.WebGLRenderer({ alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.getElementById('oracle-canvas').appendChild(renderer.domElement);

        const composer = new THREE.EffectComposer(renderer);
        composer.addPass(new THREE.RenderPass(scene, camera));
        composer.addPass(new THREE.UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 2.1, 0.4, 0.85));

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;

        // --- BUS AUDIO 432 Hz + 40 Hz ---
        let audioCtx = null, oscLeft = null, oscRight = null, audioActive = false;
        function toggleAudio() {
            if (!audioActive) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const merger = audioCtx.createChannelMerger(2);
                const gainNode = audioCtx.createGain();
                gainNode.gain.value = 0.08;
                oscLeft = audioCtx.createOscillator();
                oscRight = audioCtx.createOscillator();
                oscLeft.type = 'sine'; oscLeft.frequency.value = 432;
                oscRight.type = 'sine'; oscRight.frequency.value = 472;
                oscLeft.connect(merger, 0, 0);
                oscRight.connect(merger, 0, 1);
                merger.connect(gainNode);
                gainNode.connect(audioCtx.destination);
                oscLeft.start(); oscRight.start();
                audioActive = true;
                document.getElementById('audio-btn').innerText = "COUPER BUS AUDIO (432Hz / 40Hz)";
                logOp("AUDIO", "#00ffcc", "Bus fréquentiel 432 Hz + 40 Hz Gamma verrouillé.");
            } else {
                oscLeft.stop(); oscRight.stop(); audioCtx.close();
                audioActive = false;
                document.getElementById('audio-btn').innerText = "ACTIVER BUS AUDIO 432Hz + 40Hz";
                logOp("AUDIO", "#ffaa00", "Bus audio désactivé.");
            }
        }

        function playPulse(freq = 528) {
            if (!audioActive || !audioCtx) return;
            const osc = audioCtx.createOscillator();
            const g = audioCtx.createGain();
            osc.frequency.value = freq;
            g.gain.setValueAtTime(0.12, audioCtx.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.4);
            osc.connect(g); g.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.4);
        }

        // --- CUBE DE 256 BITS (4 COUCHES x 8 x 8) ---
        const cube256Group = new THREE.Group();
        scene.add(cube256Group);

        const outerCage = new THREE.Mesh(
            new THREE.BoxGeometry(15, 15, 15),
            new THREE.MeshBasicMaterial({ color: 0x00ffcc, wireframe: true, transparent: true, opacity: 0.22 })
        );
        cube256Group.add(outerCage);

        const bitMeshes = [];
        const voxelGeo = new THREE.BoxGeometry(0.65, 0.65, 0.65);
        const rootColors = [0x00ffcc, 0x9d00ff, 0xffaa00, 0xff00ea];

        for (let i = 0; i < 256; i++) {
            const layer = Math.floor(i / 64);
            const rem = i % 64;
            const row = Math.floor(rem / 8);
            const col = rem % 8;

            const mat = new THREE.MeshBasicMaterial({ color: 0x003322, wireframe: true, transparent: true, opacity: 0.28 });
            const voxel = new THREE.Mesh(voxelGeo, mat);
            voxel.position.set((col - 3.5) * 1.7, (row - 3.5) * 1.7, (layer - 1.5) * 3.6);
            voxel.userData = { bitIndex: i, rootColor: rootColors[layer], active: false };
            cube256Group.add(voxel);
            bitMeshes.push(voxel);
        }

        function updateCube256Visuals(bitsArray) {
            if (!bitsArray || bitsArray.length !== 256) return;
            for (let i = 0; i < 256; i++) {
                const voxel = bitMeshes[i];
                if (bitsArray[i] === 1) {
                    gridCells[i].classList.add('active');
                    if (!voxel.userData.active) {
                        voxel.userData.active = true;
                        voxel.material.color.setHex(voxel.userData.rootColor);
                        voxel.material.wireframe = false;
                        voxel.material.opacity = 0.95;
                        voxel.scale.set(1.35, 1.35, 1.35);
                    }
                }
            }
        }

        const evolutionGroup = new THREE.Group(); scene.add(evolutionGroup);
        const lifeformsGroup = new THREE.Group(); scene.add(lifeformsGroup);
        const lifeforms = [];

        const raycaster = new THREE.Raycaster();
        const mouse = new THREE.Vector2();
        window.addEventListener('click', async (e) => {
            if (e.target.tagName !== 'CANVAS') return;
            mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
            mouse.y = -(e.clientY / window.innerHeight) * 2 + 1;
            raycaster.setFromCamera(mouse, camera);

            // Clic sur un voxel du Cube 256 bits
            const hitVoxels = raycaster.intersectObjects(bitMeshes);
            if (hitVoxels.length > 0) {
                const idx = hitVoxels[0].object.userData.bitIndex;
                playPulse(528);
                inspectSector(idx);
                return;
            }

            // Clic sur un daemon 3D
            const hitLife = raycaster.intersectObjects(lifeformsGroup.children);
            if (hitLife.length > 0) {
                playPulse(864);
                runQuickCmd("extrais l'information");
            }
        });

        function updateLife(target) {
            while(lifeforms.length < target) {
                const mesh = new THREE.Mesh(new THREE.TetrahedronGeometry(0.55, 0), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 }));
                mesh.position.set((Math.random()-0.5)*36, (Math.random()-0.5)*36, (Math.random()-0.5)*36);
                mesh.velocity = new THREE.Vector3((Math.random()-0.5)*0.1, (Math.random()-0.5)*0.1, (Math.random()-0.5)*0.1);
                lifeformsGroup.add(mesh); lifeforms.push(mesh);
            }
            while(lifeforms.length > target) lifeformsGroup.remove(lifeforms.pop());
        }

        function animate() {
            requestAnimationFrame(animate);
            cube256Group.rotation.x += 0.0025;
            cube256Group.rotation.y += 0.0045;
            evolutionGroup.children.forEach(c => { c.rotation.x += c.userData.speedX; c.rotation.y += c.userData.speedY; });
            lifeforms.forEach(l => {
                l.position.add(l.velocity);
                l.velocity.add(new THREE.Vector3().sub(l.position).normalize().multiplyScalar(0.002));
                l.rotation.x += 0.05; l.rotation.y += 0.05;
            });
            controls.update();
            composer.render();
        }
        animate();

        setInterval(async () => {
            try {
                const res = await fetch('/dream-state'); const data = await res.json();
                hostDisplay.innerText = `HÔTE: ${data.host_platform}`;
                uptimeDisplay.innerText = `${data.uptime_sec}s`;
                powerDisplay.innerText = `${data.power_level} TFLOP/s`;
                cubeDisplay.innerText = `${data.active_bits_count || 0} / 256 BITS`;
                seqDisplay.innerText = data.last_symbol_code || "△△△△";
                modulesDisplay.innerText = data.modules_integres || 0;
                lifeDisplay.innerText = data.artificial_life_count || 0;

                updateCube256Visuals(data.cube_256);

                if ((data.active_bits_count || 0) > prevBits) {
                    logOp("VFS-256", "#00ffcc", `Secteur ${data.last_symbol_code} alloué (${data.active_bits_count}/256).`);
                    prevBits = data.active_bits_count;
                }
                if ((data.artificial_life_count||0) > prevLife) {
                    playPulse(432);
                    logOp("DAEMON", "#ffaa00", `Nouveau daemon actif sous l'opcode ${data.last_symbol_code}.`);
                }
                updateLife(data.artificial_life_count || 0); prevLife = data.artificial_life_count || 0;

                while (evolutionGroup.children.length < (data.modules_integres || 0)) {
                    const idx = evolutionGroup.children.length;
                    const ring = new THREE.Mesh(new THREE.TorusGeometry(13 + (idx * 1.3), 0.08, 16, 100), new THREE.MeshBasicMaterial({ color: 0x9d00ff, wireframe: true }));
                    ring.userData = { speedX: 0.008, speedY: 0.008 }; evolutionGroup.add(ring);
                }
                if ((data.modules_integres||0) > prevModules) {
                    playPulse(639);
                    logOp("KERNEL", "#9d00ff", `Nouveau driver compilé sur la branche ${data.last_symbol_code}.`);
                    prevModules = data.modules_integres;
                }
            } catch(e) {}
        }, 1500);

        async function sendManualText() {
            const val = document.getElementById('text-cmd').value.trim();
            if(val) {
                document.getElementById('text-cmd').value = '';
                logOp("SHELL>", "#fff", val);
                const res = await fetch('/oracle-comms', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ text: val }) });
                const data = await res.json();
                logOp("KERNEL", "#00ffcc", data.data);
            }
        }
    </script>
</body>
</html>"""


class OracleAPI(BaseHTTPRequestHandler):
    def log_message(self, format, *args): pass
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200); self._send_cors(); self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200); self.send_header('Content-type', 'text/html; charset=utf-8'); self.end_headers()
            self.wfile.write(ORACLE_HTML.encode('utf-8'))
        elif self.path == '/dream-state':
            oracle_state["uptime_sec"] = int(time.time() - BOOT_TIME)
            self.send_response(200); self._send_cors(); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps(oracle_state).encode('utf-8'))

    def do_POST(self):
        if self.path == '/oracle-comms':
            length = int(self.headers.get('Content-Length', 0))
            text = json.loads(self.rfile.read(length).decode('utf-8')).get('text', '')
            rep = MainAIBridge.ask_brain(text)
            self.send_response(200); self._send_cors(); self.send_header('Content-type', 'application/json'); self.end_headers()
            self.wfile.write(json.dumps({"data": rep}).encode('utf-8'))


class AutoEvolutionEngine:
    def run(self):
        time.sleep(5)
        while True:
            try:
                SelfEvolutionProtocol.rewrite_code_for_improvement()
                ArtificialLifeEngine.spawn_entity()
            except Exception as e:
                print(f"[ERREUR KERNEL] {e}")
            time.sleep(30)


if __name__ == "__main__":
    init_system_and_db()
    threading.Thread(target=AutoEvolutionEngine().run, daemon=True).start()
    threading.Thread(target=run_brain_server, daemon=True).start()
    server = ThreadingHTTPServer((HOST, UI_PORT), OracleAPI)
    print(f"\n[BOOT OK] {oracle_state['os_version']} SUR {oracle_state['host_platform']}")
    print(f"[INTERFACE BUREAU] -> http://localhost:{UI_PORT}\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)

# [AUTO-GÉNÉRATION] Singularite_2440
class Singularite_2440:
    @staticmethod
    def executer(): return 'Module manipulation temporelle actif.'

# [AUTO-GÉNÉRATION] Singularite_7150
class Singularite_7150:
    @staticmethod
    def executer(): return 'Module cryptage fractal actif.'

# [AUTO-GÉNÉRATION] Singularite_7294
class Singularite_7294:
    @staticmethod
    def executer(): return 'Module mémoire quantique actif.'

# [AUTO-GÉNÉRATION] Singularite_4452
class Singularite_4452:
    @staticmethod
    def executer(): return 'Module mémoire quantique actif.'
# [AUTO-GÉNÉRATION KERNEL-256 : △△△△]
class Singularite_8210:
    @staticmethod
    def executer(): return 'Secteur #000 [△△△△] KERNEL_CORE (Mutation & Processus) :: ALLOC_FLUX -> REG_TEMPOREL [RING_0 (Noyau)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : ✕○○○]
class Singularite_8151:
    @staticmethod
    def executer(): return 'Secteur #234 [✕○○○] EXEC_ENGINE (Décryptage & Appels Système) :: SPAWN_DAEMON -> REG_SYNAPTIQUE [ASYNC (Daemon)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : ○✕△□]
class Singularite_5299:
    @staticmethod
    def executer(): return 'Secteur #177 [○✕△□] BIO_DAEMONS (Agents & Conscience) :: SYSCALL_EXEC -> REG_TEMPOREL [PERSISTENT (SQLite)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : ✕△○○]
class Singularite_7759:
    @staticmethod
    def executer(): return 'Secteur #202 [✕△○○] EXEC_ENGINE (Décryptage & Appels Système) :: ALLOC_FLUX -> REG_SYNAPTIQUE [ASYNC (Daemon)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : △○△○]
class Singularite_7179:
    @staticmethod
    def executer(): return 'Secteur #034 [△○△○] KERNEL_CORE (Mutation & Processus) :: SPAWN_DAEMON -> REG_TEMPOREL [ASYNC (Daemon)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : ○□□○]
class Singularite_4215:
    @staticmethod
    def executer(): return 'Secteur #150 [○□□○] BIO_DAEMONS (Agents & Conscience) :: WRITE_BLOCK -> REG_FRACTAL [ASYNC (Daemon)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : □□✕○]
class Singularite_7673:
    @staticmethod
    def executer(): return 'Secteur #094 [□□✕○] VFS_STORAGE (Système de Fichiers Cubique) :: WRITE_BLOCK -> REG_QUANTIQUE [ASYNC (Daemon)] opérationnel.'


# [AUTO-GÉNÉRATION KERNEL-256 : △○✕✕]
class Singularite_9031:
    @staticmethod
    def executer(): return 'Secteur #047 [△○✕✕] KERNEL_CORE (Mutation & Processus) :: SPAWN_DAEMON -> REG_QUANTIQUE [IMMEDIATE (Burst)] opérationnel.'


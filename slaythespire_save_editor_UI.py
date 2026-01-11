import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import json
import base64
from itertools import cycle
import copy
import ctypes
import platform
import traceback
import sys

# --- Core Logic ---

KEY = b"key"

# Embedded Card Data (Source: rrenaud/slay_analysis)
ALL_CARDS = sorted([
    "A Thousand Cuts", "Accuracy", "Acrobatics", "Adaptation", "Adrenaline", "After Image", "Aggregate", 
    "All For One", "All Out Attack", "Alpha", "Amplify", "Anger", "Apotheosis", "Apparition", "Armaments", 
    "AscendersBane", "Auto Shields", "Backflip", "Backstab", "Ball Lightning", "Bandage Up", "Bane", 
    "Barricade", "Barrage", "Bash", "Battle Trance", "BattleHymn", "Beam Cell", "BecomeAlmighty", 
    "Berserk", "Beta", "Biased Cognition", "Bite", "Blade Dance", "Blasphemy", "Blizzard", 
    "Blood for Blood", "Bloodletting", "Bludgeon", "Blur", "Body Slam", "BootSequence", 
    "Bouncing Flask", "BowlingBash", "Brilliance", "Brutality", "Buffer", "Bullet Time", "Burn", 
    "Burning Pact", "Burst", "Calculated Gamble", "Caltrops", "Capacitor", "Carnage", "CarveReality", 
    "Catalyst", "Chaos", "Chill", "Choke", "Chrysalis", "Clash", "Cleave", "Cloak And Dagger", 
    "Clothesline", "Clumsy", "Cold Snap", "Collect", "Combust", "Compile Driver", "Concentrate", 
    "Conclude", "ConjureBlade", "Consecrate", "Conserve Battery", "Consume", "Coolheaded", "Core Surge", 
    "Corpse Explosion", "Creative AI", "Crescendo", "Crippling Poison", "CrushJoints", "CurseOfTheBell", 
    "CutThroughFate", "Dagger Spray", "Dagger Throw", "Dark Embrace", "Dark Shackles", "Darkness", 
    "Dash", "Dazed", "Deadly Poison", "Decay", "DeceiveReality", "Deep Breath", "Defend_B", "Defend_G", 
    "Defend_P", "Defend_R", "Deflect", "Defragment", "Demon Form", "DeusExMachina", "DevaForm", 
    "Devotion", "Die Die Die", "Disarm", "Discovery", "Distraction", "Dodge and Roll", "Doom and Gloom", 
    "Doppelganger", "Double Energy", "Double Tap", "Doubt", "Dramatic Entrance", "Dropkick", 
    "Dual Wield", "Dualcast", "Echo Form", "Electrodynamics", "EmptyBody", "EmptyFist", "EmptyMind", 
    "Endless Agony", "Enlightenment", "Entrench", "Envenom", "Eruption", "Escape Plan", "Establishment", 
    "Evaluate", "Eviscerate", "Evolve", "Exhume", "Expertise", "Expunger", "FTL", "FameAndFortune", 
    "Fasting2", "FearNoEvil", "Feed", "Feel No Pain", "Fiend Fire", "Finesse", "Finisher", 
    "Fire Breathing", "Fission", "Flame Barrier", "Flash of Steel", "Flechettes", "Flex", 
    "FlurryOfBlows", "Flying Knee", "FlyingSleeves", "FollowUp", "Footwork", "Force Field", 
    "ForeignInfluence", "Forethought", "Fusion", "Gash", "Genetic Algorithm", "Ghostly", 
    "Ghostly Armor", "Glacier", "Glass Knife", "Go for the Eyes", "Good Instincts", "Grand Finale", 
    "Halt", "HandOfGreed", "Havoc", "Headbutt", "Heatsinks", "Heavy Blade", "Heel Hook", 
    "Hello World", "Hemokinesis", "Hologram", "Hyperbeam", "Immolate", "Impatience", "Impervious", 
    "Indignation", "Infernal Blade", "Infinite Blades", "Inflame", "Injury", "InnerPeace", "Insight", 
    "Intimidate", "Iron Wave", "J.A.X.", "Jack Of All Trades", "Judgement", "Juggernaut", 
    "JustLucky", "Leap", "Leg Sweep", "LessonLearned", "LikeWater", "Limit Break", "LiveForever", 
    "Lockon", "Loop", "Machine Learning", "Madness", "Magnetism", "Malaise", "Master of Strategy", 
    "Masterful Stab", "MasterReality", "Mayhem", "Meditate", "Melter", "MentalFortress", 
    "Metallicize", "Metamorphosis", "Meteor Strike", "Mind Blast", "Miracle", "Multi-Cast", 
    "Necronomicurse", "Neutralize", "Night Terror", "Nirvana", "Normality", "Noxious Fumes", 
    "Offering", "Omega", "Omniscience", "Outmaneuver", "Pain", "Panacea", "Panache", "PanicButton", 
    "Parasite", "PathToVictory", "Perfected Strike", "Perseverance", "Phantasmal Killer", 
    "PiercingWail", "Poisoned Stab", "Pommel Strike", "Power Through", "Pray", "Predator", 
    "Prepared", "Pride", "Prostrate", "Protect", "Pummel", "Purity", "Quick Slash", "Rage", 
    "Ragnarok", "Rainbow", "Rampage", "ReachHeaven", "Reaper", "Reboot", "Rebound", "Reckless Charge", 
    "Recycle", "Redo", "Reflex", "Regret", "Reinforced Body", "Reprogram", "Riddle With Holes", 
    "Rip and Tear", "RitualDagger", "Rupture", "Sadistic Nature", "Safety", "Sanctity", 
    "SandsOfTime", "SashWhip", "Scrape", "Scrawl", "Searing Blow", "Second Wind", "Secret Technique", 
    "Secret Weapon", "Seeing Red", "Seek", "Self Repair", "Sentinel", "Setup", "Sever Soul", 
    "Shame", "Shiv", "Shockwave", "Shrug It Off", "SignatureMove", "Skewer", "Skim", "Slice", 
    "Slimed", "Smite", "Spot Weakness", "SpiritShield", "Stack", "Static Discharge", "Steam", 
    "Steam Power", "Storm", "Storm of Steel", "Streamline", "Strike_B", "Strike_G", "Strike_P", 
    "Strike_R", "Study", "Sucker Punch", "Sunder", "Survivor", "Sweeping Beam", "Swift Strike", 
    "Swivel", "Sword Boomerang", "Tactician", "TalkToTheHand", "Tantrum", "Tempest", "Terror", 
    "The Bomb", "Thinking Ahead", "ThirdEye", "ThroughViolence", "Thunder Strike", "Thunderclap", 
    "Tools of the Trade", "Transmutation", "Trip", "True Grit", "Turbo", "Twin Strike", 
    "Underhanded Strike", "Undo", "Unload", "Uppercut", "Vault", "Vengeance", "Venomology", 
    "Vigilance", "Violence", "Void", "Wallop", "Warcry", "WaveOfTheHand", "Weave", 
    "Well Laid Plans", "WheelKick", "Whirlwind", "White Noise", "Wild Strike", "WindmillStrike", 
    "Wireheading", "Wish", "Worship", "Wound", "Wraith Form v2", "WraithForm", "WreathOfFlame", 
    "Writhe", "Zap"
])

ALL_RELICS = sorted([
    "Anchor", "Ancient Tea Set", "Apparition", "Astrolabe", "Bag of Marbles", "Bag of Preparation", 
    "Bird-Faced Urn", "Black Blood", "Black Star", "Blood Vial", "Bloody Idol", "Blue Candle", 
    "Bottled Flame", "Bottled Lightning", "Bottled Tornado", "Bronze Scales", "Brimstone", 
    "Burning Blood", "Calling Bell", "Captain's Wheel", "Cauldron", "Ceramic Fish", "Choker", 
    "Cursed Key", "Darkstone Periapt", "Dead Branch", "Dolly's Mirror", "Dream Catcher", 
    "Ectoplasm", "Empty Cage", "Eternal Feather", "Fossilized Helix", "Frozen Egg", "Frozen Eye", 
    "Gambling Chip", "Ginger", "Girya", "Golden Idol", "Gremlin Horn", "Happy Flower", 
    "Hovering Kite", "Ice Cream", "Incense Burner", "Inserter", "Juzu Bracelet", "Kunai", 
    "Lantern", "Lizard Tail", "Magic Flower", "Mango", "Mark of the Bloom", "Matryoshka", 
    "Maw Bank", "Meat on the Bone", "Medical Kit", "Membership Card", "Mercury Hourglass", 
    "Mummified Hand", "Necronomicon", "N'loth's Gift", "Oddly Smooth Stone", "Old Coin", 
    "Omamori", "Orichalcum", "Pandora's Box", "Peace Pipe", "Pear", "Pen Nib", "Philosopher's Stone", 
    "Pocketwatch", "Potion Belt", "Prayer Wheel", "Preserved Insect", "Question Card", "Red Skull", 
    "Regal Pillow", "Ring of the Serpent", "Ring of the Snake", "Runic Dome", "Runic Pyramid", 
    "Sacred Bark", "Snecko Eye", "Sozu", "Spoon", "Ssserpent Head", "Stone Calendar", "Strawberry", 
    "Sundial", "Surgical Kit", "Tingsha", "Tiny Chest", "Tiny House", "Tough Bandages", 
    "Toxic Egg", "Toy Ornithopter", "Unceasing Top", "Velvet Choker", "War Paint", "Whetstone", 
    "White Beast Statue", "Wing Boots", "Wound Potion", "Wrist Blade"
])

def xor_data(data: bytes) -> bytes:
    return bytes(b ^ k for b, k in zip(data, cycle(KEY)))

def load_save_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            raw_data = f.read()
        
        decoded_b64 = base64.b64decode(raw_data)
        decrypted_data = xor_data(decoded_b64)
        json_str = decrypted_data.decode('utf-8')
        return json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Failed to load file: {e}")

def save_save_file(filepath, data):
    try:
        json_str = json.dumps(data)
        encrypted_data = xor_data(json_str.encode('utf-8'))
        final_data = base64.b64encode(encrypted_data)
        
        with open(filepath, 'wb') as f:
            f.write(final_data)
    except Exception as e:
        raise ValueError(f"Failed to save file: {e}")

# --- UI ---

class STSEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slay the Spire Save Editor")
        
        # --- High DPI & Scaling Logic ---
        self.scale_factor = 1.0
        try:
            if platform.system() == "Windows":
                # Tell Windows we are DPI aware so text isn't blurry
                ctypes.windll.shcore.SetProcessDpiAwareness(1)
                
                # Get the screen's DPI to calculate a scaling factor
                # Standard DPI is 96. If we are at 192 (200% scaling), factor is 2.0
                hdc = ctypes.windll.user32.GetDC(0)
                dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88) # 88 = LOGPIXELSX
                ctypes.windll.user32.ReleaseDC(0, hdc)
                
                self.scale_factor = dpi / 96.0
                print(f"Detected DPI: {dpi}, Scale Factor: {self.scale_factor}")
        except Exception as e:
            print(f"DPI Detection failed: {e}")
            pass

        # Adjust window size based on scale
        base_width = 650
        base_height = 650
        scaled_width = int(base_width * self.scale_factor)
        scaled_height = int(base_height * self.scale_factor)
        self.root.geometry(f"{scaled_width}x{scaled_height}")

        # --- Font Configuration ---
        # Calculate font sizes
        base_font_size = 10
        scaled_font_size = int(base_font_size * self.scale_factor)
        
        # Windows UI font usually Segoe UI, fallbacks for others
        ui_font = "Segoe UI" if platform.system() == "Windows" else "Helvetica"
        
        self.default_font = (ui_font, scaled_font_size)
        self.bold_font = (ui_font, scaled_font_size, "bold")
        self.small_font = (ui_font, int(scaled_font_size * 0.8))
        self.mono_font = ("Consolas", scaled_font_size)

        # Apply Global Theme Settings
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "xpnative" in style.theme_names():
            style.theme_use("xpnative")
        else:
            style.theme_use("clam")
        
        # Set default fonts for all widgets
        style.configure(".", font=self.default_font)
        style.configure("Treeview.Heading", font=self.bold_font)
        style.configure("TLabelframe.Label", font=self.bold_font)
        
        # Also set the standard Tk font option just in case
        self.root.option_add("*Font", self.default_font)
        
        # Fix for Combobox dropdown font often being tiny on Windows:
        self.root.option_add('*TCombobox*Listbox.font', self.default_font)

        # --- App Initialization ---
        self.current_data = None
        self.current_filepath = None

        self._create_menu()
        self._init_variables()
        self._create_notebook()
        
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=self.small_font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, font=self.default_font)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open .autosave...", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As...", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def _create_notebook(self):
        # Scale padding
        pad = int(10 * self.scale_factor)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=pad, pady=pad)

        # Tab 1: General Stats
        self.tab_general = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_general, text="General")
        self._build_general_tab()

        # Tab 2: Cards
        self.tab_cards = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_cards, text="Cards")
        self._build_cards_tab()

        # Tab 3: Relics
        self.tab_relics = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_relics, text="Relics")
        self._build_relics_tab()
        
        # Tab 4: Raw JSON (Advanced)
        self.tab_raw = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_raw, text="Raw JSON")
        self._build_raw_tab()

    def _init_variables(self):
        # General Vars
        self.var_gold = tk.IntVar()
        self.var_hp = tk.IntVar()
        self.var_max_hp = tk.IntVar()
        self.var_floor = tk.IntVar()
        self.var_ascension = tk.IntVar()
        self.var_name = tk.StringVar()
        
        # Gems / Keys
        self.var_emerald = tk.BooleanVar()
        self.var_ruby = tk.BooleanVar()
        self.var_sapphire = tk.BooleanVar()

    def _build_general_tab(self):
        # Scale padding
        pad_outer = int(20 * self.scale_factor)
        pad_y = int(10 * self.scale_factor)
        pad_x = int(5 * self.scale_factor)
        
        frame = ttk.Frame(self.tab_general, padding=pad_outer)
        frame.pack(fill="both", expand=True)

        grid_opts = {'padx': pad_x, 'pady': pad_y, 'sticky': tk.W}

        ttk.Label(frame, text="Name:").grid(row=0, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_name, width=30, font=self.default_font).grid(row=0, column=1, **grid_opts)

        ttk.Label(frame, text="Gold:").grid(row=1, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_gold, font=self.default_font).grid(row=1, column=1, **grid_opts)

        ttk.Label(frame, text="Current HP:").grid(row=2, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_hp, font=self.default_font).grid(row=2, column=1, **grid_opts)

        ttk.Label(frame, text="Max HP:").grid(row=3, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_max_hp, font=self.default_font).grid(row=3, column=1, **grid_opts)

        ttk.Label(frame, text="Floor:").grid(row=4, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_floor, font=self.default_font).grid(row=4, column=1, **grid_opts)
        
        ttk.Label(frame, text="Ascension Level:").grid(row=5, column=0, **grid_opts)
        ttk.Entry(frame, textvariable=self.var_ascension, font=self.default_font).grid(row=5, column=1, **grid_opts)

        # Gems / Keys Section
        sep_pad = int(20 * self.scale_factor)
        ttk.Separator(frame, orient='horizontal').grid(row=6, column=0, columnspan=2, sticky='ew', pady=sep_pad)
        ttk.Label(frame, text="Keys (Gems):").grid(row=7, column=0, **grid_opts)
        
        keys_frame = ttk.Frame(frame)
        keys_frame.grid(row=7, column=1, sticky=tk.W)
        
        ttk.Checkbutton(keys_frame, text="Emerald (Green)", variable=self.var_emerald).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(keys_frame, text="Ruby (Red)", variable=self.var_ruby).pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(keys_frame, text="Sapphire (Blue)", variable=self.var_sapphire).pack(anchor=tk.W, pady=2)

    def _build_cards_tab(self):
        pad_outer = int(15 * self.scale_factor)
        pad_inner = int(10 * self.scale_factor)
        
        frame = ttk.Frame(self.tab_cards, padding=pad_outer)
        frame.pack(fill="both", expand=True)

        # Listbox with Scrollbar
        list_frame = ttk.LabelFrame(frame, text="Current Deck", padding=pad_inner)
        list_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, pad_inner))
        
        self.cards_listbox = tk.Listbox(list_frame, width=40, height=20, font=self.default_font)
        self.cards_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.cards_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.cards_listbox.config(yscrollcommand=scrollbar.set)

        # Buttons
        btn_frame = ttk.Frame(frame, padding=(0, pad_inner))
        btn_frame.pack(side=tk.RIGHT, fill="y", expand=False)
        
        btn_pady = int(5 * self.scale_factor)

        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_card).pack(fill="x", pady=btn_pady)
        
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=pad_outer)

        ttk.Label(btn_frame, text="Add Card:").pack(fill="x", pady=(btn_pady, 2))
        
        # Combobox for Card Selection
        self.card_combobox = ttk.Combobox(btn_frame, values=ALL_CARDS, height=20, width=30, font=self.default_font)
        self.card_combobox.pack(fill="x", pady=2)
        self.card_combobox.bind('<KeyRelease>', self.check_combo)
        
        ttk.Button(btn_frame, text="Add Card", command=self.add_card).pack(fill="x", pady=pad_inner)
        
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=pad_outer)
        
        lbl = ttk.Label(btn_frame, text="Tip: Double-click a card\nin the list to toggle\nUpgraded (+) status.", font=self.small_font)
        lbl.pack(fill="x", pady=btn_pady)
        self.cards_listbox.bind('<Double-1>', self.toggle_upgrade_card)

    def check_combo(self, event):
        pass

    def _build_relics_tab(self):
        pad_outer = int(15 * self.scale_factor)
        pad_inner = int(10 * self.scale_factor)
        
        frame = ttk.Frame(self.tab_relics, padding=pad_outer)
        frame.pack(fill="both", expand=True)

        list_frame = ttk.LabelFrame(frame, text="Current Relics", padding=pad_inner)
        list_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, pad_inner))
        
        self.relics_listbox = tk.Listbox(list_frame, width=40, height=20, font=self.default_font)
        self.relics_listbox.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.relics_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.relics_listbox.config(yscrollcommand=scrollbar.set)

        btn_frame = ttk.Frame(frame, padding=(0, pad_inner))
        btn_frame.pack(side=tk.RIGHT, fill="y")
        
        btn_pady = int(5 * self.scale_factor)

        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_relic).pack(fill="x", pady=btn_pady)
        
        ttk.Separator(btn_frame, orient='horizontal').pack(fill='x', pady=pad_outer)

        ttk.Label(btn_frame, text="Add Relic:").pack(fill="x", pady=(btn_pady, 2))
        
        # Combobox for Relic Selection
        self.relic_combobox = ttk.Combobox(btn_frame, values=ALL_RELICS, height=20, width=30, font=self.default_font)
        self.relic_combobox.pack(fill="x", pady=2)
        
        ttk.Button(btn_frame, text="Add Relic", command=self.add_relic).pack(fill="x", pady=pad_inner)

    def _build_raw_tab(self):
        pad = int(10 * self.scale_factor)
        frame = ttk.Frame(self.tab_raw, padding=pad)
        frame.pack(fill="both", expand=True)
        
        self.raw_text = tk.Text(frame, wrap=tk.NONE, font=self.mono_font)
        self.raw_text.pack(fill="both", expand=True, side=tk.LEFT)
        
        scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=self.raw_text.yview)
        scrollbar_y.pack(fill="y", side=tk.RIGHT)
        self.raw_text.config(yscrollcommand=scrollbar_y.set)
        
        # Warn user
        lbl = ttk.Label(frame, text="WARNING: Manual edits here overwrite all other tabs on Save.", foreground="red", font=self.small_font)
        lbl.pack(side=tk.BOTTOM, pady=5)

    # --- Actions ---

    def open_file(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Autosave Files", "*.autosave*"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        try:
            data = load_save_file(filepath)
            self.current_data = data
            self.current_filepath = filepath
            self.refresh_ui()
            self.status_bar.config(text=f"Loaded: {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load file: {e}")

    def save_file(self):
        if not self.current_filepath:
            return self.save_file_as()
        
        self._save(self.current_filepath)

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".autosave",
            filetypes=[("Autosave Files", "*.autosave*"), ("All Files", "*.*")]
        )
        if not filepath:
            return
        
        self._save(filepath)

    def _save(self, filepath):
        try:
            # Gather data from UI
            data = self.gather_data_from_ui()
            save_save_file(filepath, data)
            self.status_bar.config(text=f"Saved to: {filepath}")
            messagebox.showinfo("Success", "File saved successfully.")
            self.current_filepath = filepath
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def refresh_ui(self):
        if not self.current_data:
            return
        
        data = self.current_data
        
        # General
        self.var_name.set(data.get("name", ""))
        self.var_gold.set(data.get("gold", 0))
        self.var_hp.set(data.get("current_health", 0))
        self.var_max_hp.set(data.get("max_health", 0))
        self.var_floor.set(data.get("floor_num", 0))
        self.var_ascension.set(data.get("ascension_level", 0))
        
        # Gems / Keys
        self.var_emerald.set(data.get("has_emerald_key", False))
        self.var_ruby.set(data.get("has_ruby_key", False))
        self.var_sapphire.set(data.get("has_sapphire_key", False))
        
        # Cards
        self.cards_listbox.delete(0, tk.END)
        for card in data.get("cards", []):
            display = card.get("id", "UNKNOWN")
            if card.get("upgrades", 0) > 0:
                display += "+" + str(card["upgrades"])
            self.cards_listbox.insert(tk.END, display)
            
        # Relics
        self.relics_listbox.delete(0, tk.END)
        for relic in data.get("relics", []):
            self.relics_listbox.insert(tk.END, relic)
            
        # Raw
        self.raw_text.delete(1.0, tk.END)
        self.raw_text.insert(tk.END, json.dumps(data, indent=2))

    def gather_data_from_ui(self):
        if not self.current_data:
            return {{}}
        
        data = self.current_data
        
        # Update General
        data["name"] = self.var_name.get()
        data["gold"] = self.var_gold.get()
        data["current_health"] = self.var_hp.get()
        data["max_health"] = self.var_max_hp.get()
        data["floor_num"] = self.var_floor.get()
        data["ascension_level"] = self.var_ascension.get()
        
        # Update Gems
        data["has_emerald_key"] = self.var_emerald.get()
        data["has_ruby_key"] = self.var_ruby.get()
        data["has_sapphire_key"] = self.var_sapphire.get()
        
        return data

    # --- Card Logic ---
    
    def remove_card(self):
        selection = self.cards_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.cards_listbox.delete(index)
        del self.current_data["cards"][index]
        self._sync_raw()

    def add_card(self):
        card_id = self.card_combobox.get().strip()
        if not card_id:
            return
        
        new_card = {"id": card_id, "upgrades": 0, "misc": 0}
        self.current_data["cards"].append(new_card)
        
        # Display
        self.cards_listbox.insert(tk.END, card_id)
        
        # Optional: Scroll to bottom
        self.cards_listbox.yview(tk.END)
        
        self._sync_raw()

    def toggle_upgrade_card(self, event):
        selection = self.cards_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        
        card = self.current_data["cards"][index]
        if card["upgrades"] == 0:
            card["upgrades"] = 1
        else:
            card["upgrades"] = 0
            
        # Update UI
        display = card["id"]
        if card["upgrades"] > 0:
            display += "+" + str(card["upgrades"])
        
        self.cards_listbox.delete(index)
        self.cards_listbox.insert(index, display)
        self.cards_listbox.selection_set(index) # restore selection
        self._sync_raw()

    # --- Relic Logic ---
    
    def remove_relic(self):
        selection = self.relics_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        self.relics_listbox.delete(index)
        del self.current_data["relics"][index]
        self._sync_raw()

    def add_relic(self):
        relic_id = self.relic_combobox.get().strip()
        if not relic_id:
            return
        
        self.current_data["relics"].append(relic_id)
        self.relics_listbox.insert(tk.END, relic_id)
        self.relic_combobox.set("") # Clear input
        self._sync_raw()

    def _sync_raw(self):
        """Updates the raw text view to match current object state"""
        self.raw_text.delete(1.0, tk.END)
        self.raw_text.insert(tk.END, json.dumps(self.current_data, indent=2))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = STSEditorApp(root)
        root.mainloop()
    except Exception:
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

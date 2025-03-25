import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import json
from datetime import datetime
import sqlite3
import os

class AdvancedEnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş İngilizce Öğrenme Asistanı")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        # Veritabanı bağlantısı
        self.create_database()

        # Kullanıcı bilgileri
        self.current_user = None
        self.score = 0

        # Kelime veritabanı
        self.vocabulary = {
            "Subjects": ["I", "You", "He", "She", "It", "We", "They"],
            "Objects": ["book", "game", "food", "water", "computer", "phone", "ball",
                       "car", "house", "table", "chair", "window", "door", "pen"],
            "Places": ["home", "school", "park", "library", "garden", "market",
                      "hospital", "restaurant", "cinema", "beach", "airport"],
            "Time_Expressions": ["today", "tomorrow", "yesterday", "now", "every day",
                               "sometimes", "often", "never", "always", "last week",
                               "next month", "in the morning", "at night"],
            "Adjectives": ["happy", "sad", "big", "small", "beautiful", "interesting",
                          "difficult", "easy", "hot", "cold", "new", "old", "good",
                          "bad", "fast", "slow", "clever", "friendly"]
        }

        # Düzensiz fiiller
        self.irregular_verbs = {
            "drink": {"past": "drank", "past_participle": "drunk",
                     "turkish": "içmek"},
            "eat": {"past": "ate", "past_participle": "eaten",
                   "turkish": "yemek"},
            "write": {"past": "wrote", "past_participle": "written",
                     "turkish": "yazmak"},
            "read": {"past": "read", "past_participle": "read",
                    "turkish": "okumak"},
            "speak": {"past": "spoke", "past_participle": "spoken",
                     "turkish": "konuşmak"},
            "go": {"past": "went", "past_participle": "gone",
                  "turkish": "gitmek"},
            "see": {"past": "saw", "past_participle": "seen",
                   "turkish": "görmek"},
            "take": {"past": "took", "past_participle": "taken",
                    "turkish": "almak"},
            "give": {"past": "gave", "past_participle": "given",
                    "turkish": "vermek"},
            "come": {"past": "came", "past_participle": "come",
                    "turkish": "gelmek"},
            "do": {"past": "did", "past_participle": "done",
                  "turkish": "yapmak"},
            "make": {"past": "made", "past_participle": "made",
                    "turkish": "yapmak"},
            "get": {"past": "got", "past_participle": "gotten",
                   "turkish": "almak"},
            "run": {"past": "ran", "past_participle": "run",
                   "turkish": "koşmak"},
            "begin": {"past": "began", "past_participle": "begun",
                     "turkish": "başlamak"}
        }

        # Düzenli fiiller
        self.regular_verbs = {
            "play": "oynamak",
            "walk": "yürümek",
            "jump": "zıplamak",
            "study": "çalışmak",
            "work": "çalışmak",
            "listen": "dinlemek",
            "watch": "izlemek",
            "help": "yardım etmek",
            "like": "sevmek",
            "love": "aşk ile sevmek",
            "hate": "nefret etmek",
            "start": "başlamak",
            "finish": "bitirmek",
            "learn": "öğrenmek",
            "teach": "öğretmek"
        }

        # Tüm fiilleri birleştir
        self.vocabulary["Verbs"] = list(self.irregular_verbs.keys()) + list(self.regular_verbs.keys())

        # Cümle kalıpları
        self.sentence_patterns = {
            "Simple Present": {
                "pattern": "Subject + Verb(s) + Object",
                "example": "He reads a book",
                "rules": [
                    "He/She/It -> Verb + s/es",
                    "I/You/We/They -> Verb",
                    "Olumlu: Subject + Verb",
                    "Olumsuz: Subject + don't/doesn't + Verb",
                    "Soru: Do/Does + Subject + Verb?"
                ],
                "turkish": "Geniş Zaman"
            },
            "Present Continuous": {
                "pattern": "Subject + am/is/are + Verb(ing) + Object",
                "example": "I am reading a book",
                "rules": [
                    "I -> am",
                    "He/She/It -> is",
                    "You/We/They -> are",
                    "Olumlu: Subject + am/is/are + Verb-ing",
                    "Olumsuz: Subject + am/is/are + not + Verb-ing",
                    "Soru: Am/Is/Are + Subject + Verb-ing?"
                ],
                "turkish": "Şimdiki Zaman"
            },
            "Simple Past": {
                "pattern": "Subject + Verb(ed/irregular) + Object",
                "example": "She played tennis",
                "rules": [
                    "Regular verbs: add -ed",
                    "Irregular verbs: special form",
                    "Olumlu: Subject + Verb(past)",
                    "Olumsuz: Subject + didn't + Verb",
                    "Soru: Did + Subject + Verb?"
                ],
                "turkish": "Geçmiş Zaman"
            }
        }

        self.login_screen()

    def create_database(self):
        conn = sqlite3.connect('english_learning.db')
        c = conn.cursor()

        # Kullanıcılar tablosu
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT PRIMARY KEY,
                     password TEXT,
                     score INTEGER,
                     last_login TEXT)''')

        # İlerleme tablosu
        c.execute('''CREATE TABLE IF NOT EXISTS progress
                    (username TEXT,
                     activity TEXT,
                     score INTEGER,
                     date TEXT)''')

        conn.commit()
        conn.close()

    def login_screen(self):
        self.clear_window()

        login_frame = tk.Frame(self.root, bg="#f0f0f0")
        login_frame.pack(expand=True)

        tk.Label(login_frame, text="İngilizce Öğrenme Asistanı",
                font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(login_frame, text="Kullanıcı Adı:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12))
        self.username_entry.pack(pady=5)

        tk.Label(login_frame, text="Şifre:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        self.password_entry = tk.Entry(login_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        button_frame = tk.Frame(login_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Giriş Yap",
                 command=self.login,
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Kayıt Ol",
                 command=self.register_screen,
                 font=("Arial", 12), bg="#2196F3", fg="white").pack(side=tk.LEFT)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect('english_learning.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            self.current_user = username
            self.score = user[2]
            c.execute("UPDATE users SET last_login=? WHERE username=?",
                     (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username))
            conn.commit()
            conn.close()
            self.create_main_menu()
        else:
            conn.close()
            messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı!")

    def register_screen(self):
        self.clear_window()

        register_frame = tk.Frame(self.root, bg="#f0f0f0")
        register_frame.pack(expand=True)

        tk.Label(register_frame, text="Yeni Kullanıcı Kaydı",
                font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(register_frame, text="Kullanıcı Adı:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        self.reg_username_entry = tk.Entry(register_frame, font=("Arial", 12))
        self.reg_username_entry.pack(pady=5)

        tk.Label(register_frame, text="Şifre:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        self.reg_password_entry = tk.Entry(register_frame, show="*", font=("Arial", 12))
        self.reg_password_entry.pack(pady=5)

        tk.Label(register_frame, text="Şifre Tekrar:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        self.reg_password_confirm_entry = tk.Entry(register_frame, show="*", font=("Arial", 12))
        self.reg_password_confirm_entry.pack(pady=5)

        button_frame = tk.Frame(register_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Kayıt Ol",
                 command=self.register,
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Geri Dön",
                 command=self.login_screen,
                 font=("Arial", 12), bg="#f44336", fg="white").pack(side=tk.LEFT)

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        password_confirm = self.reg_password_confirm_entry.get()

        if not all([username, password, password_confirm]):
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
            return

        if password != password_confirm:
            messagebox.showerror("Hata", "Şifreler eşleşmiyor!")
            return

        conn = sqlite3.connect('english_learning.db')
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password, score, last_login) VALUES (?, ?, 0, ?)",
                     (username, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            messagebox.showinfo("Başarılı", "Kayıt başarıyla oluşturuldu!")
            self.login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Hata", "Bu kullanıcı adı zaten kullanılıyor!")
        finally:
            conn.close()
    def create_main_menu(self):
        self.clear_window()

        # Üst bilgi çubuğu
        info_frame = tk.Frame(self.root, bg="#2196F3", height=50)
        info_frame.pack(fill=tk.X)
        info_frame.pack_propagate(False)

        tk.Label(info_frame, text=f"Kullanıcı: {self.current_user}",
                font=("Arial", 12), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=20)

        self.score_label = tk.Label(info_frame, text=f"Puan: {self.score}",
                                  font=("Arial", 12), bg="#2196F3", fg="white")
        self.score_label.pack(side=tk.RIGHT, padx=20)

        menu_frame = tk.Frame(self.root, bg="#f0f0f0")
        menu_frame.pack(pady=20, expand=True)

        tk.Label(menu_frame, text="İngilizce Öğrenme Asistanı",
                font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        buttons = [
            ("Cümle Kalıpları Öğrenme", self.pattern_learning_mode, "#4CAF50"),
            ("Cümle Oluşturma Alıştırması", self.sentence_building_mode, "#2196F3"),
            ("Düzensiz Fiil Alıştırması", self.irregular_verb_practice, "#FF9800"),
            ("Kelime Bilgisi Testi", self.vocabulary_test_mode, "#9C27B0"),
            ("Zamanlar ve Kullanımları", self.tenses_mode, "#00BCD4"),
            ("İnteraktif Cümle Kurma", self.interactive_sentence_mode, "#3F51B5"),
            ("Kelime Ezberleme", self.vocabulary_memorization_mode, "#009688"),
            ("İlerleme Raporu", self.progress_report, "#795548"),
            ("Çıkış", self.logout, "#f44336")
        ]

        for text, command, color in buttons:
            tk.Button(menu_frame, text=text, command=command,
                     font=("Arial", 12), width=25, height=2,
                     bg=color, fg="white",
                     activebackground=color).pack(pady=8)

    def vocabulary_memorization_mode(self):
        self.clear_window()

        memo_frame = tk.Frame(self.root, bg="#f0f0f0")
        memo_frame.pack(pady=20)

        tk.Label(memo_frame, text="Kelime Ezberleme",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Kategori seçimi
        categories = ["Düzensiz Fiiller", "Düzenli Fiiller", "Nesneler", "Yerler", "Sıfatlar"]

        self.category_var = tk.StringVar()
        self.category_var.set(categories[0])

        tk.Label(memo_frame, text="Kategori Seçin:",
                font=("Arial", 12), bg="#f0f0f0").pack()

        category_menu = ttk.Combobox(memo_frame, textvariable=self.category_var,
                                   values=categories, font=("Arial", 12))
        category_menu.pack(pady=10)

        # Kelime gösterme alanı
        self.word_frame = tk.Frame(memo_frame, bg="#ffffff", width=400, height=200)
        self.word_frame.pack(pady=20)
        self.word_frame.pack_propagate(False)

        self.word_label = tk.Label(self.word_frame, text="",
                                 font=("Arial", 16, "bold"), bg="#ffffff")
        self.word_label.pack(expand=True)

        # Kontrol butonları
        button_frame = tk.Frame(memo_frame, bg="#f0f0f0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Önceki",
                 command=lambda: self.show_word("prev"),
                 font=("Arial", 12), bg="#2196F3", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Sonraki",
                 command=lambda: self.show_word("next"),
                 font=("Arial", 12), bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Çevir",
                 command=self.toggle_translation,
                 font=("Arial", 12), bg="#FF9800", fg="white").pack(side=tk.LEFT, padx=10)

        self.current_word_index = 0
        self.showing_translation = False
        self.current_words = []

        # Kategori değişikliğini izle
        self.category_var.trace('w', self.update_word_list)

        # İlk kelime listesini yükle
        self.update_word_list()

        self.add_return_button()

    def update_word_list(self, *args):
        category = self.category_var.get()

        if category == "Düzensiz Fiiller":
            self.current_words = [(verb, f"{info['turkish']}\nPast: {info['past']}\nPast Part.: {info['past_participle']}")
                                for verb, info in self.irregular_verbs.items()]
        elif category == "Düzenli Fiiller":
            self.current_words = [(verb, turkish) for verb, turkish in self.regular_verbs.items()]
        elif category == "Nesneler":
            self.current_words = [(obj, "Türkçe karşılığı") for obj in self.vocabulary["Objects"]]
        elif category == "Yerler":
            self.current_words = [(place, "Türkçe karşılığı") for place in self.vocabulary["Places"]]
        elif category == "Sıfatlar":
            self.current_words = [(adj, "Türkçe karşılığı") for adj in self.vocabulary["Adjectives"]]

        self.current_word_index = 0
        self.showing_translation = False
        self.show_word("current")

    def show_word(self, direction):
        if not self.current_words:
            return

        if direction == "next":
            self.current_word_index = (self.current_word_index + 1) % len(self.current_words)
        elif direction == "prev":
            self.current_word_index = (self.current_word_index - 1) % len(self.current_words)

        self.showing_translation = False
        word = self.current_words[self.current_word_index][0]
        self.word_label.config(text=f"{word}\n\n{self.current_word_index + 1}/{len(self.current_words)}")

    def toggle_translation(self):
        if not self.current_words:
            return

        self.showing_translation = not self.showing_translation
        word, translation = self.current_words[self.current_word_index]

        if self.showing_translation:
            self.word_label.config(text=f"{word}\n\n{translation}")
        else:
            self.word_label.config(text=word)

    def progress_report(self):
        self.clear_window()

        report_frame = tk.Frame(self.root, bg="#f0f0f0")
        report_frame.pack(pady=20)

        tk.Label(report_frame, text="İlerleme Raporu",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Veritabanından ilerleme bilgilerini al
        conn = sqlite3.connect('english_learning.db')
        c = conn.cursor()
        c.execute("""SELECT activity, SUM(score) as total_score,
                    COUNT(*) as activity_count, MAX(date) as last_date
                    FROM progress WHERE username=?
                    GROUP BY activity""", (self.current_user,))

        progress_data = c.fetchall()
        conn.close()

        if not progress_data:
            tk.Label(report_frame, text="Henüz hiç aktivite tamamlanmamış.",
                    font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
        else:
            # Tablo başlıkları
            headers = ["Aktivite", "Toplam Puan", "Tamamlama", "Son Tarih"]
            for i, header in enumerate(headers):
                tk.Label(report_frame, text=header,
                        font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, column=i, padx=10, pady=5)

            # Tablo verileri
            for row, data in enumerate(progress_data, start=1):
                for col, value in enumerate(data):
                    tk.Label(report_frame, text=str(value),
                            font=("Arial", 12), bg="#f0f0f0").grid(row=row, column=col, padx=10, pady=5)

        self.add_return_button()

    def update_progress(self, activity, points):
        conn = sqlite3.connect('english_learning.db')
        c = conn.cursor()

        # İlerlemeyi kaydet
        c.execute("""INSERT INTO progress (username, activity, score, date)
                    VALUES (?, ?, ?, ?)""",
                 (self.current_user, activity, points, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

        # Kullanıcı puanını güncelle
        self.score += points
        c.execute("UPDATE users SET score = ? WHERE username = ?",
                 (self.score, self.current_user))

        conn.commit()
        conn.close()

        # Skor göstergesini güncelle
        if hasattr(self, 'score_label'):
            self.score_label.config(text=f"Puan: {self.score}")

    def logout(self):
        self.current_user = None
        self.score = 0
        self.login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_return_button(self):
        tk.Button(self.root, text="Ana Menüye Dön",
                 command=self.create_main_menu,
                 font=("Arial", 12), bg="#f44336", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEnglishLearningApp(root)
    root.mainloop()

# Created/Modified files during execution:
# - english_learning.db (SQLite veritabanı dosyası)

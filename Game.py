import tkinter as tk
from tkinter import ttk, messagebox
import random

class AdvancedEnglishLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gelişmiş İngilizce Öğrenme Asistanı")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Temel kelime veritabanı
        self.vocabulary = {
            "Subjects": ["I", "You", "He", "She", "It", "We", "They"],
            "Verbs": ["play", "read", "write", "speak", "eat", "drink", "sleep", "run", "walk"],
            "Objects": ["book", "game", "food", "water", "computer", "phone", "ball"],
            "Places": ["home", "school", "park", "library", "garden", "market"],
            "Time_Expressions": ["today", "tomorrow", "yesterday", "now", "every day", "sometimes"],
            "Adjectives": ["happy", "sad", "big", "small", "beautiful", "interesting", "difficult"]
        }

        # Cümle kalıpları
        self.sentence_patterns = {
            "Simple Present": {
                "pattern": "Subject + Verb(s) + Object",
                "example": "He reads a book",
                "rules": ["He/She/It -> Verb + s/es", "I/You/We/They -> Verb"]
            },
            "Present Continuous": {
                "pattern": "Subject + am/is/are + Verb(ing) + Object",
                "example": "I am reading a book",
                "rules": ["I -> am", "He/She/It -> is", "You/We/They -> are"]
            },
            "Simple Past": {
                "pattern": "Subject + Verb(ed/irregular) + Object",
                "example": "She played tennis",
                "rules": ["Regular verbs: add -ed", "Irregular verbs: special form"]
            }
        }

        self.create_main_menu()

        # Skor sistemi
        self.score = 0
        self.score_label = tk.Label(root, text=f"Puan: {self.score}",
                                  font=("Arial", 12), bg="#f0f0f0")
        self.score_label.pack(pady=10)

    def create_main_menu(self):
        menu_frame = tk.Frame(self.root, bg="#f0f0f0")
        menu_frame.pack(pady=20)

        tk.Label(menu_frame, text="İngilizce Cümle Kurma Asistanı",
                font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

        buttons = [
            ("Cümle Kalıpları Öğrenme", self.pattern_learning_mode),
            ("Cümle Oluşturma Alıştırması", self.sentence_building_mode),
            ("Kelime Bilgisi Testi", self.vocabulary_test_mode),
            ("Zamanlar ve Kullanımları", self.tenses_mode),
            ("İnteraktif Cümle Kurma", self.interactive_sentence_mode)
        ]

        for text, command in buttons:
            tk.Button(menu_frame, text=text, command=command,
                     font=("Arial", 12), width=25,
                     bg="#4CAF50", fg="white",
                     activebackground="#45a049").pack(pady=10)

    def pattern_learning_mode(self):
        self.clear_window()

        learn_frame = tk.Frame(self.root, bg="#f0f0f0")
        learn_frame.pack(pady=20)

        tk.Label(learn_frame, text="Cümle Kalıpları",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        for tense, info in self.sentence_patterns.items():
            pattern_frame = tk.Frame(learn_frame, bg="#e0e0e0", relief="raised", bd=2)
            pattern_frame.pack(pady=10, padx=20, fill="x")

            tk.Label(pattern_frame, text=tense,
                    font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=5)
            tk.Label(pattern_frame, text=f"Kalıp: {info['pattern']}",
                    font=("Arial", 12), bg="#e0e0e0").pack()
            tk.Label(pattern_frame, text=f"Örnek: {info['example']}",
                    font=("Arial", 12), bg="#e0e0e0").pack()

            rules_text = "\n".join(f"• {rule}" for rule in info['rules'])
            tk.Label(pattern_frame, text=f"Kurallar:\n{rules_text}",
                    font=("Arial", 11), bg="#e0e0e0", justify="left").pack(pady=5)

        self.add_return_button()

    def sentence_building_mode(self):
        self.clear_window()

        build_frame = tk.Frame(self.root, bg="#f0f0f0")
        build_frame.pack(pady=20)

        tk.Label(build_frame, text="Cümle Oluşturma Alıştırması",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Kelime seçme alanları
        self.subject_var = tk.StringVar()
        self.verb_var = tk.StringVar()
        self.object_var = tk.StringVar()

        # Özne seçimi
        tk.Label(build_frame, text="Özne seçin:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        ttk.Combobox(build_frame, textvariable=self.subject_var,
                    values=self.vocabulary["Subjects"]).pack(pady=5)

        # Fiil seçimi
        tk.Label(build_frame, text="Fiil seçin:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        ttk.Combobox(build_frame, textvariable=self.verb_var,
                    values=self.vocabulary["Verbs"]).pack(pady=5)

        # Nesne seçimi
        tk.Label(build_frame, text="Nesne seçin:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        ttk.Combobox(build_frame, textvariable=self.object_var,
                    values=self.vocabulary["Objects"]).pack(pady=5)

        # Cümle oluşturma butonu
        tk.Button(build_frame, text="Cümle Oluştur",
                 command=self.create_sentence,
                 font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=20)

        # Oluşturulan cümle için label
        self.sentence_label = tk.Label(build_frame, text="",
                                     font=("Arial", 14), bg="#f0f0f0", wraplength=400)
        self.sentence_label.pack(pady=10)

        self.add_return_button()

    def create_sentence(self):
        subject = self.subject_var.get()
        verb = self.verb_var.get()
        object = self.object_var.get()

        if not all([subject, verb, object]):
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        # Fiil çekimi
        if subject in ["He", "She", "It"]:
            verb += "s"

        sentence = f"{subject} {verb} the {object}."
        self.sentence_label.config(text=sentence)
        self.score += 5
        self.update_score()

    def interactive_sentence_mode(self):
        self.clear_window()

        interactive_frame = tk.Frame(self.root, bg="#f0f0f0")
        interactive_frame.pack(pady=20)

        tk.Label(interactive_frame, text="İnteraktif Cümle Kurma",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Zaman seçimi
        tk.Label(interactive_frame, text="Zaman seçin:",
                font=("Arial", 12), bg="#f0f0f0").pack()
        self.tense_var = tk.StringVar()
        ttk.Combobox(interactive_frame, textvariable=self.tense_var,
                    values=list(self.sentence_patterns.keys())).pack(pady=5)

        # Kelime seçimleri
        categories = ["Subjects", "Verbs", "Objects", "Places", "Time_Expressions", "Adjectives"]
        self.selection_vars = {}

        for category in categories:
            tk.Label(interactive_frame, text=f"{category} seçin:",
                    font=("Arial", 12), bg="#f0f0f0").pack()
            var = tk.StringVar()
            self.selection_vars[category] = var
            ttk.Combobox(interactive_frame, textvariable=var,
                        values=self.vocabulary[category]).pack(pady=5)

        tk.Button(interactive_frame, text="Gelişmiş Cümle Oluştur",
                 command=self.create_complex_sentence,
                 font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=20)

        self.complex_sentence_label = tk.Label(interactive_frame, text="",
                                             font=("Arial", 14), bg="#f0f0f0", wraplength=400)
        self.complex_sentence_label.pack(pady=10)

        self.add_return_button()

    def create_complex_sentence(self):
        tense = self.tense_var.get()
        selections = {k: v.get() for k, v in self.selection_vars.items()}

        if not all([tense] + list(selections.values())):
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return

        # Zaman yapısına göre cümle oluşturma
        if tense == "Simple Present":
            verb = selections["Verbs"]
            if selections["Subjects"] in ["He", "She", "It"]:
                verb += "s"
            sentence = f"{selections['Time_Expressions']}, {selections['Subjects']} {verb} " \
                      f"the {selections['Adjectives']} {selections['Objects']} at the {selections['Places']}."

        elif tense == "Present Continuous":
            is_are = "am" if selections["Subjects"] == "I" else \
                    "is" if selections["Subjects"] in ["He", "She", "It"] else "are"
            sentence = f"{selections['Time_Expressions']}, {selections['Subjects']} {is_are} " \
                      f"{selections['Verbs']}ing the {selections['Adjectives']} {selections['Objects']} " \
                      f"at the {selections['Places']}."

        elif tense == "Simple Past":
            # Basit geçmiş zaman için -ed eklemesi (gerçek uygulamada düzensiz fiiller için ayrı liste kullanılmalı)
            verb = selections["Verbs"] + "ed"
            sentence = f"{selections['Time_Expressions']}, {selections['Subjects']} {verb} " \
                      f"the {selections['Adjectives']} {selections['Objects']} at the {selections['Places']}."

        self.complex_sentence_label.config(text=sentence)
        self.score += 10
        self.update_score()

    def vocabulary_test_mode(self):
        self.clear_window()

        test_frame = tk.Frame(self.root, bg="#f0f0f0")
        test_frame.pack(pady=20)

        tk.Label(test_frame, text="Kelime Bilgisi Testi",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Rastgele kategori ve kelime seçimi
        category = random.choice(list(self.vocabulary.keys()))
        word = random.choice(self.vocabulary[category])

        self.current_test_word = word
        self.current_test_category = category

        tk.Label(test_frame, text=f"Bu kelime hangi kategoriye ait?\n'{word}'",
                font=("Arial", 14), bg="#f0f0f0").pack(pady=20)

        # Seçenekler için butonlar
        for cat in self.vocabulary.keys():
            tk.Button(test_frame, text=cat,
                     command=lambda c=cat: self.check_category(c),
                     font=("Arial", 12), bg="#2196F3", fg="white").pack(pady=5)

        self.add_return_button()

    def check_category(self, selected_category):
        if selected_category == self.current_test_category:
            self.score += 10
            messagebox.showinfo("Tebrikler!", "Doğru cevap!")
        else:
            self.score -= 5
            messagebox.showinfo("Yanlış", f"Doğru cevap: {self.current_test_category}")

        self.update_score()
        self.vocabulary_test_mode()

    def tenses_mode(self):
        self.clear_window()

        tenses_frame = tk.Frame(self.root, bg="#f0f0f0")
        tenses_frame.pack(pady=20)

        tk.Label(tenses_frame, text="Zamanlar ve Kullanımları",
                font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        # Her zaman için detaylı açıklama
        tenses_info = {
            "Simple Present": {
                "usage": ["Genel doğrular", "Alışkanlıklar", "Düzenli tekrarlanan eylemler"],
                "examples": ["The sun rises in the east.", "I go to school every day."]
            },
            "Present Continuous": {
                "usage": ["Şu anda olan eylemler", "Geçici durumlar", "Gelecek planları"],
                "examples": ["I am studying now.", "She is working in London this month."]
            },
            "Simple Past": {
                "usage": ["Geçmişte tamamlanmış eylemler", "Geçmişteki alışkanlıklar"],
                "examples": ["I went to school yesterday.", "She lived in Paris for 5 years."]
            }
        }

        for tense, info in tenses_info.items():
            tense_frame = tk.Frame(tenses_frame, bg="#e0e0e0", relief="raised", bd=2)
            tense_frame.pack(pady=10, padx=20, fill="x")

            tk.Label(tense_frame, text=tense,
                    font=("Arial", 14, "bold"), bg="#e0e0e0").pack(pady=5)

            tk.Label(tense_frame, text="Kullanım:",
                    font=("Arial", 12, "bold"), bg="#e0e0e0").pack()
            for usage in info["usage"]:
                tk.Label(tense_frame, text=f"• {usage}",
                        font=("Arial", 11), bg="#e0e0e0").pack()

            tk.Label(tense_frame, text="Örnekler:",
                    font=("Arial", 12, "bold"), bg="#e0e0e0").pack()
            for example in info["examples"]:
                tk.Label(tense_frame, text=f"• {example}",
                        font=("Arial", 11), bg="#e0e0e0").pack()

        self.add_return_button()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.score_label = tk.Label(self.root, text=f"Puan: {self.score}",
                                  font=("Arial", 12), bg="#f0f0f0")
        self.score_label.pack(pady=10)

    def update_score(self):
        self.score_label.config(text=f"Puan: {self.score}")

    def add_return_button(self):
        tk.Button(self.root, text="Ana Menüye Dön",
                 command=lambda: [self.clear_window(), self.create_main_menu()],
                 font=("Arial", 12), bg="#f44336", fg="white").pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedEnglishLearningApp(root)
    root.mainloop()

# Created/Modified files during execution:
# Bu uygulama herhangi bir dosya oluşturmamaktadır.

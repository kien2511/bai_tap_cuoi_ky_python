import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import random
import time

# --- File I/O functions ---

def open_file(filename):
    try:
        return open(filename, "r", encoding="utf-8")
    except FileNotFoundError:
        messagebox.showerror("Lỗi", f"Không tìm thấy file: {filename}")
        return None

def next_block(file):
    while True:
        question = file.readline()
        if question == "":
            return None, None
        question = question.strip()
        if question != "":
            break
    while True:
        answer = file.readline()
        if answer == "":
            return None, None
        answer = answer.strip()
        if answer != "":
            break
    file.readline()
    return question, answer

# --- GUI Class ---

class TriviaGUI:
    def __init__(self, master, filename):
        self.master = master
        self.master.title("🌟 Trivia Challenge 🌟")
        self.master.geometry("700x550")
        self.master.configure(bg="#fffaf0")

        self.score = 0
        self.filename = filename
        self.file = open_file(self.filename)
        if not self.file:
            self.master.destroy()
            return

        self.question, self.answer = next_block(self.file)
        if self.question is None:
            messagebox.showerror("Lỗi", "File không đúng định dạng hoặc rỗng.")
            self.master.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        self.lbl_title = tk.Label(self.master, text="🌟 Thử thách kiến thức 🌟", font=("Comic Sans MS", 22, "bold"),
                                  bg="#fffaf0", fg="#ff4500")
        self.lbl_title.pack(pady=15)

        self.frame = tk.Frame(self.master, bg="#fffaf0")
        self.frame.pack(pady=10)

        self.lbl_score = tk.Label(self.frame, text=f"⭐ Điểm: {self.score}", font=("Verdana", 13, "bold"),
                                  bg="#fffaf0", fg="#228b22")
        self.lbl_score.pack(pady=5)

        self.lbl_question = tk.Label(self.frame, text=self.question, wraplength=600, font=("Helvetica", 15),
                                     bg="#fffaf0", fg="#000080", justify="center")
        self.lbl_question.pack(pady=15)

        self.entry_answer = tk.Entry(self.frame, font=("Helvetica", 13), width=45, justify="center", bd=4, relief="sunken")
        self.entry_answer.pack(pady=10)
        self.entry_answer.bind("<Return>", lambda e: self.submit_answer())
        self.entry_answer.focus()

        self.button_frame = tk.Frame(self.master, bg="#fffaf0")
        self.button_frame.pack(pady=15)

        self.btn_submit = tk.Button(self.button_frame, text="✅ Nộp", font=("Helvetica", 13, "bold"),
                                    command=self.submit_answer, bg="#4CAF50", fg="white", width=14, height=2)
        self.btn_submit.grid(row=0, column=0, padx=15)

        self.btn_end = tk.Button(self.button_frame, text="⛔ Kết thúc", font=("Helvetica", 13, "bold"),
                                 command=self.end_game, bg="#f44336", fg="white", width=14, height=2)
        self.btn_end.grid(row=0, column=1, padx=15)

        self.canvas = tk.Canvas(self.master, width=700, height=180, bg="#fffaf0", highlightthickness=0)
        self.canvas.pack()

    def submit_answer(self):
        user_answer = self.entry_answer.get().strip()
        if user_answer.lower() == self.answer.lower():
            self.score += 1
            self.lbl_score.config(text=f"⭐ Điểm: {self.score}")
            self.animated_correct_feedback()
        else:
            messagebox.showinfo("❌ Sai rồi!", f"Đáp án đúng là: {self.answer}")
        self.next_question()

    def animated_correct_feedback(self):
        for i in range(5):
            self.master.update()
            self.lbl_question.config(fg=random.choice(["green", "blue", "orange", "purple"]))
            time.sleep(0.1)
        self.lbl_question.config(fg="#000080")
        messagebox.showinfo("🖊️ Đúng rồi!", "Chính xác! Bạn thật tuyệt!")

    def next_question(self):
        self.question, self.answer = next_block(self.file)
        if self.question is None:
            self.end_game()
        else:
            self.lbl_question.config(text=self.question)
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.focus()

    def end_game(self):
        self.canvas.delete("all")
        self.canvas.create_text(350, 90, text=f"🏁 Trò chơi kết thúc! Điểm số: {self.score}", font=("Helvetica", 18, "bold"),
                                fill="#8b0000")
        self.master.after(1500, self.master.destroy)
        if self.file:
            self.file.close()

# --- Main ---

if __name__ == "__main__":
    root = tk.Tk()
    filename = simpledialog.askstring("📂 File câu hỏi", "Nhập tên file câu hỏi:", initialvalue="trivia.txt")
    if filename:
        app = TriviaGUI(root, filename)
        root.mainloop()
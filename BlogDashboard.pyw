import os
import subprocess
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

# Configuration
BLOG_DIR = os.path.expanduser(r"~\Documents\EchoNomad26.github.io")
POSTS_DIR = os.path.join(BLOG_DIR, "content", "blog")

class BlogDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("EchoNomad Dashboard")
        self.root.geometry("680x450")
        self.root.configure(bg="#121212")
        
        # UI Styling
        self.bg_color = "#121212"
        self.fg_color = "#e0e0e0"
        self.btn_bg = "#2a2a2a"
        self.accent_color = "#005f00"
        self.font_main = ("Consolas", 11)
        
        # Header
        header = tk.Label(root, text="EchoNomad Archive", bg=self.bg_color, fg=self.fg_color, font=("Consolas", 16, "bold"))
        header.pack(pady=(15, 10))
        
        # Listbox for posts
        self.listbox = tk.Listbox(root, bg="#1e1e1e", fg=self.fg_color, font=self.font_main, 
                                  selectbackground="#404040", relief=tk.FLAT, highlightthickness=1, highlightcolor="#333")
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.listbox.bind('<Double-1>', lambda x: self.edit_post())
        
        # Buttons Frame
        btn_frame = tk.Frame(root, bg=self.bg_color)
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Action Buttons
        btn_opts = {"bg": self.btn_bg, "fg": self.fg_color, "relief": tk.FLAT, "font": self.font_main, "cursor": "hand2", "padx": 10, "pady": 5}
        
        tk.Button(btn_frame, text="✍️ New", command=self.new_post, **btn_opts).pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="📤 Upload", command=self.upload_post, **btn_opts).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="📝 Edit", command=self.edit_post, **btn_opts).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Delete", command=self.delete_post, **btn_opts).pack(side=tk.LEFT, padx=5)
        
        publish_btn = tk.Button(btn_frame, text="🚀 Sync to GitHub", command=self.publish, 
                                bg=self.accent_color, fg="white", relief=tk.FLAT, font=("Consolas", 11, "bold"), cursor="hand2", padx=10, pady=5)
        publish_btn.pack(side=tk.RIGHT)
        
        self.load_posts()

    def load_posts(self):
        self.listbox.delete(0, tk.END)
        if not os.path.exists(POSTS_DIR):
            return
        # List all markdown files, newest first
        files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith('.md')], reverse=True)
        for f in files:
            self.listbox.insert(tk.END, f" {f}")

    def new_post(self):
        slug = simpledialog.askstring("New Post", "Enter a short URL slug (e.g., daily-thought):", parent=self.root)
        if not slug: return
        
        slug = slug.strip().lower().replace(" ", "-")
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.md"
        
        os.chdir(BLOG_DIR)
        subprocess.run(["hugo", "new", f"blog/{filename}"], shell=True)
        
        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.exists(filepath):
            # Auto-remove draft status
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            content = content.replace("draft: true", "draft: false")
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)
            
            self.load_posts()
            subprocess.Popen(["notepad.exe", filepath])

    def upload_post(self):
        source_path = filedialog.askopenfilename(
            title="Select Markdown File to Upload",
            filetypes=[("Markdown Files", "*.md"), ("Text Files", "*.txt"), ("All Files", "*.*")],
            parent=self.root
        )
        if not source_path: return
        
        filename = os.path.basename(source_path)
        destination_path = os.path.join(POSTS_DIR, filename)
        
        # Prevent accidental overwriting
        if os.path.exists(destination_path):
            if not messagebox.askyesno("File Exists", f"'{filename}' already exists in your archive. Overwrite it?"):
                return
                
        try:
            shutil.copy2(source_path, destination_path)
            self.load_posts()
            messagebox.showinfo("Success", f"Successfully imported '{filename}'!")
        except Exception as e:
            messagebox.showerror("Import Error", f"Could not copy the file:\n{e}")

    def edit_post(self):
        selection = self.listbox.curselection()
        if not selection: return
        filename = self.listbox.get(selection[0]).strip()
        filepath = os.path.join(POSTS_DIR, filename)
        subprocess.Popen(["notepad.exe", filepath])

    def delete_post(self):
        selection = self.listbox.curselection()
        if not selection: return
        filename = self.listbox.get(selection[0]).strip()
        if messagebox.askyesno("Confirm Delete", f"Permanently delete '{filename}'?"):
            os.remove(os.path.join(POSTS_DIR, filename))
            self.load_posts()

    def publish(self):
        os.chdir(BLOG_DIR)
        self.root.config(cursor="watch")
        self.root.update()
        
        try:
            subprocess.run(["git", "add", "."], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["git", "commit", "-m", f"Dashboard UI sync: {datetime.now().strftime('%Y-%m-%d %H:%M')}"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            subprocess.run(["git", "push", "origin", "main"], shell=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW)
            messagebox.showinfo("Success", "All changes published to GitHub successfully!")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "Failed to sync with GitHub. Check your connection.")
        finally:
            self.root.config(cursor="")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogDashboard(root)
    root.mainloop()
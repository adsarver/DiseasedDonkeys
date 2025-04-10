import tkinter as tk
from threading import Thread
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import queue, os

DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user = Column(String(255), nullable=False)

Base.metadata.create_all(engine)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Add User to MySQL")

        self.label = tk.Label(root, text="Enter a username:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        self.button = tk.Button(root, text="Add User", command=self.start_add_user_thread)
        self.button.pack(pady=10)

        self.status = tk.Label(root, text="", fg="blue")
        self.status.pack()

        self.result_queue = queue.Queue()
        self.root.after(100, self.check_result_queue)

    def start_add_user_thread(self):
        username = self.entry.get().strip()
        if username:
            thread = Thread(target=self.add_user_to_db, args=(username,))
            thread.start()
        else:
            self.status.config(text="Please enter a username", fg="red")

    def add_user_to_db(self, username):
        try:
            session = Session()
            new_user = User(user=username)
            session.add(new_user)
            session.commit()
            session.close()
            self.result_queue.put("User added successfully!")
        except Exception as e:
            self.result_queue.put(f"Error: {e}")

    def check_result_queue(self):
        try:
            result = self.result_queue.get_nowait()
            self.status.config(text=result, fg="green" if "successfully" in result else "red")
        except queue.Empty:
            pass
        self.root.after(100, self.check_result_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
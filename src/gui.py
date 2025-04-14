import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

requests = []
request_id_counter = 1

def add_request(user, description, room):
    global request_id_counter
    request = {
        'id': request_id_counter,
        'user': user,
        'status': 'Incomplete',
        'request_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'complete_time': '',
        'description': description,
        'room': room,
        'assignee': ''
    }
    requests.append(request)
    request_id_counter += 1

def show_main():
    def refresh_student_tree():
        for i in student_tree.get_children():
            student_tree.delete(i)
        for req in requests:
            if req['user'] == student_user.get():
                student_tree.insert('', 'end', values=(req['id'], req['status'], req['request_time'], req['complete_time'], req['description'], req['room']))

    def refresh_worker_tree(filtered_only=False):
        for i in worker_tree.get_children():
            worker_tree.delete(i)
        for req in requests:
            if filtered_only and req['assignee'] != worker_name.get():
                continue
            if worker_filter.get().strip() and worker_filter.get().strip() not in req['assignee']:
                continue
            worker_tree.insert('', 'end', values=(req['id'], req['status'], req['request_time'], req['complete_time'], req['description'], req['room'], req['assignee']))

    def submit_request():
        user = student_user.get().strip()
        desc = desc_entry.get("1.0", "end").strip()
        room = room_entry.get().strip()
        if user and desc and room:
            add_request(user, desc, room)
            desc_entry.delete("1.0", "end")
            room_entry.delete(0, "end")
            refresh_student_tree()
        else:
            messagebox.showerror("Input Error", "All fields must be filled.")

    def update_complete_time():
        selected = worker_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a request.")
            return
        for item in selected:
            item_id = int(worker_tree.item(item)['values'][0])
            for req in requests:
                if req['id'] == item_id:
                    req['complete_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        refresh_worker_tree(filtered_only=filter_var.get())

    def assign_self():
        selected = worker_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a request.")
            return
        assignee = worker_name.get().strip()
        if not assignee:
            messagebox.showwarning("No Name", "Enter your name to assign yourself.")
            return
        for item in selected:
            item_id = int(worker_tree.item(item)['values'][0])
            for req in requests:
                if req['id'] == item_id:
                    req['assignee'] = assignee
        refresh_worker_tree(filtered_only=filter_var.get())

    def sort_worker_tree(col):
        global requests
        requests.sort(key=lambda x: x[col.lower().replace(' ', '_')])
        refresh_worker_tree(filtered_only=filter_var.get())

    def on_student_name_change(event):
        refresh_student_tree()

    def on_worker_input_change(event):
        refresh_worker_tree(filtered_only=filter_var.get())

    def on_tab_changed(event):
        selected_tab = event.widget.tab(event.widget.index("current"))['text']
        if selected_tab == 'Worker View':
            refresh_worker_tree(filtered_only=filter_var.get())

    main_window = tk.Tk()
    main_window.title("Request System")

    tab_control = ttk.Notebook(main_window)
    tab_control.bind("<<NotebookTabChanged>>", on_tab_changed)

    student_tab = ttk.Frame(tab_control)
    tab_control.add(student_tab, text='Student View')

    tk.Label(student_tab, text="Your Name:").pack(pady=5)
    student_user = tk.Entry(student_tab)
    student_user.pack(pady=5)
    student_user.bind("<KeyRelease>", on_student_name_change)

    tk.Label(student_tab, text="Description:").pack(pady=5)
    desc_entry = tk.Text(student_tab, height=4, width=40)
    desc_entry.pack(pady=5)

    tk.Label(student_tab, text="Room:").pack(pady=5)
    room_entry = tk.Entry(student_tab)
    room_entry.pack(pady=5)

    tk.Button(student_tab, text="Submit Request", command=submit_request).pack(pady=10)

    tk.Label(student_tab, text="Your Requests:").pack(pady=5)
    student_tree = ttk.Treeview(student_tab, columns=('ID', 'Status', 'Request Time', 'Complete Time', 'Description', 'Room'), show='headings')
    for col in ('ID', 'Status', 'Request Time', 'Complete Time', 'Description', 'Room'):
        student_tree.heading(col, text=col)
        student_tree.column(col, width=120)
    student_tree.pack(pady=10, fill='x')

    worker_tab = ttk.Frame(tab_control)
    tab_control.add(worker_tab, text='Worker View')

    tk.Label(worker_tab, text="Your Name:").pack(pady=5)
    worker_name = tk.Entry(worker_tab)
    worker_name.pack(pady=5)
    worker_name.bind("<KeyRelease>", on_worker_input_change)

    tk.Label(worker_tab, text="Filter by Assignee:").pack(pady=5)
    worker_filter = tk.Entry(worker_tab)
    worker_filter.pack(pady=5)
    worker_filter.bind("<KeyRelease>", on_worker_input_change)

    filter_var = tk.BooleanVar()

    columns = ('ID', 'Status', 'Request Time', 'Complete Time', 'Description', 'Room', 'Assignee')
    worker_tree = ttk.Treeview(worker_tab, columns=columns, show='headings')
    for col in columns:
        worker_tree.heading(col, text=col, command=lambda c=col: sort_worker_tree(c))
        worker_tree.column(col, width=120)
    worker_tree.pack(pady=10, fill='x')

    tk.Button(worker_tab, text="Set Complete Time", command=update_complete_time).pack(pady=5)
    tk.Button(worker_tab, text="Assign Myself", command=assign_self).pack(pady=5)

    tab_control.pack(expand=1, fill='both')
    refresh_worker_tree()
    main_window.mainloop()

show_main()
import os
import shutil
import subprocess
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox, ttk

# 전역 변수로 폴더 경로를 저장
folder_selected = ''

def get_git_branches():
    global folder_selected
    branches = []
    try:
        result = subprocess.run(['git', 'branch', '-a'], cwd=folder_selected, capture_output=True, text=True)
        if result.returncode == 0:
            branches_raw = result.stdout.split('\n')
            for branch in branches_raw:
                branch = branch.strip()
                if branch.startswith('remotes/'):
                    branch = branch.split('/', 2)[-1]
                branches.append(branch)
            branches = list(set(branches))  # 중복 제거
    except Exception as e:
        messagebox.showerror("Error", f"Failed to list branches: {e}")
    return branches

def install_pre_commit_hook():
    global folder_selected
    current_dir = os.path.dirname(os.path.realpath(__file__))
    pre_commit_script_path = os.path.join(current_dir, 'pre-commit.py')
    git_hooks_path = os.path.join(folder_selected, '.git', 'hooks')
    target_pre_commit_path = os.path.join(git_hooks_path, 'pre-commit')

    if os.path.isfile(pre_commit_script_path):
        shutil.copy(pre_commit_script_path, target_pre_commit_path)
        os.chmod(target_pre_commit_path, 0o775)
        messagebox.showinfo("Success", "Pre-commit hook installed successfully.")
    else:
        messagebox.showerror("Error", "pre-commit.py not found.")

def git_add():
    global folder_selected
    subprocess.run(['git', 'add', '.'], cwd=folder_selected)
    messagebox.showinfo("Success", "All changes added to git.")

def git_commit():
    global folder_selected
    commit_message = simpledialog.askstring("Input", "Enter commit message:")
    if commit_message:
        result = subprocess.run(['git', 'commit', '-m', commit_message], cwd=folder_selected, text=True, capture_output=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", "Commit successful.")
        else:
            messagebox.showerror("Error", "Commit failed.\n" + result.stderr)

def git_push(branch):
    global folder_selected
    if not branch:
        messagebox.showwarning("Warning", "No branch selected for push.")
        return
    try:
        result = subprocess.run(['git', 'push', 'origin', branch], cwd=folder_selected, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Success", "Push successful.")
        else:
            messagebox.showerror("Error", f"Push failed:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to push: {e}")

def browse_files(listbox, text_area, branch_combobox):
    global folder_selected
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        listbox.delete(0, END)
        for file in os.listdir(folder_selected):
            if os.path.isfile(os.path.join(folder_selected, file)):
                listbox.insert(END, file)
        listbox.bind('<<ListboxSelect>>', lambda event: display_file_content(event, text_area))

        # Git 브랜치 목록 업데이트
        try:
            result = subprocess.run(['git', 'branch', '-a'], cwd=folder_selected, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, universal_newlines=True)
            if result.returncode == 0:
                branches_raw = result.stdout.split('\n')
                branches = [branch.strip() for branch in branches_raw if branch.strip()]
                local_branches = [branch.replace('* ', '') for branch in branches if not branch.startswith('remotes/')]
                branch_combobox['values'] = local_branches
                if local_branches:
                    branch_combobox.current(0)
            else:
                messagebox.showerror("Error", "Failed to fetch branches.\n" + result.stderr)
                branch_combobox['values'] = []
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while fetching branches: {e}")
            branch_combobox['values'] = []


def display_file_content(event, text_area):
    global folder_selected
    widget = event.widget
    selection = widget.curselection()
    file_name = widget.get(selection[0])
    file_path = os.path.join(folder_selected, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        text_area.delete(1.0, END)
        text_area.insert(END, content)

def main():
    root = Tk()
    root.title("Git Helper")

    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    listbox = Listbox(frame, width=50, height=15)
    listbox.pack(side=LEFT, fill=BOTH)

    text_area = Text(frame, width=50, height=15)
    text_area.pack(side=RIGHT, fill=BOTH)

    button_frame = Frame(root)
    button_frame.pack(padx=10, pady=10)

    branch_label = Label(button_frame, text="Branch:")
    branch_label.pack(side=LEFT)
    branch_combobox = ttk.Combobox(button_frame, width=15)
    branch_combobox.pack(side=LEFT, padx=5)
    Button(button_frame, text="Git push", command=lambda: git_push(branch_combobox.get())).pack(side=LEFT)

    Button(button_frame, text="Open Folder", command=lambda: browse_files(listbox, text_area, branch_combobox)).pack(side=LEFT)
    Button(button_frame, text="Install pre-commit", command=install_pre_commit_hook).pack(side=LEFT)
    Button(button_frame, text="Git Add", command=git_add).pack(side=LEFT)
    Button(button_frame, text="Git Commit", command=git_commit).pack(side=LEFT)
    Button(button_frame, text="Git push", command=git_push).pack(side=LEFT)

    root.mainloop()

if __name__ == "__main__":
    main()

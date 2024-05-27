from git import Repo
import subprocess

def getCommand(command):
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.strip()
    return output

def createRepo():
    repo = Repo.init("/home/student/Desktop/Lab5Midterm")

    add_file = ['/home/student/Desktop/Lab5Midterm/snmp.txt', '/home/student/Desktop/Lab5Midterm/image.jpg']

    repo.index.add(add_file)

    repo.index.commit("Added files")

    origin = repo.create_remote('origin', "https://github.com/Logan-Chayet/Lab5.git")
    repo.git.push("--set-upstream", origin, "master")

def pushModified():
    repo = Repo("/home/student/Desktop/Lab5Midterm")

    # Check for modified files
    files_changed = [i.a_path for i in repo.index.diff(None)]

    # Push modified files to GitHub
    if files_changed:
        repo.index.add(files_changed)
        repo.index.commit("Modified Files")
        getCommand(["git","push", "-f", "origin", "main"])


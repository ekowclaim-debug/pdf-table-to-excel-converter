import os
import subprocess
import sys

# =========================================================
# CONFIGURATION
# =========================================================

PROJECT_PATH = r"C:\Users\chron\OneDrive\Desktop\time"

REPO_URL = "https://github.com/ekowclaim-debug/pdf-table-to-excel-converter.git"

COMMIT_MESSAGE = "Upload project to GitHub"


# =========================================================
# RUN COMMAND
# =========================================================

def run_command(command, allow_error=False):
    print("\n" + "=" * 60)
    print("RUNNING:")
    print(" ".join(command))
    print("=" * 60)

    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_PATH,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace"
        )

        if result.stdout.strip():
            print(result.stdout.strip())

        if result.stderr.strip():
            print(result.stderr.strip())

        if result.returncode != 0 and not allow_error:
            print(f"\n❌ COMMAND FAILED WITH CODE: {result.returncode}")
            sys.exit(1)

        return result

    except FileNotFoundError:
        print("\n❌ Git was not found.")
        print("Please install Git and restart your CMD/terminal.")
        sys.exit(1)


# =========================================================
# CHECK PROJECT FOLDER
# =========================================================

if not os.path.isdir(PROJECT_PATH):
    print("\n❌ PROJECT FOLDER NOT FOUND:")
    print(PROJECT_PATH)
    sys.exit(1)

print("\n" + "=" * 60)
print("GITHUB PROJECT UPLOADER")
print("=" * 60)

print(f"\nProject: {PROJECT_PATH}")
print(f"Repository: {REPO_URL}")


# =========================================================
# CHECK GIT
# =========================================================

git_check = subprocess.run(
    ["git", "--version"],
    text=True,
    capture_output=True
)

if git_check.returncode != 0:
    print("\n❌ Git is not installed or is not available in PATH.")
    sys.exit(1)

print(f"\nGit: {git_check.stdout.strip()}")


# =========================================================
# INITIALIZE GIT
# =========================================================

git_folder = os.path.join(PROJECT_PATH, ".git")

if not os.path.isdir(git_folder):

    print("\nInitializing Git repository...")
    run_command(["git", "init"])

else:
    print("\n✓ Git repository already initialized.")


# =========================================================
# CONFIGURE USER IDENTITY IF NEEDED
# =========================================================

print("\nChecking Git user configuration...")

name_result = run_command(
    ["git", "config", "user.name"],
    allow_error=True
)

email_result = run_command(
    ["git", "config", "user.email"],
    allow_error=True
)

if name_result.returncode != 0 or not name_result.stdout.strip():

    print("\n⚠ Git user name is not configured.")

    name = input("Enter your Git name: ").strip()

    if not name:
        print("❌ Git name cannot be empty.")
        sys.exit(1)

    run_command(["git", "config", "user.name", name])


if email_result.returncode != 0 or not email_result.stdout.strip():

    print("\n⚠ Git email is not configured.")

    email = input("Enter your Git email: ").strip()

    if not email:
        print("❌ Git email cannot be empty.")
        sys.exit(1)

    run_command(["git", "config", "user.email", email])


# =========================================================
# SET REMOTE
# =========================================================

print("\nChecking GitHub remote...")

remote_result = run_command(
    ["git", "remote", "get-url", "origin"],
    allow_error=True
)

if remote_result.returncode == 0:

    print("\nUpdating existing origin...")
    run_command(
        ["git", "remote", "set-url", "origin", REPO_URL]
    )

else:

    print("\nAdding origin...")
    run_command(
        ["git", "remote", "add", "origin", REPO_URL]
    )


# =========================================================
# ADD ALL FILES
# =========================================================

print("\nAdding project files...")

run_command(["git", "add", "."])


# =========================================================
# CHECK STATUS
# =========================================================

run_command(["git", "status"])


# =========================================================
# COMMIT
# =========================================================

print("\nCreating commit...")

commit_result = run_command(
    ["git", "commit", "-m", COMMIT_MESSAGE],
    allow_error=True
)

commit_output = (
    commit_result.stdout +
    commit_result.stderr
).lower()


if commit_result.returncode != 0:

    if "nothing to commit" in commit_output:

        print("\n✓ No new changes to commit.")

    else:

        print("\n❌ COMMIT FAILED.")
        print("\nPlease copy the error above and send it to me.")
        sys.exit(1)


# =========================================================
# SET MAIN BRANCH
# =========================================================

print("\nSetting branch to main...")

run_command(["git", "branch", "-M", "main"])


# =========================================================
# SHOW REMOTE
# =========================================================

print("\nChecking remote connection...")

run_command(["git", "remote", "-v"])


# =========================================================
# PUSH TO GITHUB
# =========================================================

print("\nPushing project to GitHub...")

push_result = run_command(
    ["git", "push", "-u", "origin", "main"],
    allow_error=True
)


if push_result.returncode != 0:

    print("\n" + "=" * 60)
    print("❌ GITHUB PUSH FAILED")
    print("=" * 60)

    print("\nMost likely reasons:")
    print("1. GitHub authentication is required.")
    print("2. The repository does not exist.")
    print("3. You do not have access to the repository.")
    print("4. The repository URL is incorrect.")
    print("5. A file exceeds GitHub's 100 MB limit.")

    print("\nIMPORTANT:")
    print("Copy the exact error shown above and send it to me.")

    sys.exit(1)


# =========================================================
# SUCCESS
# =========================================================

print("\n" + "=" * 60)
print("✅ SUCCESS!")
print("YOUR PROJECT HAS BEEN PUSHED TO GITHUB.")
print("=" * 60)

print(f"\nGitHub Repository:")
print(REPO_URL)
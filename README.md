# 2605_DS5111_xdy6sg

Setup automation for a DS5111 development VM. These scripts take a fresh
Ubuntu VM to a working Python environment backed by GitHub, so the machine
can be recreated quickly if the cloud instance is lost.

## Starting point (assumptions)

This guide assumes the AWS VM already exists. Before running anything below,
you should have:

- A running Ubuntu Server 26.04 VM that you can SSH into.
- An SSH key on the VM registered with your GitHub account.

Verify the GitHub connection with:

    ssh -T git@github.com

You should see: `Hi <username>! You've successfully authenticated...`

## Setup steps

1. **Clone this repository**

       git clone git@github.com:sportsanalystf/2605_DS5111_xdy6sg.git
       cd 2605_DS5111_xdy6sg

2. **Provision the VM**

   Installs `make`, Python virtual environment support, and `tree`.

       bash scripts/init.sh

   Quick test: run `tree`. If it lists files instead of returning
   "command not found", the install worked.

3. **Configure git credentials**

   Sets the global git user so commits are tagged with your name and email.

       bash scripts/init_git_creds.sh

   Quick test: the script echoes `user.email` and `user.name` to the
   console after running.

   Note: a new user should edit `scripts/init_git_creds.sh` and replace
   the `USER` and `NAME` values with their own GitHub email and username
   before running it.

4. **Build the Python virtual environment**

   Creates the `env/` virtual environment and installs the packages
   listed in `requirements.txt`.

       make update

   Quick test:

       . env/bin/activate
       pip list

   The prompt should now show `(env)` on the left, and `pip list`
   should include `pandas` and `numpy`.

## Repository contents

- `scripts/init.sh` — installs base system packages (make, venv, tree)
- `scripts/init_git_creds.sh` — sets git global user configuration
- `makefile` — builds the Python virtual environment
- `requirements.txt` — Python package list
- `.gitignore` — excludes the generated `env/` directory from git

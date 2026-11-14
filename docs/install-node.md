# Install Node.js, npm, and npx

You do not need a separate npx installation. Install a supported Node.js **LTS**
release with npm; npm includes npx.

## macOS

1. Open the [official Node.js download page](https://nodejs.org/en/download).
2. Select an LTS release and the macOS installer (`.pkg`) for your Mac.
3. Run the installer and complete setup.
4. Close and reopen your terminal. Restart Orca if it was already running.

## Windows: native installation

1. Open the [official Node.js download page](https://nodejs.org/en/download).
2. Select an LTS release and the Windows installer (`.msi`) for your computer.
3. Run the installer with the default npm and PATH options enabled.
4. Open a new PowerShell or Command Prompt window. Restart Orca if it was
   already running.

If your agent runs inside **WSL**, follow the Linux instructions inside WSL
instead. A native Windows installation does not replace the Linux installation
used by that agent.

## Linux, including Ubuntu in WSL

Use nvm to install Node.js for your user. Run the following in Bash or Zsh.
You need curl and Bash. If curl is missing, install it using your distribution's
package manager; on Ubuntu/Debian:

```bash
sudo apt update
sudo apt install curl ca-certificates
```

Install nvm using its official installer, then install Node.js LTS:

```bash
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh | bash
source "$HOME/.nvm/nvm.sh"
nvm install --lts
```

The installer configures your shell profile. Open a new terminal and repeat the
checks below to confirm the setup is available in a fresh session. If nvm is not
loaded in that session, follow its [shell setup troubleshooting](https://github.com/nvm-sh/nvm#troubleshooting-on-linux).

## Verify the installation

Run these commands in the same environment where your agent runs:

```bash
node --version
npm --version
npx --version
```

Each command should print a version number. If a command is not found, reopen
the terminal and check that Node.js is installed in that environment and on
its PATH.

If PowerShell blocks `npm.ps1` or `npx.ps1`, use their command-file entrypoints
without changing the execution policy:

```powershell
npm.cmd --version
npx.cmd --version
```

You can likewise replace `npx` with `npx.cmd` in the skill commands below.

## Check the course repository

List the available skills without installing any:

```bash
npx skills add mbk-dev/ai-learning --list
```

On the first run, npx may ask to download the Skills CLI package. Confirm the
package prompt to proceed.

Then follow the [skill installation instructions](../README.md#installation)
for your agent. For example, install the commit skill globally for Codex:

```bash
npx skills add mbk-dev/ai-learning --skill commit -g -a codex
```

Use `-a claude-code` for Claude Code or `-a opencode` for OpenCode. Omit `-g`
for project-only installation. Review any existing skill with the same name
before replacing it.

## Official references

- [npm: downloading and installing Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm/)
- [Node.js downloads](https://nodejs.org/en/download)
- [nvm installation and updates](https://github.com/nvm-sh/nvm#installing-and-updating)

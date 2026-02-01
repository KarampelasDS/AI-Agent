# AI Agent

This project features an AI agent (powered by Gemini) designed to assist with coding tasks, navigating the project's file system, and executing Python scripts. All from the comfort of your terminal.

## Capabilities:

The agent is equipped with a set of tools to manage the coding environment:

- **List Files and Directories:** Can list the contents of any directory, providing an overview of the project structure, including file sizes and whether an item is a file or a directory.
- **Read File Contents:** Can read and display the content of any specified file.
- **Execute Python Files:** Can run Python scripts directly, making it easy to test code or automate tasks.
- **Write or Overwrite Files:** Can create new files or update existing ones with the content provided.

## How the Agent Can Help:

- **Project Navigation:** Easily explore the project's file system.
- **Code Inspection:** Quickly view the contents of source files.
- **Script Execution:** Run Python scripts without leaving the conversation.
- **File Management:** Create or modify files as needed.

The agent is designed to make the coding experience smoother and more efficient.

## Environment Variables

This project uses environment variables for configuration. You need to set the following variables in a `.env` file in the root directory:

- `GEMINI_API_KEY`: Your API key for the Gemini service.
- `WORKING_DIRECTORY`: The working directory for the AI agent. If not set, it defaults to `./calculator`, which contains a test project for the AI agent.

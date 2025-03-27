package main

import (
	"fmt"
	"os"
	"os/exec"
	"strings"
)

const (
	DefaultEditor  = "micro"
	DefaultBrowser = "glow"
	DailyNotesPath = "DIARY"
	Version        = "0.8.0"
)

func main() {
	// Handle options
	if len(os.Args) > 1 {
		switch os.Args[1] {
		case "-h", "--help", "-H":
			printHelp()
			return
		case "-v", "--version", "-V":
			printVersion()
			return
		default:
			fmt.Println("Unknown Option:", os.Args[1])
			printHelp()
			return
		}
	}

	// Post-options flow
	printStashes()
	printChanges()
	promptMain()
}

func printHelp() {
	fmt.Println("Usage: ./start.go [OPTION]")
	fmt.Println("Options: [-h | --help | -H] [-v | --version | -V]")
}

func printVersion() {
	commitHash := getGitCommitHash()
	compiled := getGitCompiledDate()
	fmt.Printf("GitLite %s\n", Version)
	fmt.Println("Author: Tom Scott (tmscott88)")
	fmt.Printf("Commit Hash: %s\n", commitHash)
	fmt.Printf("Compiled: %s\n", compiled)
}

func getGitCommitHash() string {
	cmd := exec.Command("git", "log", "--oneline", "-n", "1")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println("Error getting commit hash:", err)
		return ""
	}
	return strings.TrimSpace(string(output[:7]))
}

func getGitCompiledDate() string {
	cmd := exec.Command("git", "show", "-s", "--format=%cD")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println("Error getting compiled date:", err)
		return ""
	}
	return strings.TrimSpace(strings.Split(string(output), " -")[0])
}

func printChanges() {
	if hasChanges() {
		fmt.Println("\n---Changes---")
		cmd := exec.Command("git", "status", "--short")
		output, err := cmd.Output()
		if err != nil {
			fmt.Println("Error getting git status:", err)
			return
		}
		fmt.Println(string(output))
		fmt.Println("-------------")
	}
}

func hasChanges() bool {
	cmd := exec.Command("git", "status", "--porcelain")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println("Error checking for changes:", err)
		return false
	}
	return len(output) > 0
}

func printStashes() {
	if hasStashes() {
		fmt.Println("\n---Stashes---")
		cmd := exec.Command("git", "stash", "list")
		output, err := cmd.Output()
		if err != nil {
			fmt.Println("Error getting stash list:", err)
			return
		}
		fmt.Println(string(output))
		fmt.Println("-------------")
	}
}

func hasStashes() bool {
	cmd := exec.Command("git", "stash", "list")
	output, err := cmd.Output()
	if err != nil {
		fmt.Println("Error checking for stashes:", err)
		return false
	}
	return len(output) > 0
}

func promptMain() {
	for {
		fmt.Println("\nChoose an option:")
		options := []string{"Start", "Fetch", "Log", "Diff", "Pull", "Push", "Stage", "Commit", "Stash", "Revert", "Discard", "Reset", "Quit"}
		for i, option := range options {
			fmt.Printf("%d. %s\n", i+1, option)
		}

		var choice int
		fmt.Print("Enter choice: ")
		fmt.Scanf("%d", &choice)

		switch choice {
		case 1:
			promptStart()
		case 2:
			fetchGitStatus()
		case 3:
			promptLog()
		case 4:
			showDiff()
		case 5:
			executeGitCommand("git", "pull")
		case 6:
			executeGitCommand("git", "push")
		case 7:
			promptStage()
		case 8:
			promptCommit()
		case 9:
			promptStash()
		case 10:
			executeGitCommand("git", "checkout", "-p")
		case 11:
			discardUntrackedFiles()
		case 12:
			promptReset()
		case 13:
			return
		default:
			fmt.Println("Invalid choice.")
		}
	}
}

func executeGitCommand(args ...string) {
	cmd := exec.Command(args[0], args[1:]...)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		fmt.Printf("Error executing command: %v\n", err)
	}
}

func promptStart() {
	// Simulate sub-menu prompt for 'Start' option
	options := []string{"New", "Resume", "Browse", "Daily-Note", "Cancel"}
	for {
		fmt.Println("\nChoose an option:")
		for i, option := range options {
			fmt.Printf("%d. %s\n", i+1, option)
		}

		var choice int
		fmt.Print("Enter choice: ")
		fmt.Scanf("%d", &choice)

		switch choice {
		case 1:
			executeGitCommand(DefaultEditor)
		case 2:
			// Placeholder for resume functionality
			fmt.Println("Resume functionality to be implemented.")
		case 3:
			executeGitCommand(DefaultBrowser)
		case 4:
			// Open the daily note in the default editor
			openDailyNote()
		case 5:
			return
		default:
			fmt.Println("Invalid choice.")
		}
	}
}

func openDailyNote() {
	path := fmt.Sprintf("%s/%s/%s.md", DailyNotesPath, getCurrentYearMonth(), getCurrentDate())
	executeGitCommand(DefaultEditor, path)
}

func getCurrentYearMonth() string {
	// Use Go's time package to get the current year and month
	return "2025-03" // For now, hardcoding it
}

func getCurrentDate() string {
	// Use Go's time package to get the current date
	return "2025-03-26" // Hardcoding current date
}

func promptLog() {
	options := []string{"Simple", "Verbose", "Cancel"}
	for {
		fmt.Println("\nChoose an option:")
		for i, option := range options {
			fmt.Printf("%d. %s\n", i+1, option)
		}

		var choice int
		fmt.Print("Enter choice: ")
		fmt.Scanf("%d", &choice)

		switch choice {
		case 1:
			executeGitCommand("git", "log", "--oneline", "--all")
			return
		case 2:
			executeGitCommand("git", "log", "-p", "--oneline")
			return
		case 3:
			return
		default:
			fmt.Println("Invalid choice.")
		}
	}
}

func showDiff() {
	cmd := exec.Command("git", "diff")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		fmt.Println("Error executing diff:", err)
	}
}

func fetchGitStatus() {
	executeGitCommand("git", "fetch")
	executeGitCommand("git", "status")
}

func promptCommit() {
	var message string
	fmt.Print("Enter commit message (or pass empty message to cancel): ")
	fmt.Scanf("%s", &message)

	if message != "" {
		executeGitCommand("git", "commit", "-m", message)
	} else {
		fmt.Println("Canceled commit.")
	}
}

func promptStage() {
	// Implementation for stage selection
}

func promptStash() {
	// Implementation for stash functionality
}

func discardUntrackedFiles() {
	executeGitCommand("git", "clean", "-i", "-d")
}

func promptReset() {
	// Implementation for reset functionality
}

package main

import (
	"log"
	"os"
	"os/exec"
	"time"
	"syscall"

	"github.com/fsnotify/fsnotify"
)

func main() {
	configPath := "/etc/otelcol-config/config.yaml"
	if envPath := os.Getenv("OTEL_CONFIG_PATH"); envPath != "" {
		configPath = envPath
	}

	watchIntervalStr := os.Getenv("WATCH_INTERVAL")
	watchInterval, err := time.ParseDuration(watchIntervalStr)
	if err != nil {
		watchInterval = 5 * time.Second
	}

	log.Printf("Starting watcher for %s with interval %v", configPath, watchInterval)

	cmd := startCollector(configPath)

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		log.Fatal(err)
	}
	defer watcher.Close()

	err = watcher.Add(configPath)
	if err != nil {
		log.Printf("Error adding watcher: %v. Polling mode enabled.", err)
	}

	ticker := time.NewTicker(watchInterval)
	defer ticker.Stop()

	var lastModTime time.Time
	if info, err := os.Stat(configPath); err == nil {
		lastModTime = info.ModTime()
	}

	for {
		select {
		case event, ok := <-watcher.Events:
			if !ok {
				return
			}
			if event.Op&fsnotify.Write == fsnotify.Write {
				log.Println("Config file modified (event), restarting collector...")
				cmd = restartCollector(cmd, configPath)
			}
		case err, ok := <-watcher.Errors:
			if !ok {
				return
			}
			log.Println("error:", err)
		case <-ticker.C:
			// Fallback polling
			if info, err := os.Stat(configPath); err == nil {
				if info.ModTime().After(lastModTime) {
					log.Println("Config file modified (polling), restarting collector...")
					lastModTime = info.ModTime()
					cmd = restartCollector(cmd, configPath)
				}
			}
		}
	}
}

func startCollector(configPath string) *exec.Cmd {
	cmd := exec.Command("/usr/local/bin/otelcol", "--config", configPath)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err := cmd.Start()
	if err != nil {
		log.Fatalf("Failed to start collector: %v", err)
	}
	log.Println("Collector started with PID", cmd.Process.Pid)
	return cmd
}

func restartCollector(cmd *exec.Cmd, configPath string) *exec.Cmd {
	if cmd != nil && cmd.Process != nil {
		log.Println("Stopping collector PID", cmd.Process.Pid)
		cmd.Process.Signal(syscall.SIGTERM)
		cmd.Wait()
	}
	return startCollector(configPath)
}

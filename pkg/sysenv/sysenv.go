package sysenv

import os

// Set or get environment variables

// Get function to read an environment or return a default value
func Get(key string, defaultVal string) string {
    if value, exists := os.LookupEnv(key); exists {
	return value
    }

    return defaultVal
}

// Set function to set an environment and return true if successful else return false on failure
func Set(key string, value string) bool {
    err := os.Setenv(key, value)
    if err == nil {
	return true
    }
    return false
}
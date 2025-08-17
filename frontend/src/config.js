// Default API base URL - can be overridden by environment variables
const DEFAULT_API_BASE_URL = 'http://localhost:5000/api'

// Get API base URL from environment variable or use default
export const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || DEFAULT_API_BASE_URL

// Other configuration options
export const config = {
  apiBaseUrl: API_BASE_URL,
  // Add other config options here as needed
  requestTimeout: 30000, // 30 seconds
  retryAttempts: 3
}

export default config

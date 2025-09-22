/**
 * API Service for Minecraft Click
 * Handles communication between the game and the backend API
 * Supports both authenticated and anonymous play
 */

class GameAPIService {
    constructor() {
        this.baseURL = '/api';
        this.isAuthenticated = false;
        this.username = '';
        this.password = '';
        this.offlineMode = false;
    }

    /**
     * Set authentication credentials
     */
    setCredentials(username, password) {
        this.username = username;
        this.password = password;
        this.isAuthenticated = !!username && !!password;
    }

    /**
     * Clear authentication credentials
     */
    clearCredentials() {
        this.username = '';
        this.password = '';
        this.isAuthenticated = false;
    }

    /**
     * Enable offline mode (fallback to localStorage)
     */
    enableOfflineMode() {
        this.offlineMode = true;
        console.log('API Service: Offline mode enabled');
    }

    /**
     * Disable offline mode
     */
    disableOfflineMode() {
        this.offlineMode = false;
        console.log('API Service: Offline mode disabled');
    }

    /**
     * Make HTTP request with error handling
     */
    async makeRequest(endpoint, options = {}) {
        if (this.offlineMode) {
            throw new Error('Offline mode - API requests disabled');
        }

        try {
            const url = `${this.baseURL}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.message || 'API request failed');
            }

            return data;
        } catch (error) {
            console.error(`API request failed (${endpoint}):`, error);
            
            // If network error and we have credentials, enable offline mode
            if (error.name === 'TypeError' && this.isAuthenticated) {
                console.warn('Network error detected, enabling offline mode');
                this.enableOfflineMode();
            }
            
            throw error;
        }
    }

    /**
     * Register a new user
     */
    async register(username, password, email = '') {
        try {
            const response = await this.makeRequest('/register', {
                method: 'POST',
                body: JSON.stringify({
                    username,
                    password,
                    email
                })
            });

            if (response.success) {
                this.setCredentials(username, password);
            }

            return response;
        } catch (error) {
            return {
                success: false,
                message: error.message || 'Registration failed'
            };
        }
    }

    /**
     * Login user
     */
    async login(username, password) {
        try {
            const response = await this.makeRequest('/login', {
                method: 'POST',
                body: JSON.stringify({
                    username,
                    password
                })
            });

            if (response.success) {
                this.setCredentials(username, password);
            }

            return response;
        } catch (error) {
            return {
                success: false,
                message: error.message || 'Login failed'
            };
        }
    }

    /**
     * Check if username is available
     */
    async checkUsername(username) {
        try {
            const response = await this.makeRequest('/check-username', {
                method: 'POST',
                body: JSON.stringify({ username })
            });

            return response;
        } catch (error) {
            return {
                success: false,
                available: false,
                message: error.message || 'Username check failed'
            };
        }
    }

    /**
     * Save game state to server
     */
    async saveGameState(gameState, platform = 'web') {
        if (!this.isAuthenticated) {
            // Save to localStorage as fallback
            return this.saveGameStateOffline(gameState);
        }

        try {
            const response = await this.makeRequest('/game/save', {
                method: 'POST',
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    gameState,
                    platform
                })
            });

            return response;
        } catch (error) {
            console.warn('Failed to save to server, falling back to localStorage:', error);
            return this.saveGameStateOffline(gameState);
        }
    }

    /**
     * Load game state from server
     */
    async loadGameState() {
        if (!this.isAuthenticated) {
            // Load from localStorage as fallback
            return this.loadGameStateOffline();
        }

        try {
            const response = await this.makeRequest('/game/load', {
                method: 'POST',
                body: JSON.stringify({
                    username: this.username,
                    password: this.password
                })
            });

            return response;
        } catch (error) {
            console.warn('Failed to load from server, falling back to localStorage:', error);
            return this.loadGameStateOffline();
        }
    }

    /**
     * Sync game state (smart sync based on timestamps)
     */
    async syncGameState(gameState, platform = 'web') {
        if (!this.isAuthenticated) {
            // Just save locally
            return this.saveGameStateOffline(gameState);
        }

        try {
            const response = await this.makeRequest('/game/sync', {
                method: 'POST',
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    gameState,
                    platform
                })
            });

            return response;
        } catch (error) {
            console.warn('Failed to sync with server, falling back to localStorage:', error);
            return this.saveGameStateOffline(gameState);
        }
    }

    /**
     * Save high score
     */
    async saveHighScore(highScoreData) {
        if (!this.isAuthenticated) {
            return {
                success: false,
                message: 'Must be logged in to save high scores'
            };
        }

        try {
            const response = await this.makeRequest('/highscores', {
                method: 'POST',
                body: JSON.stringify({
                    username: this.username,
                    password: this.password,
                    ...highScoreData
                })
            });

            return response;
        } catch (error) {
            return {
                success: false,
                message: error.message || 'Failed to save high score'
            };
        }
    }

    /**
     * Get high scores
     */
    async getHighScores() {
        try {
            const response = await this.makeRequest('/highscores', {
                method: 'GET'
            });

            return response;
        } catch (error) {
            return {
                success: false,
                scores: [],
                message: error.message || 'Failed to load high scores'
            };
        }
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            const response = await this.makeRequest('/health', {
                method: 'GET'
            });

            return response;
        } catch (error) {
            return {
                success: false,
                status: 'unhealthy',
                message: error.message || 'Health check failed'
            };
        }
    }

    // ===== OFFLINE MODE METHODS =====

    /**
     * Save game state to localStorage (offline mode)
     */
    saveGameStateOffline(gameState) {
        try {
            const saveData = {
                ...gameState,
                saveTime: Date.now(),
                offline: true
            };

            localStorage.setItem('minecraftClickSave', JSON.stringify(saveData));
            
            return {
                success: true,
                message: 'Game saved locally (offline mode)',
                offline: true
            };
        } catch (error) {
            return {
                success: false,
                message: 'Failed to save game locally',
                offline: true
            };
        }
    }

    /**
     * Load game state from localStorage (offline mode)
     */
    loadGameStateOffline() {
        try {
            const saveData = localStorage.getItem('minecraftClickSave');
            if (!saveData) {
                return {
                    success: false,
                    message: 'No saved game found',
                    offline: true
                };
            }

            const gameState = JSON.parse(saveData);
            
            return {
                success: true,
                gameState,
                offline: true,
                lastSaved: new Date(gameState.saveTime || 0).toISOString()
            };
        } catch (error) {
            return {
                success: false,
                message: 'Failed to load game from localStorage',
                offline: true
            };
        }
    }

    /**
     * Clear offline save data
     */
    clearOfflineData() {
        try {
            localStorage.removeItem('minecraftClickSave');
            return {
                success: true,
                message: 'Offline data cleared'
            };
        } catch (error) {
            return {
                success: false,
                message: 'Failed to clear offline data'
            };
        }
    }

    // ===== UTILITY METHODS =====

    /**
     * Check if we're currently online
     */
    async checkOnlineStatus() {
        try {
            const response = await this.healthCheck();
            return response.success;
        } catch (error) {
            return false;
        }
    }

    /**
     * Get connection status info
     */
    getConnectionInfo() {
        return {
            isAuthenticated: this.isAuthenticated,
            username: this.username,
            offlineMode: this.offlineMode,
            hasOfflineData: !!localStorage.getItem('minecraftClickSave')
        };
    }
}

// Create global instance
window.gameAPI = new GameAPIService();

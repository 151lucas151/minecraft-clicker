// Minecraft Clicker Game
class MinecraftClicker {
    constructor() {
        this.gameState = {
            blocks: 0,
            blocksPerClick: 1,
            blocksPerSecond: 0,
            totalMined: 0,
            totalClicks: 0,
            upgradesOwned: 0,
            startTime: Date.now(),
            playTime: 0,
            upgrades: {},
            achievements: {}
        };

        this.upgrades = [
            {
                id: 'wooden_pickaxe',
                name: 'Wooden Pickaxe',
                description: 'Increases blocks per click by 1',
                baseCost: 10,
                costMultiplier: 1.15,
                effect: { type: 'click', value: 1 }
            },
            {
                id: 'stone_pickaxe',
                name: 'Stone Pickaxe',
                description: 'Produces 1 block per second',
                baseCost: 50,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 1 }
            },
            {
                id: 'iron_pickaxe',
                name: 'Iron Pickaxe',
                description: 'Produces 5 blocks per second',
                baseCost: 200,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 5 }
            },
            {
                id: 'diamond_pickaxe',
                name: 'Diamond Pickaxe',
                description: 'Produces 25 blocks per second',
                baseCost: 1000,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 25 }
            },
            {
                id: 'netherite_pickaxe',
                name: 'Netherite Pickaxe',
                description: 'Produces 100 blocks per second',
                baseCost: 5000,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 100 }
            },
            {
                id: 'mining_robot',
                name: 'Mining Robot',
                description: 'Produces 500 blocks per second',
                baseCost: 25000,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 500 }
            },
            {
                id: 'automated_mine',
                name: 'Automated Mine',
                description: 'Produces 2500 blocks per second',
                baseCost: 100000,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 2500 }
            },
            {
                id: 'quantum_miner',
                name: 'Quantum Miner',
                description: 'Produces 10000 blocks per second',
                baseCost: 500000,
                costMultiplier: 1.15,
                effect: { type: 'passive', value: 10000 }
            }
        ];

        this.achievements = [
            {
                id: 'first_click',
                name: 'First Click',
                description: 'Click the mining button for the first time',
                condition: () => this.gameState.totalClicks >= 1,
                reward: 10
            },
            {
                id: 'hundred_clicks',
                name: 'Hundred Clicks',
                description: 'Click 100 times',
                condition: () => this.gameState.totalClicks >= 100,
                reward: 100
            },
            {
                id: 'thousand_clicks',
                name: 'Thousand Clicks',
                description: 'Click 1000 times',
                condition: () => this.gameState.totalClicks >= 1000,
                reward: 1000
            },
            {
                id: 'first_upgrade',
                name: 'First Tool',
                description: 'Buy your first mining tool',
                condition: () => this.gameState.upgradesOwned >= 1,
                reward: 50
            },
            {
                id: 'ten_upgrades',
                name: 'Tool Collector',
                description: 'Own 10 mining tools',
                condition: () => this.gameState.upgradesOwned >= 10,
                reward: 500
            },
            {
                id: 'hundred_blocks',
                name: 'Hundred Blocks',
                description: 'Have 100 blocks',
                condition: () => this.gameState.blocks >= 100,
                reward: 200
            },
            {
                id: 'thousand_blocks',
                name: 'Thousand Blocks',
                description: 'Have 1000 blocks',
                condition: () => this.gameState.blocks >= 1000,
                reward: 2000
            },
            {
                id: 'million_blocks',
                name: 'Million Blocks',
                description: 'Have 1,000,000 blocks',
                condition: () => this.gameState.blocks >= 1000000,
                reward: 100000
            }
        ];

        this.init();
    }

    init() {
        this.loadGame();
        this.setupEventListeners();
        this.renderUpgrades();
        this.renderAchievements();
        this.startGameLoop();
        this.updateDisplay();
    }

    setupEventListeners() {
        // Mining button click
        document.getElementById('bitcoinButton').addEventListener('click', () => {
            this.clickMine();
        });

        // Control buttons
        document.getElementById('saveButton').addEventListener('click', () => {
            this.saveGame();
            this.showNotification('Game saved!', 'success');
        });

        document.getElementById('loadButton').addEventListener('click', () => {
            this.loadGame();
            this.showNotification('Game loaded!', 'success');
        });

        document.getElementById('resetButton').addEventListener('click', () => {
            if (confirm('Are you sure you want to reset your progress? This cannot be undone.')) {
                this.resetGame();
                this.showNotification('Game reset!', 'success');
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                this.clickMine();
            }
        });
    }

    clickMine() {
        this.gameState.blocks += this.gameState.blocksPerClick;
        this.gameState.totalMined += this.gameState.blocksPerClick;
        this.gameState.totalClicks++;

        // Visual feedback
        const button = document.getElementById('bitcoinButton');
        button.classList.add('clicked');
        setTimeout(() => button.classList.remove('clicked'), 100);

        // Create particle effect
        this.createParticle();

        this.updateDisplay();
        this.checkAchievements();
    }

    createParticle() {
        const button = document.getElementById('bitcoinButton');
        const rect = button.getBoundingClientRect();
        
        // Create multiple particles for a more realistic effect
        for (let i = 0; i < 3; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random position around the button
            const offsetX = (Math.random() - 0.5) * 40;
            const offsetY = (Math.random() - 0.5) * 40;
            
            particle.style.left = rect.left + rect.width / 2 + offsetX + 'px';
            particle.style.top = rect.top + rect.height / 2 + offsetY + 'px';
            document.body.appendChild(particle);

            setTimeout(() => {
                if (document.body.contains(particle)) {
                    document.body.removeChild(particle);
                }
            }, 1000);
        }
    }

    buyUpgrade(upgradeId) {
        const upgrade = this.upgrades.find(u => u.id === upgradeId);
        if (!upgrade) return;

        const owned = this.gameState.upgrades[upgradeId] || 0;
        const cost = this.calculateUpgradeCost(upgrade, owned);

        if (this.gameState.blocks >= cost) {
            this.gameState.blocks -= cost;
            this.gameState.upgrades[upgradeId] = (this.gameState.upgrades[upgradeId] || 0) + 1;
            this.gameState.upgradesOwned++;

            // Apply upgrade effect
            if (upgrade.effect.type === 'click') {
                this.gameState.blocksPerClick += upgrade.effect.value;
            } else if (upgrade.effect.type === 'passive') {
                this.gameState.blocksPerSecond += upgrade.effect.value;
            }

            this.updateDisplay();
            this.renderUpgrades();
            this.checkAchievements();
            this.showNotification(`Purchased ${upgrade.name}!`, 'success');
        } else {
            this.showNotification('Not enough blocks!', 'error');
        }
    }

    calculateUpgradeCost(upgrade, owned) {
        return Math.floor(upgrade.baseCost * Math.pow(upgrade.costMultiplier, owned));
    }

    canAffordUpgrade(upgradeId) {
        const upgrade = this.upgrades.find(u => u.id === upgradeId);
        if (!upgrade) return false;

        const owned = this.gameState.upgrades[upgradeId] || 0;
        const cost = this.calculateUpgradeCost(upgrade, owned);
        return this.gameState.blocks >= cost;
    }

    renderUpgrades() {
        const grid = document.getElementById('upgradesGrid');
        grid.innerHTML = '';

        this.upgrades.forEach(upgrade => {
            const owned = this.gameState.upgrades[upgrade.id] || 0;
            const cost = this.calculateUpgradeCost(upgrade, owned);
            const canAfford = this.canAffordUpgrade(upgrade.id);

            const upgradeElement = document.createElement('div');
            upgradeElement.className = `upgrade-item ${canAfford ? '' : 'disabled'}`;
            upgradeElement.innerHTML = `
                <div class="upgrade-name">${upgrade.name}</div>
                <div class="upgrade-description">${upgrade.description}</div>
                <div class="upgrade-cost">Cost: ${this.formatNumber(cost)} Blocks</div>
                <div class="upgrade-owned">Owned: ${owned}</div>
            `;

            if (canAfford) {
                upgradeElement.addEventListener('click', () => this.buyUpgrade(upgrade.id));
            }

            grid.appendChild(upgradeElement);
        });
    }

    renderAchievements() {
        const grid = document.getElementById('achievementsGrid');
        grid.innerHTML = '';

        this.achievements.forEach(achievement => {
            const unlocked = this.gameState.achievements[achievement.id] || false;
            const conditionMet = achievement.condition();

            const achievementElement = document.createElement('div');
            achievementElement.className = `achievement-item ${unlocked ? '' : 'locked'}`;
            achievementElement.innerHTML = `
                <div class="achievement-name">${achievement.name}</div>
                <div class="achievement-description">${achievement.description}</div>
                ${unlocked ? '<div class="achievement-reward">Reward: ' + this.formatNumber(achievement.reward) + ' BTC</div>' : ''}
            `;

            grid.appendChild(achievementElement);
        });
    }

    checkAchievements() {
        this.achievements.forEach(achievement => {
            if (!this.gameState.achievements[achievement.id] && achievement.condition()) {
                this.gameState.achievements[achievement.id] = true;
                this.gameState.blocks += achievement.reward;
                this.gameState.totalMined += achievement.reward;
                this.showNotification(`Achievement Unlocked: ${achievement.name}! +${achievement.reward} Blocks`, 'success');
                this.renderAchievements();
            }
        });
    }

    updateDisplay() {
        // Update main displays
        document.getElementById('bitcoinAmount').textContent = this.formatNumber(this.gameState.blocks);
        document.getElementById('bitcoinRate').textContent = this.formatNumber(this.gameState.blocksPerSecond);
        document.getElementById('clickValue').textContent = this.formatNumber(this.gameState.blocksPerClick);

        // Update statistics
        document.getElementById('totalMined').textContent = this.formatNumber(this.gameState.totalMined);
        document.getElementById('totalClicks').textContent = this.formatNumber(this.gameState.totalClicks);
        document.getElementById('upgradesOwned').textContent = this.formatNumber(this.gameState.upgradesOwned);

        // Update play time
        const playTimeSeconds = Math.floor((Date.now() - this.gameState.startTime) / 1000);
        const hours = Math.floor(playTimeSeconds / 3600);
        const minutes = Math.floor((playTimeSeconds % 3600) / 60);
        const seconds = playTimeSeconds % 60;
        
        let timeString = '';
        if (hours > 0) timeString += `${hours}h `;
        if (minutes > 0) timeString += `${minutes}m `;
        timeString += `${seconds}s`;
        
                document.getElementById('playTime').textContent = timeString;

        // Update mining tool display
        this.updateMiningTool();

        // Re-render upgrades to update affordability
        this.renderUpgrades();
    }

    updateMiningTool() {
        // Hide all tools first
        const tools = [
            'woodenPickaxe', 'stonePickaxe', 'ironPickaxe', 'diamondPickaxe', 
            'netheritePickaxe', 'miningRobot', 'automatedMine', 'quantumMiner'
        ];
        
        tools.forEach(toolId => {
            const tool = document.getElementById(toolId);
            if (tool) {
                tool.classList.remove('active');
            }
        });

        // Show all tools you own
        if (this.gameState.upgrades['wooden_pickaxe'] > 0) {
            document.getElementById('woodenPickaxe').classList.add('active');
        }
        if (this.gameState.upgrades['stone_pickaxe'] > 0) {
            document.getElementById('stonePickaxe').classList.add('active');
        }
        if (this.gameState.upgrades['iron_pickaxe'] > 0) {
            document.getElementById('ironPickaxe').classList.add('active');
        }
        if (this.gameState.upgrades['diamond_pickaxe'] > 0) {
            document.getElementById('diamondPickaxe').classList.add('active');
        }
        if (this.gameState.upgrades['netherite_pickaxe'] > 0) {
            document.getElementById('netheritePickaxe').classList.add('active');
        }
        if (this.gameState.upgrades['mining_robot'] > 0) {
            document.getElementById('miningRobot').classList.add('active');
        }
        if (this.gameState.upgrades['automated_mine'] > 0) {
            document.getElementById('automatedMine').classList.add('active');
        }
        if (this.gameState.upgrades['quantum_miner'] > 0) {
            document.getElementById('quantumMiner').classList.add('active');
        }
    }

    startGameLoop() {
        setInterval(() => {
            // Add passive income
            if (this.gameState.blocksPerSecond > 0) {
                this.gameState.blocks += this.gameState.blocksPerSecond;
                this.gameState.totalMined += this.gameState.blocksPerSecond;
            }
            this.updateDisplay();
        }, 1000);
    }

    formatNumber(num) {
        if (num < 1000) return num.toString();
        if (num < 1000000) return (num / 1000).toFixed(1) + 'K';
        if (num < 1000000000) return (num / 1000000).toFixed(1) + 'M';
        if (num < 1000000000000) return (num / 1000000000).toFixed(1) + 'B';
        return (num / 1000000000000).toFixed(1) + 'T';
    }

    showNotification(message, type = 'success') {
        const notification = document.getElementById('notification');
        notification.textContent = message;
        notification.className = `notification ${type} show`;

        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }

    saveGame() {
        const saveData = {
            ...this.gameState,
            saveTime: Date.now()
        };
        localStorage.setItem('minecraftClickerSave', JSON.stringify(saveData));
    }

    loadGame() {
        const saveData = localStorage.getItem('minecraftClickerSave');
        if (saveData) {
            const loadedState = JSON.parse(saveData);
            
            // Preserve start time for play time calculation
            const originalStartTime = this.gameState.startTime;
            
            this.gameState = { ...loadedState };
            this.gameState.startTime = originalStartTime;
            
            this.updateDisplay();
            this.renderUpgrades();
            this.renderAchievements();
        }
    }

    resetGame() {
        this.gameState = {
            blocks: 0,
            blocksPerClick: 1,
            blocksPerSecond: 0,
            totalMined: 0,
            totalClicks: 0,
            upgradesOwned: 0,
            startTime: Date.now(),
            playTime: 0,
            upgrades: {},
            achievements: {}
        };
        
        localStorage.removeItem('minecraftClickerSave');
        this.updateDisplay();
        this.renderUpgrades();
        this.renderAchievements();
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new MinecraftClicker();
}); 
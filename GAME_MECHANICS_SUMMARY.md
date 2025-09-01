# Minecraft Clicker - Implemented Game Mechanics

This document summarizes all the game mechanics that have been implemented to support the enchantment system.

## 1. Tool Durability System (Unbreaking/Mending)

### Features:
- Tools have durability (100/100 by default)
- Each click reduces durability by 1
- Tools break when durability reaches 0
- Broken tools cannot mine blocks
- Visual indicators show durability status

### Enchantment Effects:
- **Unbreaking**: Reduces chance of durability loss
  - Level 1: 50% chance to avoid durability loss
  - Level 2: 33% chance to avoid durability loss  
  - Level 3: 25% chance to avoid durability loss
- **Mending**: Automatically repairs tools over time
  - Each level repairs 2 durability per second
  - Shows notification when tool is fully repaired

## 2. Mining Speed System (Efficiency)

### Features:
- Base mining cooldown of 100ms between clicks
- Mining speed affects click cooldown
- Visual feedback with button animations
- Particle effects for high-speed mining

### Enchantment Effects:
- **Efficiency**: Increases mining speed by 25% per level
  - Level 1: 125% speed (80ms cooldown)
  - Level 2: 150% speed (67ms cooldown)
  - Level 3: 175% speed (57ms cooldown)
  - Level 4: 200% speed (50ms cooldown)
  - Level 5: 225% speed (44ms cooldown)

## 3. Block Health System (Sharpness)

### Features:
- Blocks have health points
- Multiple clicks required to break tougher blocks
- Block health scales with game progress
- Different block types have different health multipliers
- Visual health bar shows block damage

### Block Types:
- Stone: 1x health
- Iron Ore: 1.5x health
- Gold Ore: 2x health
- Diamond Ore: 3x health
- Obsidian: 5x health
- Bedrock: 10x health

### Enchantment Effects:
- **Sharpness**: Increases damage dealt to blocks by 15% per level
  - Level 1: 115% damage
  - Level 2: 130% damage
  - Level 3: 145% damage
  - Level 4: 160% damage
  - Level 5: 175% damage

## 4. Bonus Block System (Fortune)

### Features:
- Chance-based bonus block drops
- Visual notifications for fortune procs
- Bonus amount varies randomly

### Enchantment Effects:
- **Fortune**: 10% chance per level for bonus blocks
  - When triggered, gives 0-50% bonus blocks per level
  - Shows notification with exact bonus percentage

## 5. Rare Block System (Looting)

### Features:
- Special rare block types can drop
- Tracks total rare blocks found
- Visual notifications for rare finds

### Rare Block Types:
- Diamond
- Emerald
- Gold
- Iron
- Coal

### Enchantment Effects:
- **Looting**: 15% chance per level to find rare blocks
  - Rare blocks give 50% bonus blocks
  - Shows notification with block type

## 6. Special Block System (Silk Touch)

### Features:
- Ultra-rare special blocks
- One-time collection (no duplicates)
- Significant bonuses when found

### Special Block Types:
- Ancient Debris
- End Stone
- Nether Star
- Dragon Egg

### Enchantment Effects:
- **Silk Touch**: 5% chance to find special blocks
  - Special blocks give 2x bonus blocks
  - Each special block can only be found once

## 7. Mining Power System (Infinity)

### Features:
- Global multiplier for all mining
- Affects blocks per click
- Displayed in UI as percentage

### Enchantment Effects:
- **Infinity**: Increases all mining by 50%
  - Multiplies blocks gained from all sources

## UI Additions

### New Display Elements:
1. **Tool Durability Bar**
   - Shows current/max durability
   - Color-coded (green/orange/red)
   - Pulses when broken

2. **Block Health Bar**
   - Shows current block health
   - Updates with each hit

3. **Mining Stats Panel**
   - Mining Speed percentage
   - Mining Power percentage
   - Rare Blocks Found counter
   - Special Blocks Found counter

### Enhanced Notifications:
- Fortune procs (green)
- Rare block finds (purple)
- Special block finds (orange)
- Tool break/repair (red/green)
- Error messages (red)

## Save System Updates

All new game mechanics are automatically saved and loaded:
- Tool durability state
- Current block health and damage
- Rare/special blocks found
- All counters and multipliers

## Visual Effects

### New Animations:
- Mining speed visual feedback (button scale)
- Mining particles for high-speed mining
- Durability bar animations
- Broken tool pulse effect

## Balance Considerations

The mechanics are balanced to create progression:
1. Early game: Focus on basic mining
2. Mid game: Tool durability becomes important
3. Late game: Maximize efficiency with all enchantments
4. End game: Collect all special blocks

All enchantments work together synergistically:
- Efficiency + Sharpness = Fast block breaking
- Fortune + Looting = Maximum resource gain
- Unbreaking + Mending = Sustainable mining
- Infinity = Universal power boost
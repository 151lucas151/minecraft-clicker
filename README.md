# Minecraft Clicker - Enhanced Version

A fun incremental mining game where you click to mine blocks and upgrade your mining operation!

## 🌐 Play the Game

- **🎮 Main Game**: [minecraftclick.com](https://minecraftclick.com) - Play the full game with all features
- **📄 Landing Page**: [hromp.com/minecraft-clicker](https://hromp.com/minecraft-clicker) - Game information and features
- **📱 Mobile App**: [React Native App Repository](https://github.com/151lucas151/minecraft-click-app) - *In Development* - Native mobile app for iOS and Android

## 🎮 Game Features

- **Incremental Mining**: Click to mine blocks and earn passive income
- **25+ Upgrades**: From wooden pickaxes to reality-bending mining tools
- **Achievement System**: Unlock achievements for various milestones
- **User Accounts**: Secure registration and login system
- **High Score Tracking**: Compete with other players globally
- **Profile Management**: Customize your profile with pictures and settings
- **Persistent Progress**: Save your game progress locally and in the cloud

## 🆕 Recent Improvements

### Domain and Deployment
- **New Domain**: Game now available at [minecraftclick.com](https://minecraftclick.com)
- **HTTPS Support**: Full SSL encryption for secure gameplay
- **API Optimization**: All endpoints updated for new domain structure
- **Navigation Fixes**: High scores and profile links updated

### User Account System
- **Secure Registration**: Create accounts with username, password, and email
- **Profile Pictures**: Choose from various mining tools as your profile picture
- **Profile Settings Page**: Manage your account, change passwords, update email
- **Session Management**: Stay logged in across browser sessions

### High Score System
- **Dedicated High Scores Page**: Beautiful table view of top players
- **Global Leaderboard**: See how you rank against other miners
- **Personal Statistics**: Track your best scores and achievements
- **Real-time Updates**: Refresh scores to see latest rankings

### Enhanced UI/UX
- **Modern Design**: Clean, responsive interface with smooth animations
- **Navigation**: Easy access to high scores and profile settings
- **Notifications**: Real-time feedback for all actions
- **Mobile Responsive**: Works great on all device sizes

## 🚀 Getting Started

1. **Visit the Game**: Go to [minecraftclick.com](https://minecraftclick.com) to play
2. **Create Account**: Click "Register" to create your account
3. **Start Mining**: Click the grass block to begin mining
4. **Buy Upgrades**: Purchase mining tools to increase your production
5. **Save Progress**: Your progress is automatically saved
6. **Compete**: Save high scores and compete with other players

## 🛠️ Technical Features

### Backend API (Flask)
- **User Authentication**: Secure password hashing with PBKDF2
- **Database**: SQLite with proper schema for users and high scores
- **RESTful API**: Clean endpoints for all game functionality
- **CORS Support**: Cross-origin requests enabled for web integration

### Frontend (Vanilla JavaScript)
- **No Dependencies**: Pure JavaScript, HTML, and CSS
- **Local Storage**: Offline progress saving
- **Real-time Updates**: Live game state management
- **Responsive Design**: Works on desktop and mobile

## 📊 Game Statistics

The game tracks various statistics:
- Total blocks mined
- Total clicks performed
- Number of upgrades owned
- Play time
- Personal best scores
- Achievement progress

## 🏆 High Score Categories

High scores are ranked by:
1. **Total Blocks Mined**: Your lifetime mining achievement
2. **Current Blocks**: Your current block balance
3. **Upgrades Owned**: Number of mining tools purchased
4. **Play Time**: Time spent in the game

## 🔧 API Endpoints

All API endpoints are available at `https://minecraftclick.com/api/`:

- `POST /api/register` - Create new account
- `POST /api/login` - User authentication
- `GET /api/profile` - Get user profile
- `PUT /api/profile` - Update profile settings
- `POST /api/change-password` - Change password
- `GET /api/highscores` - Get global leaderboard
- `POST /api/highscores` - Save high score
- `GET /api/health` - API health check
- `POST /api/game/save` - Save game state
- `POST /api/game/load` - Load game state
- `GET /api/user/<username>` - Get public user profile

## 🎯 Game Strategy

1. **Early Game**: Focus on click upgrades to increase manual mining
2. **Mid Game**: Invest in passive income upgrades for steady progress
3. **Late Game**: Purchase expensive upgrades for exponential growth
4. **End Game**: Aim for achievements and compete for high scores

## 🔒 Security Features

- **Password Hashing**: PBKDF2 with salt for secure password storage
- **Input Validation**: All user inputs are validated and sanitized
- **SQL Injection Protection**: Parameterized queries prevent attacks
- **XSS Protection**: Content Security Policy headers

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🎨 Customization

### Profile Pictures
Choose from various mining tools:
- Default avatar
- Wooden pickaxe
- Stone pickaxe
- Iron pickaxe
- Diamond pickaxe
- Netherite pickaxe

### Game Settings
- Adjust notification preferences
- Customize UI themes
- Set personal goals and targets

## 🐛 Troubleshooting

### Common Issues
1. **Can't Save High Score**: Make sure you're logged in
2. **Progress Not Saving**: Check browser local storage permissions
3. **API Errors**: Verify the backend server is running
4. **Login Issues**: Ensure username/password are correct

### Support
If you encounter any issues:
1. Check the browser console for error messages
2. Verify your internet connection
3. Try refreshing the page
4. Clear browser cache if needed

## 🚀 Future Enhancements

Planned features for future updates:
- **Email Password Reset**: Recover accounts via email
- **Social Features**: Friend lists and private competitions
- **More Achievements**: Additional milestones and rewards
- **Seasonal Events**: Special limited-time content
- **Advanced Statistics**: Detailed analytics and charts
- **Mobile App**: Native mobile application (React Native) - *In Development*

## 📱 Mobile Development

A React Native mobile app is currently in development to bring Minecraft Clicker to iOS and Android devices. The mobile app will feature:
- **Native Performance**: Optimized for mobile devices
- **Offline Play**: Continue mining even without internet
- **Push Notifications**: Get notified of achievements and milestones
- **Touch Controls**: Optimized touch interface for mobile
- **Cross-Platform**: Single codebase for iOS and Android

**Repository**: [151lucas151/minecraft-click-app](https://github.com/151lucas151/minecraft-click-app)

## 📄 License

This project is open source and available under the MIT License.

---

**Happy Mining! ⛏️** 
# Among Us - Single Player Edition 🚀

## Overview
This project is a **single-player adaptation** of the popular game **Among Us**, built using Python. It allows players to experience the core mechanics of the game in a solo environment with AI-controlled crewmates and impostors.

## Features 🎮
- 👥 **Crewmate & Impostor Roles** – AI-based behavior simulation.
- 🕵️ **Sabotage and Emergency Meetings** – Mimics real Among Us gameplay.
- 📜 **Task Completion System** – Players complete assigned tasks.
- 🎨 **Custom Sprites & UI** – Includes original and modified assets.
- 🛠️ **Modular Engine Design** – Expandable components for additional features.

## Folder Structure 📂
```
Among-Us/
├── images/              # Stores all game images and sprites
├── engine/              # Core engine logic
│   ├── collision_manager.py
│   ├── component.py
│   ├── components/      # Game components
│   │   ├── animation.py
│   │   ├── button.py
│   │   ├── collection.py
│   │   ├── movement.py
│   │   ├── room.py
│   │   ├── sprite.py
│   ├── entity.py
│   ├── scene.py
│   ├── scene_manager.py
│   ├── input_manager.py
│   ├── event_manager.py
├── scenes/              # JSON files defining game scenarios
│   ├── crewWin.json
│   ├── emergencyMeeting.json
│   ├── imposterWin.json
├── docs/                # Documentation files
│   ├── roadmap.txt      # Project roadmap and future plans
├── game.py              # Main game entry point
├── README.md            # Project overview and setup instructions
```

## Installation & Setup 🛠️
### Prerequisites
- **Python 3.8+** installed

### Install Dependencies
```
pip install -r requirements.txt
```

### Run the Game
```
python game.py
```

🚀 **Enjoy the game!** 🚀


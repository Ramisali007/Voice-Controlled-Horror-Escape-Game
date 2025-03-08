# Voice-Controlled Horror Escape Game

Welcome to the **Voice-Controlled Horror Escape Game**! This project is a 3D horror game where players interact with the environment using voice commands. The game leverages **Whisper AI** for speech-to-text transcription and **Panda3D** for the 3D game engine. Players can control objects like doors, flashlights, and closets using natural language commands.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Dependencies](#dependencies)
5. [File Structure](#file-structure)
6. [Usage](#usage)
7. [Generating JSON and SRT Files](#generating-json-and-srt-files)
8. [License](#license)

---

## Project Overview

This project is a 3D horror game where players use voice commands to interact with the environment. The game uses:
- **Whisper AI** for transcribing voice commands.
- **Panda3D** for rendering the 3D environment.
- **PyAudio** for recording audio from the microphone.

Players can issue commands like:
- "Open the door"
- "Close the door"
- "Turn on the flashlight"
- "Shift door left/right"
- "Remove the door"
- "Add the door"

The game logs all commands with timestamps and generates **JSON** and **SRT** files for further analysis or subtitles.

---

## Features

- **Voice Control**: Use natural language commands to interact with the game.
- **3D Environment**: Built using Panda3D with realistic lighting and objects.
- **Command Logging**: Logs all commands with timestamps.
- **JSON and SRT Generation**: Generates JSON and SRT files for commands.
- **Flashlight Mechanic**: Turn on/off a flashlight to explore the environment.

---

## Installation

### Prerequisites

1. **Python 3.10 or later**.
2. **Panda3D**: Install using the provided `Panda3D-SDK-1.10.15-x64.exe` or via pip:
   ```bash
   pip install panda3d
   ```
3. **Whisper AI**: Install Whisper and its dependencies:
   ```bash
   pip install openai-whisper
   ```
4. **PyAudio**: Install PyAudio for audio recording:
   ```bash
   pip install pyaudio
   ```

### Setup

1. Clone or download the project files.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place the Whisper model (`base.pt`) in the `models` folder.

---

## Dependencies

- **Panda3D**: 3D game engine.
- **Whisper AI**: Speech-to-text transcription.
- **PyAudio**: Audio recording.
- **NumPy**: For audio processing.
- **Wave**: For saving audio files.
- **Threading**: For running voice commands in a separate thread.

---

## File Structure

```
Voice-Controlled Horror Escape Game/
├── models/                  # Folder for Whisper AI models
│   └── base.pt              # Whisper base model
├── .vscode/                 # VSCode settings (if applicable)
├── commands.json            # JSON file for logged commands
├── commands.srt             # SRT file for subtitles
├── horror_game.py           # Main game script
├── temp_audio.wav           # Temporary audio file for voice commands
├── Panda3D-SDK-1.10.15-x64.exe  # Panda3D installer
├── PyAudio-0.2.11-cp310-cp310-win_amd64.whl  # PyAudio wheel file
├── README.md                # This file
```

---

## Usage

1. Run the game:
   ```bash
   python horror_game.py
   ```
2. Follow the on-screen instructions to issue voice commands.
3. Press `Enter` to start recording a command.
4. The game will process the command and update the 3D environment.

### Example Commands

- **"Open the door"**: Moves the door to the open position.
- **"Close the door"**: Moves the door back to the closed position.
- **"Turn on the flashlight"**: Activates the flashlight.
- **"Shift door left"**: Moves the door to the left.
- **"Shift door right"**: Moves the door to the right.
- **"Remove the door"**: Removes the door from the scene.
- **"Add the door"**: Adds the door back to the scene.

---

## Generating JSON and SRT Files

The game automatically generates two files:
1. **`commands.json`**: Contains a log of all commands with timestamps.
   ```json
   [
       {
           "timestamp": 0.0,
           "command": "open the door"
       },
       {
           "timestamp": 5.0,
           "command": "close the door"
       }
   ]
   ```
2. **`commands.srt`**: Contains subtitles for the commands in SRT format.
   ```
   1
   0:00:00 --> 0:00:05
   open the door

   2
   0:00:05 --> 0:00:10
   close the door
   ```

---

## License

This project is open-source and available under the **MIT License**. Feel free to modify and distribute it as needed.

---

Enjoy the game.🎮

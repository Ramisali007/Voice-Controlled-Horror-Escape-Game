from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, PointLight, Vec3, Vec4
import whisper
import pyaudio
import wave
import numpy as np
from threading import Thread
import json
from datetime import timedelta

class HorrorGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Set up the scene
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add a door
        self.door = self.loader.loadModel("models/box")
        self.door.reparentTo(self.render)
        self.door.setPos(0, 10, 0)
        self.door.setScale(2, 0.2, 3)
        self.door_color = Vec4(1, 1, 1, 1)  # Default color (white)

        # Add a closet
        self.closet = self.loader.loadModel("models/box")
        self.closet.reparentTo(self.render)
        self.closet.setPos(5, 10, 0)
        self.closet.setScale(2, 0.2, 3)

        # Add a flashlight
        self.flashlight = self.loader.loadModel("models/smiley")
        self.flashlight.reparentTo(self.render)
        self.flashlight.setPos(-5, 10, 0)
        self.flashlight.setScale(0.5, 0.5, 0.5)
        self.flashlight.hide()  # Start with flashlight off

        # Add lighting
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.render.setLight(self.render.attachNewNode(self.ambientLight))

        self.directionalLight = DirectionalLight("directionalLight")
        self.directionalLight.setColor(Vec4(0.8, 0.8, 0.8, 1))
        self.directionalLight.setDirection(Vec3(-1, -1, -1))
        self.render.setLight(self.render.attachNewNode(self.directionalLight))

        # Add point light for better visibility
        pointLight = PointLight("pointLight")
        pointLight.setColor(Vec4(1, 1, 1, 1))
        pointLightNode = self.render.attachNewNode(pointLight)
        pointLightNode.setPos(0, 0, 15)
        self.render.setLight(pointLightNode)

        # Set up camera
        self.camera.setPos(0, -20, 10)  # Adjust these values as needed
        self.camera.lookAt(0, 10, 0)

        # Load Whisper model locally
        self.model = whisper.load_model("base", download_root="models")

        # Initialize lists to store commands and timestamps
        self.commands = []
        self.start_time = None

        # Start voice command thread
        self.voice_thread = Thread(target=self.listen_for_commands)
        self.voice_thread.daemon = True
        self.voice_thread.start()

    # Function to record audio from microphone
    def record_audio(self, filename, record_seconds=5):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Recording...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * record_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Recording finished.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

    # Function to transcribe audio using Whisper
    def transcribe_audio(self, filename):
        audio = whisper.load_audio(filename)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)
        options = whisper.DecodingOptions()
        result = whisper.decode(self.model, mel, options)
        return result.text

    # Function to process commands
    def process_command(self, command):
        command = command.lower()
        if "open the door" in command:
            print("Opening the door...")
            self.door.setPos(0, 12, 0)  # Move the door
            print(f"Door position: {self.door.getPos()}")
        elif "close the door" in command:
            print("Closing the door...")
            self.door.setPos(0, 10, 0)  # Move the door back
            print(f"Door position: {self.door.getPos()}")
        elif "turn on the flashlight" in command:
            print("Turning on the flashlight...")
            self.flashlight.show()  # Show the flashlight
        elif "shift door left" in command:
            print("Shifting door left...")
            self.door.setX(self.door.getX() - 2)  # Move door left
            print(f"Door position: {self.door.getPos()}")
        elif "shift door right" in command:
            print("Shifting door right...")
            self.door.setX(self.door.getX() + 2)  # Move door right
            print(f"Door position: {self.door.getPos()}")
        elif "remove the door" in command:
            print("Removing the door...")
            self.door.detachNode()  # Remove the door from the scene
        elif "add the door" in command:
            print("Adding the door...")
            self.door.reparentTo(self.render)  # Add the door back to the scene
            self.door.setColor(self.door_color)  # Restore the door color
        else:
            print("Command not recognized.")

        # Log the command with a timestamp
        self.log_command(command)

    # Function to log commands with timestamps
    def log_command(self, command):
        if self.start_time is None:
            self.start_time = self.taskMgr.globalClock.getFrameTime()
        
        current_time = self.taskMgr.globalClock.getFrameTime() - self.start_time
        self.commands.append({
            "timestamp": current_time,
            "command": command
        })

    # Function to generate JSON file
    def generate_json(self, filename="commands.json"):
        with open(filename, "w") as f:
            json.dump(self.commands, f, indent=4)
        print(f"JSON file '{filename}' generated.")

    # Function to generate SRT file
    def generate_srt(self, filename="commands.srt"):
        with open(filename, "w") as f:
            for i, cmd in enumerate(self.commands):
                start_time = timedelta(seconds=cmd["timestamp"])
                end_time = timedelta(seconds=cmd["timestamp"] + 5)  # Assuming each command lasts 5 seconds
                f.write(f"{i + 1}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{cmd['command']}\n\n")
        print(f"SRT file '{filename}' generated.")

    # Main loop for voice commands
    def listen_for_commands(self):
        while True:
            input("Press Enter to start recording...")
            self.record_audio("temp_audio.wav", record_seconds=5)
            command = self.transcribe_audio("temp_audio.wav")
            print(f"Command: {command}")
            self.process_command(command)

            # Generate JSON and SRT files after each command
            self.generate_json()
            self.generate_srt()

# Run the game
game = HorrorGame()
game.run()
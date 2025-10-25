import socketserver
import threading
import random

START_COINS = 3000
FLAG_THRESHOLD = 1_000_000
HIGH_LOW_GAMES_LIMIT = 1000
FLAG = "DREAM{redacted}"


class CasinoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.rng = random.Random()
        self.coins = START_COINS
        self.hl_remaining = HIGH_LOW_GAMES_LIMIT

        self.send("Welcome to the Vibe Casino!")
        self.send(f"You start with {self.coins} coins.")
        self.send(f"Reach {FLAG_THRESHOLD} coins to win the flag.")

        while True:
            self.send("\nMenu:\n1) High-Low\n2) Slot Machine\n3) Balance\n4) Exit")
            choice = self.recv("> ")

            if choice == "1":
                self.play_highlow()
            elif choice == "2":
                self.play_slots()
            elif choice == "3":
                self.send(f"You have {self.coins} coins.")
            elif choice == "4":
                self.send("Goodbye!")
                break
            else:
                self.send("Invalid option.")

            if self.coins >= FLAG_THRESHOLD:
                self.send(f"Congratulations! Here's your flag: {FLAG}")
                break

    def play_highlow(self):
        if self.hl_remaining <= 0:
            self.send("You've used all your High-Low plays.")
            return

        while True:
            bet_str = self.recv("Enter your bet (1-10): ")
            if not bet_str.isdigit():
                self.send("Invalid input, enter a number between 1 and 10.")
                continue
            bet = int(bet_str)
            if bet < 1 or bet > 10:
                self.send("Bet must be between 1 and 10.")
                continue
            if bet > self.coins:
                self.send(f"Not enough coins for that bet. You have {self.coins}.")
                continue
            break

        self.coins -= bet
        self.hl_remaining -= 1

        self.send(f"Guess if the number is (L)ow or (H)igh? [0-4294967294]")
        guess = self.recv("> ").strip().upper()
        num = self.rng.randint(0, 4294967294)
        middle = 2147483647

        win = (guess == "L" and num < middle) or (guess == "H" and num > middle)

        if win:
            self.coins += bet * 2
            self.send(f"You won! Number was {num}.")
        else:
            self.send(f"You lost. Number was {num}.")

        self.send(f"Remaining plays: {self.hl_remaining}")

    def play_slots(self):
        while True:
            bet_str = self.recv(f"Enter your bet (1-{self.coins}): ")
            if not bet_str.isdigit():
                self.send(f"Invalid input, enter a number between 1 and {self.coins}.")
                continue
            bet = int(bet_str)
            if bet < 1 or bet > self.coins:
                self.send(f"Bet must be between 1 and {self.coins}.")
                continue
            break

        self.coins -= bet

        result = self.rng.choices(["7", "A", "B", "C"], weights=[464, 200, 180, 156], k=3)

        self.send(f"Slot: {' '.join(result)}")

        if result == ["7", "7", "7"]:
            payout = bet * 2
            self.coins += payout
            self.send("JACKPOT! 777!")
        else:
            payout = 0
            self.send("Better luck next time.")

        self.send(f"You won {payout} coins.")

    def send(self, msg):
        self.request.sendall((msg + "\n").encode())

    def recv(self, prompt=""):
        self.send(prompt)
        return self.request.recv(1024).decode().strip()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


def main():
    host, port = "0.0.0.0", 777
    with ThreadedTCPServer((host, port), CasinoHandler) as server:
        print(f"[+] Server running on {host}:{port}")
        server.serve_forever()


if __name__ == "__main__":
    main()

import random
import re
from datetime import datetime
import time

class HotelBookingBot:
    """A fun and interactive chatbot for hotel room bookings with ID proof selection!"""

    # Predefined responses for negative answers and exit commands
    negative_responses = ("no", "nope", "nah", "naw", "not interested", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")

    # Predefined random greetings
    random_greetings = [
        "Welcome to our hotel! 🎉 How can I assist you with your room booking today? 🏨",
        "Hello! 😄 Ready to book a cozy room? I can help you with that! ✨",
        "Hey there! 👋 Let's get you a nice room to stay in! 🛏️"
    ]

    # Predefined room types
    available_rooms = {
        "Single": 3500,  # 3500 INR per night
        "Double": 5500,  # 5500 INR per night
        "Suite": 10000   # 10000 INR per night
    }

    # Available ID Proofs
    available_id_proofs = {
        1: "Passport",
        2: "Driver’s License",
        3: "Aadhaar Card",
        4: "Voter ID",
        5: "PAN Card"
    }

    def __init__(self):
        """Initialize the bot and define regex patterns to match user inputs."""
        self.booking_details = {}

    def typing_animation(self, text, delay=0.1):
        """Simulate typing animation."""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()  # Move to the next line after typing

    def greet(self):
        """Start the conversation with a random greeting and personality."""
        self.typing_animation(random.choice(self.random_greetings), 0.1)
        self.name = input("Can I have your name, please? 📝\n")

        # Ask if the user wants to proceed with booking
        willing_to_book = input(f"Hi {self.name}, would you like to book a room? (yes/no)\n")

        if self.make_exit(willing_to_book):  # Check if user wants to exit
            return

        if willing_to_book.lower() in self.negative_responses:
            self.typing_animation("No problem! Have a great day! 😊", 0.1)
            return

        self.ask_room_type()

    def make_exit(self, reply):
        """Check if the user wants to exit the conversation."""
        if reply.lower() in self.exit_commands:
            self.typing_animation("Goodbye! Have a wonderful day! 🌟", 0.1)
            return True
        return False

    def ask_room_type(self):
        """Ask the user for their preferred room type."""
        while True:
            print("Great! What type of room would you prefer?")
            print("1. 🛏️ Single - ₹3500 per night")
            print("2. 🛋️ Double - ₹5500 per night")
            print("3. 💎 Suite - ₹10000 per night")

            room_type = input("Please choose a number (1-3):\n")

            if room_type == "1":
                self.booking_details['room_type'] = "Single"
                break
            elif room_type == "2":
                self.booking_details['room_type'] = "Double"
                break
            elif room_type == "3":
                self.booking_details['room_type'] = "Suite"
                break
            else:
                print("Oops! Please choose a valid option (1-3).")

        self.ask_check_in_date()

    def ask_check_in_date(self):
        """Ask the user for their check-in date."""
        while True:
            check_in_date = input("When would you like to check in? (Please use format DD-MM-YY)\n")

            if not self.is_valid_date(check_in_date):
                print("Invalid date format. Please use DD-MM-YY. 📅")
                continue

            self.booking_details['check_in'] = check_in_date
            self.ask_check_out_date()
            break

    def ask_check_out_date(self):
        """Ask the user for their check-out date."""
        while True:
            check_out_date = input("When would you like to check out? (Please use format DD-MM-YY)\n")

            if not self.is_valid_date(check_out_date):
                print("Invalid date format. Please use DD-MM-YY. 📅")
                continue

            # Check if check-out is after check-in
            check_in_date = self.booking_details['check_in']
            if datetime.strptime(check_out_date, "%d-%m-%y") <= datetime.strptime(check_in_date, "%d-%m-%y"):
                print("Error: Check-out date must be after check-in date.")
                continue

            self.booking_details['check_out'] = check_out_date
            self.ask_number_of_guests()
            break

    def ask_number_of_guests(self):
        """Ask the user for the number of guests."""
        while True:
            try:
                num_guests = int(input("How many guests will be staying? 👨‍👩‍👧‍👦\n"))
                if num_guests <= 0:
                    print("Please enter a valid number of guests.")
                    continue
                self.booking_details['num_guests'] = num_guests
                self.ask_id_proof()
                break
            except ValueError:
                print("Please enter a valid number of guests.")

    def ask_id_proof(self):
        """Ask the user to select their ID proof from a list."""
        print("Please choose a valid ID proof from the list below:")
        for key, value in self.available_id_proofs.items():
            print(f"{key}. {value}")

        while True:
            try:
                id_choice = int(input("Enter the number corresponding to your ID proof: "))

                if id_choice in self.available_id_proofs:
                    self.booking_details['id_proof'] = self.available_id_proofs[id_choice]
                    self.booking_details['id_number'] = input(f"Please enter your {self.booking_details['id_proof']} number: ")
                    break
                else:
                    print("Oops! Please choose a valid option from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        self.show_booking_summary()

    def show_booking_summary(self):
        """Display a summary of the booking and confirm."""
        room_type = self.booking_details['room_type']
        price_per_night = self.available_rooms[room_type]
        self.typing_animation(f"Your room booking: {room_type} for ₹{price_per_night} per night.", 0.1)

        check_in = self.booking_details['check_in']
        check_out = self.booking_details['check_out']
        num_guests = self.booking_details['num_guests']

        self.typing_animation(f"Check-in: {check_in}, Check-out: {check_out}", 0.1)
        self.typing_animation(f"Number of guests: {num_guests}", 0.1)
        self.typing_animation(f"ID Proof: {self.booking_details['id_proof']}, ID Number: {self.booking_details['id_number']}", 0.1)

        # Calculate total price based on number of nights
        check_in_date = datetime.strptime(check_in, "%d-%m-%y")
        check_out_date = datetime.strptime(check_out, "%d-%m-%y")
        num_nights = (check_out_date - check_in_date).days
        total_price = price_per_night * num_nights

        self.typing_animation(f"Total price for {num_nights} night(s): ₹{total_price}", 0.1)

        confirm = input(f"Would you like to confirm your booking for ₹{total_price}? (yes/no)\n")

        if confirm.lower() == "yes":
            self.typing_animation("Hooray! 🎉 Your booking has been confirmed! Enjoy your stay! 🥳", 0.1)
        else:
            self.typing_animation("Great Choice! 😎 Let us know if you need help later!", 0.1)

    def is_valid_date(self, date_string):
        """Check if the date is in the correct format DD-MM-YY."""
        try:
            datetime.strptime(date_string, "%d-%m-%y")
            return True
        except ValueError:
            return False

    def no_match_intent(self):
        """Return a fun response when the bot can't match the user's input."""
        responses = [
            "Oops, I think I missed that! 🤔 Try again?",
            "Hmm... my circuits are fried. Could you say that again? 🤯"
        ]
        return random.choice(responses)

# Start the chatbot
if __name__ == "__main__":
    bot = HotelBookingBot()
    bot.greet()

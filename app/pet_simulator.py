import random
from datetime import datetime, timedelta

class Pet:
    def __init__(self, name, species="unknown"):
        self.name = name
        self.species = species
        self.hunger = 5
        self.energy = 5
        self.happiness = 5
        self.hygiene = 5
        self.health = 10
        self.tricks = []
        self.birthday = datetime.now()
        self.last_fed = None
        self.last_slept = None
        self.mood = "neutral"
        self.favorite_foods = []
        self.disliked_foods = []
        self.energy_decay_rate = 0.5
        self.happiness_decay_rate = 0.3
        self.hunger_growth_rate = 0.4

    def _update_stats(self):
        """Internal method to decay stats over time"""
        time_passed = random.uniform(0.8, 1.2)  # Random factor to make it less predictable
        
        self.energy = max(0, self.energy - self.energy_decay_rate * time_passed)
        self.happiness = max(0, self.happiness - self.happiness_decay_rate * time_passed)
        self.hunger = min(10, self.hunger + self.hunger_growth_rate * time_passed)
        
        # Update mood based on stats
        self._update_mood()

    def _update_mood(self):
        """Determine pet's mood based on current stats"""
        if self.health < 3:
            self.mood = "sick"
        elif self.hunger > 8:
            self.mood = "hungry"
        elif self.energy < 3:
            self.mood = "tired"
        elif self.happiness > 7:
            self.mood = "happy"
        elif self.happiness < 3:
            self.mood = "grumpy"
        else:
            self.mood = "neutral"

    def eat(self, food=None):
        self._update_stats()
        
        if food:
            if food in self.favorite_foods:
                bonus = 2
                msg = f"{self.name} loves {food}! "
            elif food in self.disliked_foods:
                bonus = -1
                msg = f"{self.name} doesn't like {food}. "
            else:
                bonus = 0
                msg = f"{self.name} is eating {food}. "
        else:
            bonus = 0
            msg = f"{self.name} is eating. "

        hunger_reduction = 3 + bonus
        self.hunger = max(0, self.hunger - hunger_reduction)
        self.energy = min(10, self.energy + 1)
        self.happiness = min(10, self.happiness + 0.5)
        self.last_fed = datetime.now()
        
        return msg + f"Hunger decreased by {hunger_reduction} points."

    def sleep(self, duration=1):
        self._update_stats()
        
        energy_gain = duration * 2
        self.energy = min(10, self.energy + energy_gain)
        self.hunger = min(10, self.hunger + duration * 0.5)
        self.happiness = min(10, self.happiness + duration * 0.3)
        self.last_slept = datetime.now()
        
        return f"{self.name} slept for {duration} hours. Gained {energy_gain} energy."

    def play(self, game="default"):
        self._update_stats()
        
        if self.energy < 2:
            return f"{self.name} is too tired to play right now."
        
        energy_cost = 2
        happiness_gain = random.randint(1, 3)
        
        self.energy = max(0, self.energy - energy_cost)
        self.happiness = min(10, self.happiness + happiness_gain)
        self.hunger = min(10, self.hunger + 1)
        
        games = {
            "fetch": f"{self.name} happily fetches the ball!",
            "laser": f"{self.name} chases the laser pointer!",
            "default": f"You play with {self.name}!"
        }
        
        return games.get(game, games["default"]) + f" Happiness +{happiness_gain}, Energy -{energy_cost}"

    def train(self, trick):
        self._update_stats()
        
        if self.energy < 3:
            return f"{self.name} is too tired to train right now."
        if trick in self.tricks:
            return f"{self.name} already knows '{trick}'!"
        
        difficulty = len(trick.split())  # More words = harder trick
        success_chance = min(0.9, max(0.3, 0.7 - difficulty * 0.1))
        
        if random.random() < success_chance:
            self.tricks.append(trick)
            self.energy -= 3
            self.happiness += 1
            return f"Success! {self.name} learned '{trick}'! (Energy -3, Happiness +1)"
        else:
            self.energy -= 2
            self.happiness -= 0.5
            return f"{self.name} didn't quite get it this time. Try again later! (Energy -2, Happiness -0.5)"

    def bathe(self):
        self._update_stats()
        
        self.hygiene = 10
        self.happiness = max(0, self.happiness - 1)  # Most pets don't like baths
        return f"{self.name} is now clean but slightly grumpy about it."

    def show_tricks(self):
        if not self.tricks:
            return f"{self.name} doesn't know any tricks yet. Try training them!"
        return f"{self.name} knows these tricks:\n- " + "\n- ".join(self.tricks)

    def get_age(self):
        age = datetime.now() - self.birthday
        return str(age).split(".")[0]  # Remove microseconds

    def get_status(self):
        self._update_stats()
        status = [
            f"🐾 {self.name}'s Status 🐾",
            f"Species: {self.species}",
            f"Age: {self.get_age()}",
            f"Mood: {self.mood.capitalize()}",
            "",
            "Stats:",
            f"Hunger: {'♥' * int(self.hunger)}{'♡' * (10 - int(self.hunger))} ({self.hunger:.1f}/10)",
            f"Energy: {'⚡' * int(self.energy)}{' ' * (10 - int(self.energy))} ({self.energy:.1f}/10)",
            f"Happiness: {'☺' * int(self.happiness)}{' ' * (10 - int(self.happiness))} ({self.happiness:.1f}/10)",
            f"Hygiene: {'✨' * int(self.hygiene)}{' ' * (10 - int(self.hygiene))} ({self.hygiene:.1f}/10)",
            f"Health: {'❤' * int(self.health)}{' ' * (10 - int(self.health))} ({self.health:.1f}/10)",
            "",
            f"Tricks known: {len(self.tricks)}",
            f"Favorite foods: {', '.join(self.favorite_foods) if self.favorite_foods else 'None'}",
            f"Disliked foods: {', '.join(self.disliked_foods) if self.disliked_foods else 'None'}"
        ]
        return "\n".join(status)

    def add_favorite_food(self, food):
        if food not in self.favorite_foods:
            self.favorite_foods.append(food)
            return f"{food} added to {self.name}'s favorite foods!"
        return f"{self.name} already has {food} as a favorite food."

    def add_disliked_food(self, food):
        if food not in self.disliked_foods:
            self.disliked_foods.append(food)
            return f"{food} added to {self.name}'s disliked foods."
        return f"{self.name} already dislikes {food}."

    def speak(self):
        moods = {
            "happy": ["Purr purr!", "Wag wag!", "Chirp chirp!"],
            "grumpy": ["Hiss!", "Grrr...", "Screech!"],
            "hungry": ["Meow?", "Bark!", "Feed me!"],
            "tired": ["Zzz...", "Too sleepy..."],
            "sick": ["Cough...", "Whimper..."],
            "neutral": ["Hello!", "What's up?"]
        }
        return random.choice(moods.get(self.mood, ["..."]))

    def random_event(self):
        events = [
            (0.3, lambda: f"{self.name} found a toy! Happiness +1", lambda: setattr(self, 'happiness', min(10, self.happiness + 1))),
            (0.1, lambda: f"{self.name} had a bad dream. Happiness -1", lambda: setattr(self, 'happiness', max(0, self.happiness - 1))),
            (0.2, lambda: f"{self.name} is exploring! Energy -1", lambda: setattr(self, 'energy', max(0, self.energy - 1))),
            (0.05, lambda: f"{self.name} learned something by watching TV! (Random trick)", self._learn_random_trick),
        ]
        
        for prob, message, action in events:
            if random.random() < prob:
                action()
                return message()
        return None

    def _learn_random_trick(self):
        random_tricks = ["sit", "roll over", "play dead", "spin", "jump"]
        new_trick = random.choice([t for t in random_tricks if t not in self.tricks])
        if new_trick:
            self.tricks.append(new_trick)

def main():
    print("🐾 Welcome to the Virtual Pet Simulator! 🐾")
    name = input("What would you like to name your pet? ")
    species = input(f"What species is {name}? (dog/cat/bird/etc) ") or "unknown"
    
    pet = Pet(name, species)
    
    # Add some default preferences based on species
    if species.lower() == "dog":
        pet.add_favorite_food("bone")
        pet.add_favorite_food("bacon")
        pet.add_disliked_food("chocolate")
    elif species.lower() == "cat":
        pet.add_favorite_food("fish")
        pet.add_favorite_food("chicken")
        pet.add_disliked_food("water")
    elif species.lower() == "bird":
        pet.add_favorite_food("seeds")
        pet.add_disliked_food("avocado")
    
    print(f"\nMeet your new {species}, {name}!")
    print(pet.speak())
    
    while True:
        print("\n" + "="*40)
        print(pet.get_status())
        print("\nWhat would you like to do?")
        print("1. Feed your pet")
        print("2. Play with your pet")
        print("3. Put your pet to sleep")
        print("4. Train your pet")
        print("5. Bathe your pet")
        print("6. Listen to your pet")
        print("7. Wait a while")
        print("8. Quit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == "1":
            food = input(f"What would you like to feed {name}? (leave blank for generic food) ")
            print(pet.eat(food))
        elif choice == "2":
            game = input("What game? (fetch/laser/default) ") or "default"
            print(pet.play(game))
        elif choice == "3":
            hours = input("How many hours should your pet sleep? (default 1) ") or "1"
            print(pet.sleep(float(hours)))
        elif choice == "4":
            trick = input("What trick would you like to teach? ")
            print(pet.train(trick))
        elif choice == "5":
            print(pet.bathe())
        elif choice == "6":
            print(f"{pet.name} says: {pet.speak()}")
        elif choice == "7":
            print(f"You watch {name} for a while...")
            event = pet.random_event()
            if event:
                print(event)
            else:
                print(f"{name} wanders around aimlessly.")
        elif choice == "8":
            print(f"Goodbye! {name} will miss you!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
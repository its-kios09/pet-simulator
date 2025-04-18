import pytest
from datetime import datetime, timedelta
from app.pet_simulator import Pet
import random


@pytest.fixture
def new_pet():
    """Fixture providing a fresh pet instance for each test"""
    pet = Pet("TestPet", "test_species")
    pet.energy_decay_rate = 0
    pet.happiness_decay_rate = 0
    pet.hunger_growth_rate = 0
    return pet


@pytest.fixture
def hungry_pet():
    """Fixture providing a pet with high hunger"""
    pet = Pet("HungryPet", "dog")
    pet.hunger = 9
    return pet


@pytest.fixture
def tired_pet():
    """Fixture providing a pet with low energy"""
    pet = Pet("TiredPet", "cat")
    pet.energy = 1
    return pet


@pytest.fixture
def happy_pet():
    """Fixture providing a happy pet"""
    pet = Pet("HappyPet", "bird")
    pet.happiness = 9
    return pet


@pytest.fixture
def decaying_pet():
    """Fixture providing a pet with stat decay enabled"""
    return Pet("DecayPet", "test_species")


def test_pet_initialization(new_pet):
    """Test pet initialization with default values"""
    assert new_pet.name == "TestPet"
    assert new_pet.species == "test_species"
    assert new_pet.hunger == 5
    assert new_pet.energy == 5
    assert new_pet.happiness == 5
    assert new_pet.hygiene == 5
    assert new_pet.health == 10
    assert new_pet.tricks == []
    assert isinstance(new_pet.birthday, datetime)
    assert new_pet.mood == "neutral"


def test_eat_generic_food(new_pet):
    """Test eating generic food"""
    initial_hunger = new_pet.hunger
    initial_energy = new_pet.energy
    result = new_pet.eat()

    assert "eating" in result.lower()
    assert new_pet.hunger < initial_hunger
    assert new_pet.energy > initial_energy
    assert "Hunger decreased by 3 points" in result
    assert new_pet.last_fed is not None


def test_eat_favorite_food(new_pet):
    """Test eating favorite food gives bonus"""
    new_pet.add_favorite_food("pizza")
    initial_hunger = new_pet.hunger
    result = new_pet.eat("pizza")

    assert "loves" in result.lower()
    assert new_pet.hunger == initial_hunger - 5  # 3 base + 2 bonus
    assert "Hunger decreased by 5 points" in result


def test_eat_disliked_food(new_pet):
    """Test eating disliked food gives penalty"""
    new_pet.add_disliked_food("broccoli")
    initial_hunger = new_pet.hunger
    result = new_pet.eat("broccoli")

    assert "doesn't like" in result.lower()
    assert new_pet.hunger == initial_hunger - 2
    assert "Hunger decreased by 2 points" in result


def test_sleep(new_pet):
    """Test sleeping restores energy"""
    new_pet.energy = 3
    result = new_pet.sleep(2)

    assert "slept for 2 hours" in result
    assert "Gained 4 energy" in result
    assert new_pet.energy == 7
    assert new_pet.hunger == 6


def test_play(new_pet):
    """Test playing increases happiness"""
    initial_energy = new_pet.energy
    initial_happiness = new_pet.happiness
    result = new_pet.play()

    assert "play" in result.lower()
    assert new_pet.happiness > initial_happiness
    assert new_pet.energy < initial_energy
    assert "Happiness +" in result
    assert "Energy -" in result


def test_play_when_tired(tired_pet):
    """Test pet refuses to play when tired"""
    initial_energy = tired_pet.energy
    result = tired_pet.play()

    assert "too tired" in result.lower()
    assert tired_pet.energy <= initial_energy


def test_train_success(new_pet, monkeypatch):
    """Test successful trick training"""
    monkeypatch.setattr(random, "random", lambda: 0.1)

    initial_energy = new_pet.energy
    initial_happiness = new_pet.happiness
    result = new_pet.train("sit")

    assert "Success" in result
    assert "sit" in new_pet.tricks
    assert new_pet.energy == initial_energy - 3
    assert new_pet.happiness == initial_happiness + 1


def test_train_failure(new_pet, monkeypatch):
    """Test failed trick training"""
    monkeypatch.setattr(random, "random", lambda: 0.9)

    initial_energy = new_pet.energy
    initial_happiness = new_pet.happiness
    result = new_pet.train("roll over")

    assert "didn't quite get it" in result
    assert "roll over" not in new_pet.tricks
    assert new_pet.energy == initial_energy - 2
    assert new_pet.happiness == initial_happiness - 0.5


def test_train_known_trick(new_pet):
    """Test pet won't learn known tricks"""
    new_pet.tricks.append("spin")
    initial_energy = new_pet.energy
    result = new_pet.train("spin")

    assert "already knows" in result
    assert new_pet.energy == initial_energy


def test_bathe(new_pet):
    """Test bathing improves hygiene"""
    new_pet.hygiene = 3
    initial_happiness = new_pet.happiness
    result = new_pet.bathe()

    assert "clean" in result.lower()
    assert new_pet.hygiene == 10
    assert new_pet.happiness == initial_happiness - 1


def test_mood_updates(new_pet):
    """Test mood changes based on stats"""
    # Test priority: sick > hungry > tired > happy > grumpy > neutral
    new_pet.health = 2
    new_pet._update_mood()
    assert new_pet.mood == "sick"

    new_pet.health = 10
    new_pet.hunger = 9
    new_pet._update_mood()
    assert new_pet.mood == "hungry"

    new_pet.hunger = 5
    new_pet.energy = 1
    new_pet._update_mood()
    assert new_pet.mood == "tired"

    new_pet.energy = 5
    new_pet.happiness = 8
    new_pet._update_mood()
    assert new_pet.mood == "happy"

    new_pet.happiness = 2
    new_pet._update_mood()
    assert new_pet.mood == "grumpy"

    new_pet.happiness = 5
    new_pet._update_mood()
    assert new_pet.mood == "neutral"


def test_random_event(new_pet, monkeypatch):
    """Test random events occur properly"""
    monkeypatch.setattr(random, "random", lambda: 0.05)  # Force event

    event = new_pet.random_event()
    assert event is not None
    assert any(
        phrase in event
        for phrase in ["found a toy", "bad dream", "exploring", "learned something"]
    )


def test_learn_random_trick(new_pet, monkeypatch):
    """Test pet can learn random tricks"""
    # Mock random choice to return "sit"
    monkeypatch.setattr(random, "choice", lambda x: "sit")

    new_pet._learn_random_trick()
    assert "sit" in new_pet.tricks


def test_get_age(new_pet):
    """Test age calculation"""
    # Mock birthday to be 1 day ago
    new_pet.birthday = datetime.now() - timedelta(days=1)
    age_str = new_pet.get_age()

    assert "day" in age_str or "00:00:00" in age_str


def test_status_display(new_pet):
    """Test status display contains all important info"""
    status = new_pet.get_status()

    assert "TestPet's Status" in status
    assert "Hunger" in status
    assert "Energy" in status
    assert "Happiness" in status
    assert "Hygiene" in status
    assert "Health" in status


def test_speak(new_pet):
    """Test pet speaks appropriately"""
    # Test neutral speech
    speech = new_pet.speak()
    assert speech in ["Hello!", "What's up?"]

    # Test happy speech
    new_pet.happiness = 8
    new_pet._update_mood()
    speech = new_pet.speak()
    assert speech in ["Purr purr!", "Wag wag!", "Chirp chirp!"]


def test_stat_decay(decaying_pet):
    """Test stats decay over time"""
    initial_energy = decaying_pet.energy
    initial_happiness = decaying_pet.happiness
    initial_hunger = decaying_pet.hunger

    decaying_pet._update_stats()

    assert decaying_pet.energy < initial_energy
    assert decaying_pet.happiness < initial_happiness
    assert decaying_pet.hunger > initial_hunger


def test_add_food_preferences(new_pet):
    """Test adding food preferences"""
    result = new_pet.add_favorite_food("chicken")
    assert "added" in result
    assert "chicken" in new_pet.favorite_foods

    result = new_pet.add_disliked_food("spinach")
    assert "added" in result
    assert "spinach" in new_pet.disliked_foods


def test_duplicate_food_preferences(new_pet):
    """Test duplicate food preferences"""
    new_pet.add_favorite_food("beef")
    result = new_pet.add_favorite_food("beef")
    assert "already" in result

    new_pet.add_disliked_food("carrots")
    result = new_pet.add_disliked_food("carrots")
    assert "already" in result

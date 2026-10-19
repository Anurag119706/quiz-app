"""Entry point - Terminal menu."""

from quiz import Quiz
from storage import print_history


def main():
    app = Quiz()

    while True:
        print("\n" + "=" * 60)
        print("QUIZ APP")
        print("=" * 60)
        print("1. Full quiz (all questions)")
        print("2. Quick quiz (5 questions)")
        print("3. Quiz by category")
        print("4. Quiz by difficulty")
        print("5. View history")
        print("6. Exit")

        choice = input("\nChoose (1-6): ").strip()

        if choice == "1":
            app.run()
        elif choice == "2":
            app.run(num=5)
        elif choice == "3":
            cat = input("Category (Programming/Math/Geography/Science/Computers):").strip()
            app.run(category=cat)
        elif choice == "4":
            diff = input("Difficulty (easy/medium/hard): ").strip()
            app.run(difficulty=diff)
        elif choice == "5":
            print_history()
        elif choice == "6":
            print("\n👋 BYE!")
            break
        else:
            print("INVALID CHOICE! PLEASE TRY AGAIN.")


if __name__ == "__main__":
    main()
"""Quiz logic: picking questions, running the round, and scoring."""

import random
from questions import DEFAULT_QUESTIONS
from storage import save_result

class Quiz:
    def __init__(self, questions=None, shuffle=True):
        self.questions = questions or DEFAULT_QUESTIONS
        self.shuffle = shuffle
        self.results = []
        self.score = 0

    def pick_questions(self, num=None, category=None, difficulty=None):
        """Filter and select questions for a round."""
        pool = self.questions

        if category:
            pool = [q for q in pool if q.get["category", ""].lower() == category.lower()]
        if difficulty:
            pool = [q for q in pool if q.get["difficulty", ""].lower() == difficulty.lower()]

        pool = list(pool)     # To avoid mutating the original
        if self.shuffle:
            random.shuffle(pool)
        if num:
            pool = pool[:num]
        return pool

    def run(self, num=None, category=None, difficulty=None):
        """Run an interactive quiz in the terminal."""

        questions = self.pick_questions(num, category, difficulty)
        if not questions:
            print("\nNo questions match those filters.")
            return

        self.score = 0
        self.results = []

        print("\n" + "=" * 60)
        print("QUIZ TIME!")
        print("=" * 60)
        print(f"Questions: {len(questions)} | Category: {category or 'All'} "
              f"|Difficulty: {difficulty or 'All'}\n")
        for i, q in enumerate(questions, 1):
            self._ask(q, i)

        self._show_results()

    def _ask(self, question, index):
        print(f"\n{'=' * 60}")
        print(f"Question {index}")
        print(f"=" * 60)
        print(f"\n{question['question']}\n")
        for i, opt in enumerate(question['options']):
            print(f" {i}. {opt}")

        answer = self._get_valid_input(len(question['options']))
        correct = answer == question['answer']

        if correct:
            self.score += 1
            print("CORRECT")
        else:
            print(f"WRONG. CORRECT ANSWER: {question['options'][question['answer']]}")

        self.results.append({
            "question": question['question'],
            "user_answer": question['options'][answer],
            "correct_answer": question['options'][question['answer']],
            "correct": correct
        })

    @staticmethod
    def _get_valid_input(max_choice):
        while True:
            try:
                choice = int(input(f"\nYour answer (0-{max_choice - 1}): "))
                if 1 <= choice <= max_choice:
                    return choice
                print(f"Enter a number between 1 and {max_choice - 1}.")
            except ValueError:
                print("Invalid input -- Enter a number.")

    def _show_results(self):
        total = len(self.results)
        percentage = (self.score / total) * 100

        print("\n" + "=" * 60)
        print(" 📊 QUIZ COMPLETE")
        print("=" * 60)
        print(f"\nScore: {self.score}/{total} ({percentage:.2f}%)")

        if percentage == 100:
            print("🏆 PERFECT SCORE!")
        elif percentage >= 80:
            print("🌟 GREAT JOB!")
        elif percentage >= 60:
            print("👍 GOOD EFFORT!")
        elif percentage >= 40:
            print("📚 KEEP PRACTICING!")
        else:
            print("💪 DON'T GIVE UP!")

        print("\nReview:")
        for i, r in enumerate(self.results, 1):
            mark = "✅" if r['correct'] else "❌"
            print(f"{mark} Q{i}: {r['question'][:55]}")

        save_result(self.score, total)
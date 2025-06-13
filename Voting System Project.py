#                                ------VOTING SYSTEM PROJECT-----


import random
from datetime import datetime

candidates = {
    "C1": 0,
    "C2": 0,
    "C3": 0
}

voters = set()

CANDIDATES_FILE = "CANDIDATES.txt"
VOTERS_FILE = "voters.txt"

def load_data():
    try:
        with open(CANDIDATES_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(":")
                    if len(parts) == 2:
                        name, count = parts
                        name = name.strip()
                        if name in candidates:
                            candidates[name] = int(count.strip())
    except FileNotFoundError:
        pass

    try:
        with open(VOTERS_FILE, "r") as f:
            for line in f:
                voter_id = line.strip()
                if voter_id:
                    voters.add(voter_id.lower())
    except FileNotFoundError:
        pass

def save_data():
    with open(CANDIDATES_FILE, "w") as f:
        for name, count in candidates.items():
            f.write(f"{name}:{count}\n")

    with open(VOTERS_FILE, "w") as f:
        for voter_id in voters:
            f.write(f"{voter_id}\n")

def display_candidates():
    print("\nCandidates:")
    for idx, name in enumerate(candidates, start=1):
        print(f"{idx}. {name}")

def generate_otp():
    return f"{random.randint(100000, 999999)}"

def vote(voter_id):
    voter_id = voter_id.strip().lower()

    if not voter_id:
        print("Invalid Voter ID!")
        return

    if voter_id in voters:
        print("You have already voted.")
        return

    otp = generate_otp()
    print(f"OTP sent to your registered contact: {otp}")

    entered_otp = input("Enter the OTP you received: ").strip()
    if entered_otp != otp:
        print("Incorrect OTP! Voting cancelled.")
        return

    display_candidates()
    try:
        choice = int(input("Enter the number of the candidate you want to vote for: "))
        candidate_list = list(candidates.keys())

        if 1 <= choice <= len(candidate_list):
            selected_candidate = candidate_list[choice - 1]
            candidates[selected_candidate] += 1
            voters.add(voter_id)
            save_data()

            timestamp = datetime.now().strftime("%d-%m-%y %H:%M:%S")
            with open(VOTERS_FILE, "a") as f:
                f.write(f"{voter_id} | {timestamp}\n")
                
            print(f"Thanks for voting, your vote for {selected_candidate} has been recorded.")
        else:
            print("Invalid candidate number!")
    except ValueError:
        print("Invalid input! Please enter a valid number.")

def show_results():
    print("\n--- Voting Results ---")
    for name, votes in candidates.items():
        print(f"{name}: {votes} vote(s)")

def show_winner():
    if not candidates:
        print("\nNo candidates available.")
        return

    max_votes = max(candidates.values())
    winners = [name for name, votes in candidates.items() if votes == max_votes]

    if len(winners) > 1:
        print("\nIt's a tie between:")
        for winner in winners:
            print(f"- {winner} with {candidates[winner]} vote(s)")
    else:
        print(f"\nThe winner is: {winners[0]} with {max_votes} vote(s)")

def add_candidate():
    new_name = input("Enter the name of the new candidate: ").strip()
    if not new_name:
        print("Candidate name cannot be empty.")
        return
    if new_name in candidates:
        print("Candidate already exists.")
        return
    candidates[new_name] = 0
    save_data()
    print(f"Candidate '{new_name}' added successfully.")

def remove_candidate():
    display_candidates()
    try:
        choice = int(input("Enter the number of the candidate to remove: "))
        candidate_list = list(candidates.keys())
        if 1 <= choice <= len(candidate_list):
            removed_candidate = candidate_list[choice - 1]
            confirm = input(f"Are you sure you want to remove '{removed_candidate}'? (y/n): ").lower()
            if confirm == 'y':
                del candidates[removed_candidate]
                save_data()
                print(f"Candidate '{removed_candidate}' removed successfully.")
                load_data()
            else:
                print("Removal cancelled.")
        else:
            print("Invalid candidate number!")
    except ValueError:
        print("Invalid input! Please enter a valid number.")

def reset_voters():
    confirm = input("Are you sure you want to reset all voter data? (y/n): ").lower()
    if confirm == 'y':
        voters.clear()
        with open(VOTERS_FILE, "w") as f:
            f.write("")  # Clears the file
        print("All voter data has been reset.")
    else:
        print("Reset cancelled.")

def reset_candidate_votes():
    confirm = input("Are you sure you want to reset all candidate votes to 0? (y/n): ").lower()
    if confirm == 'y':
        for name in candidates:
            candidates[name] = 0
        save_data()
        print("All candidate vote counts have been reset to 0.")
    else:
        print("Reset cancelled.")

def main():
    load_data()

    while True:
        print("\n---Main Menu---")
        print("1. Voter")
        print("2. Authority member")
        print("3. Exit")
        chc = input("Choose an option (1-3): ")

        if chc == '1':
            print("\n---Voting System Menu---")
            print("1. Vote")
            print("2. Show Results")
            print("3. Show Winner")
            print("4. Exit")
            chc2 = input("Enter your choice (1-4): ")

            if chc2 == '1':
                voter_id = input("Enter your Voter ID: ")
                vote(voter_id)
            elif chc2 == '2':
                show_results()
            elif chc2 == '3':
                show_winner()
            elif chc2 == '4':
                print("Thank you for using the Voting System!")
                break
            else:
                print("Invalid choice. Try again.")

        elif chc == '2':
            print("1. Show Results")
            print("2. Show Winner")
            print("3. Add Candidate")
            print("4. Remove Candidate")
            print("5. Reset Voters Data")
            print("6. Reset candidates votes")
            print("7. Exit")
            chc3 = input("Enter your choice (1-7): ")

            if chc3 == '1':
                show_results()
            elif chc3 == '2':
                show_winner()
            elif chc3 == '3':
                add_candidate()
            elif chc3 == '4':
                remove_candidate()
            elif chc3 == '5':
                reset_voters()
            elif chc3 == '6':
                reset_candidate_votes()
            elif chc3 == '7':
                print("Thank you for using the Voting System!")
                break
            else:
                print("Invalid choice. Try again.")

        elif chc == '3':
            print("Thank you for using the Voting System!")
            break

        else:
            print("Invalid choice. Try again.")

main()
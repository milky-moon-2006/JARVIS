def confirm_action(title, details=""):
    print("\n========== JARVIS SECURITY ==========")
    print(title)
    if details: print(details)
    answer=input("Type YES to continue: ").strip().lower()
    print("=====================================\n")
    return answer=="yes"
def is_exit(command):
    return command.strip().lower() in {"exit","quit","goodbye","goodbye jarvis","stop jarvis"}

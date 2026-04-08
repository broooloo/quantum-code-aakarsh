tasks = []

while True:
    print("\n1. Add Task\n2. View Tasks\n3. Delete Task\n4. Exit")
    choice = int(input("Enter choice: "))

    if choice == 1:
        task = input("Enter task: ")
        tasks.append(task)

    elif choice == 2:
        for i, t in enumerate(tasks):
            print(f"{i+1}. {t}")

    elif choice == 3:
        num = int(input("Enter task number: "))
        if 0 < num <= len(tasks):
            tasks.pop(num - 1)

    elif choice == 4:
        break

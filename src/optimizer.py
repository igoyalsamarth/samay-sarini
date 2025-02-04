from ortools.sat.python import cp_model

def samay_sarini(num_classes: int, num_periods: int, num_teachers: int):
    # Diagnostic checks
    print("\nAnalyzing parameters...")
    
    # Check 1: Basic teacher requirement
    min_teachers_needed = num_classes
    if num_teachers < min_teachers_needed:
        print(f"❌ Not enough teachers: {num_teachers} teachers cannot cover {num_classes} classes simultaneously")
        print(f"   Suggestion: Increase teachers to at least {min_teachers_needed}")
        return

    # Check 2: Teacher workload analysis
    total_slots_needed = num_classes * num_periods
    max_slots_per_teacher = 2 * num_classes  # max 2 periods per class
    total_slots_available = num_teachers * max_slots_per_teacher
    
    print("\nCurrent parameters:")
    print(f"- Classes: {num_classes}")
    print(f"- Periods: {num_periods}")
    print(f"- Teachers: {num_teachers}")
    print(f"\nConstraint analysis:")
    print(f"- Each teacher can teach max 2 periods per class")
    print(f"- Total teaching slots needed: {total_slots_needed}")
    print(f"- Total teaching slots available: {total_slots_available}")

    if total_slots_available < total_slots_needed:
        print(f"\n❌ Impossible configuration:")
        print(f"   Need {total_slots_needed} slots but only {total_slots_available} available")
        suggested_teachers = (total_slots_needed + max_slots_per_teacher - 1) // max_slots_per_teacher
        print(f"\nSuggestions to fix:")
        print(f"1. Increase teachers to at least {suggested_teachers}")
        print(f"2. OR Decrease classes to {total_slots_available // num_periods}")
        print(f"3. OR Increase periods to spread the load")
        return

    print("\n✓ Parameter check passed, attempting to find solution...")

    model = cp_model.CpModel()

    X = {}
    for c in range(num_classes):
        for p in range(num_periods):
            for t in range(num_teachers):
                X[c, p, t] = model.NewBoolVar(f'teacher_{c}_{p}_{t}')

    # Constraint: A teacher cannot be assigned to multiple classes in the same period
    for p in range(num_periods):
        for t in range(num_teachers):
            model.Add(sum(X[c, p, t] for c in range(num_classes)) <= 1)

    # Constraint: Each class must have exactly one teacher per period
    for c in range(num_classes):
        for p in range(num_periods):
            model.Add(sum(X[c, p, t] for t in range(num_teachers)) == 1)

    # Constraint: No teacher can teach more than 2 periods in any single class
    for t in range(num_teachers):
        for c in range(num_classes):
            model.Add(sum(X[c, p, t] for p in range(num_periods)) <= 2)

    # Solve with time limit
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0  # 30 second timeout
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print("\n✓ Solution found!")
        
        # Store the schedule for analysis
        schedule = {}
        for c in range(num_classes):
            print(f"\nClass {c}")
            print("-" * 20)
            print("Period | Teacher")
            print("-" * 20)
            for p in range(num_periods):
                for t in range(num_teachers):
                    if solver.Value(X[c, p, t]):
                        print(f"{p:6d} | {t:7d}")
                        if p not in schedule:
                            schedule[p] = set()
                        schedule[p].add(t)
        
        # Print free teachers per period
        print("\nFree Teachers Analysis:")
        print("-" * 40)
        print("Period | Free Teachers")
        print("-" * 40)
        for p in range(num_periods):
            busy_teachers = schedule.get(p, set())
            free_teachers = set(range(num_teachers)) - busy_teachers
            free_count = len(free_teachers)
            print(f"{p:6d} | {free_count:2d} teachers free: {sorted(free_teachers)}")
            
    else:
        print("\n❌ No solution found!")
        if status == cp_model.INFEASIBLE:
            print("The problem is infeasible with current parameters.")
        elif status == cp_model.MODEL_INVALID:
            print("The model is invalid - please check parameters.")
        else:
            print("The solver timed out or failed to find a solution.")
        
        print("\nTry:")
        print("1. Increasing the number of teachers")
        print("2. Decreasing the number of classes")
        print("3. Increasing the number of periods")

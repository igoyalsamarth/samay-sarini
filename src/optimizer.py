from ortools.sat.python import cp_model
from typing import Dict, List

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

def samay_sarini(teachers: Dict, num_classes: int, num_periods: int):
    model = cp_model.CpModel()
    
    # Constants setup
    FULL_DAY_PERIODS = num_periods
    HALF_DAY_PERIODS = FULL_DAY_PERIODS - (FULL_DAY_PERIODS // 2)
    num_teachers = len(teachers)
    teacher_names = list(teachers.keys())
    
    # Create subject to teachers mapping
    subject_to_teachers = {}
    for teacher_name, teacher_data in teachers.items():
        for subject in teacher_data['subjects']:
            if subject not in subject_to_teachers:
                subject_to_teachers[subject] = []
            subject_to_teachers[subject].append(teacher_name)

    # Decision Variables
    X = {}  # X[d, c, p, t] = 1 if teacher t teaches class c in period p on day d
    for d in range(len(DAYS)):
        max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
        for c in range(num_classes):
            for p in range(max_periods):
                for t in range(num_teachers):
                    X[d, c, p, t] = model.NewBoolVar(f'teacher_{d}_{c}_{p}_{t}')

    # Create variables to track total periods for each teacher-class combination
    total_periods = {}
    for t in range(num_teachers):
        for c in range(num_classes):
            total_periods[t, c] = model.NewIntVar(0, num_periods * len(DAYS), f'total_periods_{t}_{c}')
            
            # Link to actual assignments
            periods = []
            for d in range(len(DAYS)):
                max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
                for p in range(max_periods):
                    periods.append(X[d, c, p, t])
            model.Add(total_periods[t, c] == sum(periods))

    # 1. No teacher in more than 1 class at a time
    for d in range(len(DAYS)):
        max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
        for p in range(max_periods):
            for t in range(num_teachers):
                model.Add(sum(X[d, c, p, t] for c in range(num_classes)) <= 1)

    # Each class must have exactly one teacher per period
    for d in range(len(DAYS)):
        max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
        for c in range(num_classes):
            for p in range(max_periods):
                model.Add(sum(X[d, c, p, t] for t in range(num_teachers)) == 1)

    # NEW: Subject should not be taught more than twice in a day
    for d in range(len(DAYS)):
        max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
        for c in range(num_classes):
            for subject, subject_teachers in subject_to_teachers.items():
                teacher_indices = [teacher_names.index(t) for t in subject_teachers]
                daily_periods = []
                for p in range(max_periods):
                    for t in teacher_indices:
                        daily_periods.append(X[d, c, p, t])
                model.Add(sum(daily_periods) <= 2)

    # Subject exclusivity (except for common subjects)
    for subject, subject_teachers in subject_to_teachers.items():
        if any(teachers[t].get('common_for_all_classes', False) for t in subject_teachers):
            continue
            
        for c in range(num_classes):
            teaches = {}
            for teacher_name in subject_teachers:
                t = teacher_names.index(teacher_name)
                teaches[t] = model.NewBoolVar(f'teaches_{subject}_{c}_{t}')
                
                periods = []
                for d in range(len(DAYS)):
                    max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
                    for p in range(max_periods):
                        periods.append(X[d, c, p, t])
                
                model.Add(sum(periods) > 0).OnlyEnforceIf(teaches[t])
                model.Add(sum(periods) == 0).OnlyEnforceIf(teaches[t].Not())
            
            model.Add(sum(teaches[t] for t in teaches.keys()) == 1)

    # First period homeroom teacher constraint
    for c in range(num_classes):
        model.Add(sum(X[0, c, 0, t] for t in range(num_teachers)) == 1)
        
        for t in range(num_teachers):
            if teachers[teacher_names[t]].get('class_teacher_preference', False):
                for d in range(1, len(DAYS)):
                    model.Add(X[d, c, 0, t] == X[0, c, 0, t])

    # No more than 2 consecutive periods
    for d in range(len(DAYS)):
        max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
        for c in range(num_classes):
            for p in range(max_periods - 2):
                for t in range(num_teachers):
                    consecutive_periods = [X[d, c, p+i, t] for i in range(3)]
                    model.Add(sum(consecutive_periods) <= 2)

    # Weekly period constraints
    for teacher_name, teacher_data in teachers.items():
        t = teacher_names.index(teacher_name)
        weekly_limit = teacher_data.get('weekly_periods')
        
        if weekly_limit is not None:
            for c in range(num_classes):
                if teacher_data.get('common_for_all_classes', False):
                    model.Add(total_periods[t, c] == weekly_limit)
                else:
                    model.Add(total_periods[t, c] <= weekly_limit)

    # NEW: Balance teaching load
    # Create variables for total periods per teacher across all classes
    teacher_total_periods = {}
    for t in range(num_teachers):
        teacher_total_periods[t] = model.NewIntVar(0, num_periods * len(DAYS) * num_classes, f'teacher_total_{t}')
        model.Add(teacher_total_periods[t] == sum(total_periods[t, c] for c in range(num_classes)))

    # Create variables for the difference between max and min teaching load
    max_teaching_load = model.NewIntVar(0, num_periods * len(DAYS) * num_classes, 'max_load')
    min_teaching_load = model.NewIntVar(0, num_periods * len(DAYS) * num_classes, 'min_load')

    # Link max and min variables
    for t in range(num_teachers):
        if not teachers[teacher_names[t]].get('weekly_periods'):  # Only for non-constrained teachers
            model.Add(max_teaching_load >= teacher_total_periods[t])
            model.Add(min_teaching_load <= teacher_total_periods[t])

    # Objective: Maximize periods while minimizing the difference in teaching loads
    objective_terms = []
    for teacher_name, teacher_data in teachers.items():
        t = teacher_names.index(teacher_name)
        if not teacher_data.get('weekly_periods'):
            for c in range(num_classes):
                objective_terms.append(total_periods[t, c])
    
    # Add balance term to objective (with smaller weight)
    load_difference = model.NewIntVar(0, num_periods * len(DAYS) * num_classes, 'load_diff')
    model.Add(load_difference == max_teaching_load - min_teaching_load)
    
    if objective_terms:
        model.Maximize(sum(objective_terms) - load_difference)

    # Solve and print results
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 300
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        print("\n✓ Solution found!")
        
        # Print schedule
        for d in range(len(DAYS)):
            print(f"\n{DAYS[d]}")
            print("=" * 50)
            max_periods = HALF_DAY_PERIODS if d == 5 else FULL_DAY_PERIODS
            
            print(f"{'Period':8} | ", end="")
            for c in range(num_classes):
                print(f"Class {c:2} | ", end="")
            print()
            print("-" * 50)
            
            for p in range(max_periods):
                print(f"{p:8} | ", end="")
                for c in range(num_classes):
                    teacher_assigned = None
                    for t in range(num_teachers):
                        if solver.Value(X[d, c, p, t]):
                            teacher_assigned = teacher_names[t]
                            break
                    print(f"{teacher_assigned[:6]:8} | ", end="")
                print()

        # Print weekly totals and load distribution
        print("\nWeekly periods per teacher per class:")
        print("=" * 50)
        for t in range(num_teachers):
            teacher_name = teacher_names[t]
            total = solver.Value(teacher_total_periods[t])
            print(f"\n{teacher_name} (Total: {total} periods):")
            for c in range(num_classes):
                class_total = solver.Value(total_periods[t, c])
                print(f"  Class {c}: {class_total} periods")
                
    else:
        print("\n❌ No solution found!")
        print("Try adjusting the constraints or increasing the solver time limit.")

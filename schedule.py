from pulp import LpProblem, LpMinimize, LpVariable, lpSum, GUROBI

# Define the problem
prob = LpProblem("Scheduling_Problem", LpMinimize)

# Define decision variables (example: shift assignment)
# shifts = ["morning", "afternoon", "night"]
sys_shifts = [f"sys_{x}" for x in range(1, 28)]
ste_shifts = [f"ste_{x}" for x in range(1, 28)]
con_shifts = [f"con_{x}" for x in range(1, 28)]
shifts = [*sys_shifts, *ste_shifts, *con_shifts]
print(shifts)
employees = ["A", "B", "C", "D", "E"]
x = LpVariable.dicts("assign", [(e, s) for e in employees for s in shifts], cat='Binary')
max_shifts = LpVariable("Max_Shifts", lowBound=0, cat='Integer')

# Define objective function (example: minimize number of employees working)
prob += lpSum([x[e, s] for e in employees for s in shifts])

# Define constraints (example: each shift needs at least one employee)
for s in shifts:
    prob += lpSum([x[e, s] for e in employees]) == 1

# set max shifts per employee
for e in employees:
    prob += lpSum(x[e, s] for s in sys_shifts) == 9, f"Max_Sys_Shifts_Limit_{e}" # Limit shifts per person
    prob += max_shifts >= lpSum(x[e, s] for s in sys_shifts), f"Link_Max_Sys_Shifts_{e}" # Link max_shifts to the actual shifts
# set max shifts per employee
for e in employees:
    prob += lpSum(x[e, s] for s in ste_shifts) == 9, f"Max_Ste_Shifts_Limit_{e}" # Limit shifts per person
    prob += max_shifts >= lpSum(x[e, s] for s in ste_shifts), f"Link_Max_Ste_Shifts_{e}" # Link max_shifts to the actual shifts
# set max shifts per employee
for e in employees:
    prob += lpSum(x[e, s] for s in con_shifts) == 9, f"Max_Con_Shifts_Limit_{e}" # Limit shifts per person
    prob += max_shifts >= lpSum(x[e, s] for s in con_shifts), f"Link_Max_Con_Shifts_{e}" # Link max_shifts to the actual shifts

# Add more constraints as needed, e.g.,
# - An employee can work at most one shift per day
# - Specific employees are not available for certain shifts
solver = GUROBI()
# Solve the problem
prob.solve(solver=solver)

# Print the results
print("Status:", prob.status)
for v in prob.variables():
    if v.varValue == 1.0:
        print(v.name, "=", v.varValue)
print("Objective Value =", prob.objective.value())

import random
import math
from algo import data

# Estructura de Datos:
evaluations = data()  # Lista de evaluaciones con sus datos (por ejemplo, ID, semestre, preferencias de horario, etc.).
time_blocks = [1,2,3,4]  # Lista de bloques horarios disponibles 8:30-10:45; 11:00-13:15; 13:30-15:45; 16:00-18:15.
days= [1,2,3,4,5] #Lista de días para realizar las evaluaciones. Lunes, Martes, Miércoles, Jueves y Viernes.
restricciones = []

# Función de evaluación
def evaluate_solution(schedule):
    penalty = 0
    for day in schedule:
        semesters_in_day = set()
        #print(semesters_in_day)
        for subject in day:
            semester = find_semester(subject)
            #print(subject)
            #print(semester)
            if semester in semesters_in_day:
                #print(subject+' es del semestre ',semester)
                penalty += 1
            semesters_in_day.add(semester)
    print('Solucion: '+str(schedule)+' penalización: '+str(penalty))
    return penalty

# Función para encontrar el semestre de una asignatura
def find_semester(subject):
    for i, semester_data in enumerate(evaluations):
        if subject in semester_data['Asignaturas']:
            return i

# Función para identificar restricciones incumplidas
def identify_unresolved_constraints(schedule):
    unresolved_constraints = []

    # Implementa la lógica para identificar restricciones incumplidas, como pruebas del mismo semestre en el mismo día
    for day in schedule:
        semesters_in_day = set()
        #print(semesters_in_day)
        for subject in day:
            semester = find_semester(subject)
            #print(subject)
            #print(semester)
            if semester in semesters_in_day:
                #print(subject+' es del semestre ',semester)
                unresolved_constraints.append('same_semester')
            semesters_in_day.add(semester)
            
    return unresolved_constraints

# Función para encontrar otro día disponible para mover un curso
def find_another_day(current_day, scheduled_days):
    # Implementa la lógica para encontrar otro día disponible
    # Puedes utilizar estrategias aleatorias, secuenciales o basadas en prioridades
    # En este ejemplo, simplemente se selecciona un día diferente al actual
    all_days = set(range(len(evaluations)))
    available_days = all_days - scheduled_days
    if current_day in available_days:
        available_days.remove(current_day)
    return available_days.pop() if available_days else current_day

# Función para mover un curso de un día a otro
def move_course(schedule, from_day, to_day, course):
    schedule[from_day].remove(course)
    schedule[to_day-1].append(course)
    
# Heurística para abordar restricciones incumplidas (no agendar pruebas del mismo semestre en el mismo día)
def resolve_semester_same_day(schedule, evaluations):
    # Crear un diccionario que mapee semestres a días programados
    semesters_to_days = {}

    # Crear un nuevo horario para la solución corregida
    new_schedule = [[] for _ in range(len(schedule))]

    for day, day_schedule in enumerate(schedule):
        for course in day_schedule:
            # Obtener el semestre del curso desde las evaluaciones
            semester = find_semester(course)

            if semester is not None:
                # Verificar si ya hay un curso del mismo semestre en el día
                if semester in semesters_to_days and day in semesters_to_days[semester]:
                    # Si se incumple la restricción, encontrar otro día y agregar la asignatura allí
                    new_day = find_another_day(day, semesters_to_days[semester]) - 1
                    print(new_day)
                    new_schedule[new_day].append(course)
                    # Actualizar el registro de días programados para el semestre
                    semesters_to_days[semester].add(new_day)
                else:
                    # Si no hay cursos del mismo semestre en el día, agregar la asignatura al mismo día
                    semesters_to_days.setdefault(semester, set()).add(day)
                    new_schedule[day].append(course)

    return new_schedule

    #subjects = sum((semester_data['Asignaturas'] for semester_data in evaluations), [])
    #random.shuffle(subjects)
    #for i, subject in enumerate(subjects):
    #    day_index = i % len(days)
    #    schedule[day_index].append(subject)
    ##print(schedule)
    #return schedule

# Genera una solución inicial (personalizar según tus datos)
def generate_initial_solution(evaluations, time_blocks, days):
    schedule = [[] for _ in range(len(days))]
    #print(schedule)
    subjects = sum((semester_data['Asignaturas'] for semester_data in evaluations), [])
    random.shuffle(subjects)
    for i, subject in enumerate(subjects):
        day_index = i % len(days)
        schedule[day_index].append(subject)
    print(len(schedule))
    return schedule

# Genera una solución vecina (personalizar según tus datos)
def generate_neighbor_solution(current_solution):
    
    pass

# Hiperheurística de Simulated Annealing:
def simulated_annealing_hyperheuristic(max_iterations, initial_temperature, cooling_rate):
    current_solution = generate_initial_solution(evaluations, time_blocks, days)  # Genera una solución inicial
    current_score = evaluate_solution(current_solution)
    best_solution = current_solution
    best_score = current_score
    temperature = initial_temperature

    for iteration in range(max_iterations):
        # Identifica restricciones incumplidas
        unresolved_constraints = identify_unresolved_constraints(current_solution)

        # Selecciona la heurística de bajo nivel en función de la prioridad de la restricción. Genera nuevo vecino.
        if "same_semester" in unresolved_constraints:
            current_schedule = resolve_semester_same_day(current_solution,evaluations)
            # Evalúa la calidad de la solución resultante
            neighbor_score = evaluate_solution(current_schedule)
            print(current_schedule)
        
        # Calcula la diferencia de calidad y aplica el criterio de aceptación de SA
        delta_score = neighbor_score - current_score
        
        # Acepta la solución vecina con una cierta probabilidad
        if delta_score < 0 or random.random() < math.exp(-delta_score / temperature):
            current_solution = current_schedule
            current_score = neighbor_score

        # Actualiza la mejor solución si es necesario
        if current_score < best_score:
            best_solution = current_schedule
            best_score = current_score

        # Reduce la temperatura
        temperature *= cooling_rate
        
        # Genera una solución vecina modificando la solución actual
        #neighbor_solution = generate_neighbor_solution(current_schedule)
        #print(neighbor_solution)
        #neighbor_score = evaluate_solution(neighbor_solution)
    return best_solution
# Parámetros
max_iterations = 1000
initial_temperature = 1.0
cooling_rate = 0.95

# Ejecuta la hiperheurística de Simulated Annealing
best_solution = simulated_annealing_hyperheuristic(max_iterations, initial_temperature, cooling_rate)

# Imprime la mejor solución encontrada
print("Mejor solución encontrada:")
print(best_solution)

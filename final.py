import random
import math
from algo import data

# Lista de evaluaciones EIT con sus datos (por ejemplo, ID, semestre, preferencias de horario, etc.)
evaluations = data() 

# Parámetros globales
time_blocks_simplified = list(range(1, 5))
constraints = ['same_semester','max_evaluations_in_block']
days = ['Lunes','Martes','Miercoles','Jueves','Viernes']

# Función de evaluación
def evaluate_solution(schedule):
    penalty = {
        'same_semester': 0,
        'max_evaluations_in_block': 0
    }
    
    for day in schedule:
        semesters_in_day = set()  # Agrega los semestres que contienen pruebas agendadas en el día
        # Diccionario para realizar un seguimiento del número de evaluaciones por bloque de tiempo
        block_counts = {block: 0 for block in time_blocks_simplified}
        
        for subject, block in day:
            # Restricción de pruebas del mismo semestre en el mismo día. 
            semester = find_semester(subject)
            if semester in semesters_in_day:
                penalty['same_semester'] += 1
            semesters_in_day.add(semester)
            
            # Restricción de máximo de evaluaciones por bloque de tiempo
            if block_counts[block] > 8:
                penalty['max_evaluations_in_block'] += 1
            else:
                # Actualiza el conteo de evaluaciones para el bloque de tiempo actual
                block_counts[block] += 1
        
    print('Solucion: ' + str(schedule) + ' penalizacion: ' + str(penalty))
    return penalty

# Genera una solución inicial (personalizar según tus datos)
def generate_initial_solution(evaluations, time_blocks_simplified, days):
    subjects = sum((semester_data['Semestre'] for semester_data in evaluations), [])
    
    # Asigna aleatoriamente bloques de tiempo a todas las asignaturas
    subjects_with_time_blocks = [(subject, random.choice(time_blocks_simplified)) for subject in subjects]
    
    schedule = [[] for _ in range(len(days))]
    
    # Distribuye las asignaturas con sus bloques de tiempo en los días de schedule
    for subject, block_start in subjects_with_time_blocks:
        # Encuentra el índice del día en el que asignar la asignatura
        day_index = random.randint(0, len(days) - 1)
        schedule[day_index].append((subject, block_start))

    return schedule

# Heurística que identifica que heurística aplicar a constraint 
def identify_unresolved_constraints(current_score, constraints):
    total = sum(current_score.values())
    probabilidades = []
    numeros_posibles = []

    for constraint in constraints:
        probabilidades.append(current_score[constraint]/total)
        numeros_posibles.append(current_score[constraint])  # Reemplaza "otro_numero" con el valor que desees para la segunda probabilidad
    #print(probabilidades)
    
    numero_generado = random.choices(numeros_posibles, probabilidades)[0]
    #print(numero_generado)
    for constraint, score in current_score.items():
        if score == numero_generado:
            #print(constraint)
            return constraint
            
# Función para encontrar otro día disponible para mover un curso
def find_another_day(current_day, scheduled_days):
    # Implementa la lógica para encontrar otro día disponible
    # Puedes utilizar estrategias aleatorias, secuenciales o basadas en prioridades
    # En este ejemplo, simplemente se selecciona un día diferente al actual
    available_days = set(range(len(scheduled_days)))
    if current_day in available_days:
        available_days.remove(current_day)
    return available_days.pop() if available_days else current_day
   
# Heurística para abordar restricciones incumplidas (no agendar pruebas del mismo semestre en el mismo día)
def resolve_same_semester_same_day(schedule, evaluations):

    while True:
        # Crear una copia de la solución actual
        neighbor_solution = [day[:] for day in schedule]
        
        # Elegir un día aleatorio
        day = random.choice(range(len(schedule)))
        
        for evaluation in neighbor_solution[day]:
            for evaluation2 in neighbor_solution[day]:
                if evaluation[0] != evaluation2[0] and find_semester(evaluation[0]) == find_semester(evaluation2[0]):
                    neighbor_solution[day].remove(evaluation2)
                    #print(set(range(len(schedule))))
                    new_day = find_another_day(day, set(range(len(schedule))))
                    neighbor_solution[new_day].append(evaluation2)
                    return neighbor_solution

# Hiperheurística de Simulated Annealing:
def simulated_annealing_hyperheuristic(max_iterations, initial_temperature, cooling_rate):
    current_solution = generate_initial_solution(evaluations, time_blocks_simplified, days)  # Genera una solución inicial
    best_solution = current_solution # Mejor solución actual
        
    current_score = evaluate_solution(current_solution)
    
    best_score = sum(current_score.values())
    
    temperature = initial_temperature

    for iteration in range(max_iterations):
        if sum(current_score.values()) == 0:
            return best_solution
        constraint_resolve = identify_unresolved_constraints(current_score, constraints)
    
        if constraint_resolve == constraints[0]:
            neighbor_solution = resolve_same_semester_same_day(current_solution,evaluations)
            neighbor_score = evaluate_solution(neighbor_solution)
            neighbor_score_total = sum(neighbor_score.values())
        
        elif constraint_resolve == constraints[1]:
            #agregar la restricción
            pass
        
        # Calcula la diferencia de calidad y aplica el criterio de aceptación de SA.
        delta_score = neighbor_score_total - best_score
            
        # Decide si aceptar la solución peor
        if delta_score < 0 or random.random() < math.exp(-delta_score/temperature):
            best_solution = neighbor_solution
            current_solution = neighbor_solution
            best_score = neighbor_score_total
            current_score = neighbor_score
            print('aceptada')
            
        # Reduce la temperatura
        temperature *= cooling_rate

    return best_solution        
                
# Parámetros Simulated Annealing
max_iterations = 100000
initial_temperature = 1.0
cooling_rate = 0.97

# Ejecutar Hiperheurística de Simulated Annealing
best_solution = simulated_annealing_hyperheuristic(max_iterations, initial_temperature, cooling_rate)

# Imprime la mejor solución encontrada
print("Mejor solución encontrada: " +str(best_solution))


def has_same_semester_evaluation(evaluation, day_evaluations, evaluations):
    subject, _ = evaluation
    semester = find_semester(subject)

    # Obtener todas las evaluaciones del mismo semestre en el día
    same_semester_evaluations = [(s, b) for s, b in day_evaluations if find_semester(s) == semester]

    if len(same_semester_evaluations) > 1:
        # Obtener una de las pruebas del mismo semestre en el día
        other_evaluation = random.choice(same_semester_evaluations)
        return other_evaluation

    return None

#Criterio de aceptación de Simulated Annealing
def accept_peor(delta_score,temperature):
    print(delta_score)
    print(temperature)
    if delta_score == 0:
        # Introduce una probabilidad adicional cuando delta_score es 0
        probabilidad_adicional = 0.1  # Puedes ajustar este valor según tus necesidades
        if random.uniform(0, 1) < probabilidad_adicional:
            print('hola2')
            return True
    else:
        if random.random() < math.exp(-delta_score / temperature):
            print('hola')
            return True

# Función para encontrar el semestre de una asignatura
def find_semester(subject):
    for i, semester_data in enumerate(evaluations):
        #print(subject[0])
        if subject in semester_data['Semestre']:
            return i
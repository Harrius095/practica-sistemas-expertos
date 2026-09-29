import collections
import collections.abc
collections.Mapping = collections.abc.Mapping

from experta import *
# ==========================================
# PARTE 1: Definición de hechos
# ==========================================

class Sintoma(Fact):
    """
    Representa un síntoma o conjunto de síntomas presentados por el paciente. 
    Recibe atributos con valor booleano (ej. fiebre=True).
    """
    pass

class Diagnostico(Fact):
    """
    Almacena el nombre de la enfermedad identificada por el motor de inferencia.
    """
    pass


# ==========================================
# PARTE 2 Y EJERCICIO 1: Construcción del Sistema
# ==========================================

class DiagnosticoMedico(KnowledgeEngine):
    
    # --- Reglas Originales (Parte 2) ---
    
    @Rule(Sintoma(fiebre=True, tos=True, dolor_garganta=True))
    def regla_gripe(self):
        self.declare(Diagnostico(enfermedad="Gripe"))
        print("Diagnóstico: Gripe. Recomendación: Descanse, tome abundantes líquidos y analgésicos.")

    @Rule(Sintoma(fiebre=True, dolor_cabeza=True, nauseas=True))
    def regla_migrana(self):
        self.declare(Diagnostico(enfermedad="Migraña"))
        print("Diagnóstico: Migraña. Recomendación: Descanse en una habitación oscura y silenciosa.")

    @Rule(Sintoma(estornudos=True, congestion_nasal=True, picazon_ojos=True))
    def regla_alergia(self):
        self.declare(Diagnostico(enfermedad="Alergia"))
        print("Diagnóstico: Alergia. Recomendación: Tome antihistamínicos y evite la exposición al alérgeno.")

    @Rule(Sintoma(dolor_estomago=True, diarrea=True, vomitos=True))
    def regla_gastroenteritis(self):
        self.declare(Diagnostico(enfermedad="Gastroenteritis"))
        print("Diagnóstico: Gastroenteritis. Recomendación: Manténgase hidratado, consuma suero y dieta blanda.")

    # --- Nuevas Reglas (Ejercicio 1) ---
    
    @Rule(Sintoma(fiebre=True, tos_seca=True, perdida_olfato=True))
    def regla_covid19(self):
        self.declare(Diagnostico(enfermedad="COVID-19"))
        print("Diagnóstico: COVID-19. Recomendación: Aíslese inmediatamente, use mascarilla y contacte a su médico.")

    @Rule(Sintoma(congestion_nasal=True, estornudos=True, tos_leve=True))
    def regla_resfriado_comun(self):
        self.declare(Diagnostico(enfermedad="Resfriado común"))
        print("Diagnóstico: Resfriado común. Recomendación: Descanse y tome bebidas calientes.")

    @Rule(Sintoma(tos_persistente=True, produccion_flema=True, dificultad_respiratoria=True))
    def regla_bronquitis(self):
        self.declare(Diagnostico(enfermedad="Bronquitis"))
        print("Diagnóstico: Bronquitis. Recomendación: Consulte a un médico, evite irritantes pulmonares y descanse.")

    # Enfermedad personalizada
    @Rule(Sintoma(fiebre=True, dolor_articulaciones=True, sarpullido=True))
    def regla_dengue(self):
        self.declare(Diagnostico(enfermedad="Dengue"))
        print("Diagnóstico: Dengue. Recomendación: Hidratación constante, tome paracetamol y acuda al médico de urgencia.")

    # --- Regla de Respaldo ---
    # Se usa un 'salience' negativo para que el motor evalúe esta regla al final.
    # Se activa si en la memoria de trabajo no existe el hecho "Diagnostico".
    @Rule(NOT(Diagnostico()), salience=-10)
    def regla_respaldo(self):
        print("Resultado: No se pudo determinar un diagnóstico claro. Recomendación: Por favor, consulte a un médico para una evaluación detallada.")


# ==========================================
# PARTE 3 Y EJERCICIOS: Ejecución de casos de prueba
# ==========================================

def ejecutar_casos():
    engine = DiagnosticoMedico()

    print("--- Caso 1: Fiebre, tos, dolor de garganta ---")
    engine.reset()
    engine.declare(Sintoma(fiebre=True, tos=True, dolor_garganta=True))
    engine.run()

    print("\n--- Caso 2: Estornudos, congestión nasal, picazón en los ojos ---")
    engine.reset()
    engine.declare(Sintoma(estornudos=True, congestion_nasal=True, picazon_ojos=True))
    engine.run()

    print("\n--- Caso 3: Dolor de estómago, diarrea, vómitos ---")
    engine.reset()
    engine.declare(Sintoma(dolor_estomago=True, diarrea=True, vomitos=True))
    engine.run()

    print("\n--- Caso 4: Síntomas desconocidos (Cansancio, mareo) ---")
    engine.reset()
    engine.declare(Sintoma(cansancio=True, mareo=True))
    engine.run()

    print("\n--- Caso 5 (Y Ejercicio 2): Múltiples síntomas simultáneos (Conflicto) ---")
    # Mezclamos síntomas de Gripe y de Alergia a la vez
    engine.reset()
    engine.declare(Sintoma(fiebre=True, tos=True, dolor_garganta=True, estornudos=True, congestion_nasal=True, picazon_ojos=True))
    engine.run()
    
    print("\n--- Pruebas de nuevas enfermedades (Ejercicio 1) ---")
    print("\nPrueba Dengue:")
    engine.reset()
    engine.declare(Sintoma(fiebre=True, dolor_articulaciones=True, sarpullido=True))
    engine.run()

if __name__ == "__main__":
    ejecutar_casos()
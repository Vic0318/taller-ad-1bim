from configuracion import obtener_sesion
from crear_base_entidades import RecursoAcademico, Profesor, Carrera, Facultad

def consulta_nueva():
    session = obtener_sesion()
    try:
        nombre_facultad = "Facultad de Ingeniería"
        print(f"--- CONSULTA NUEVA: Recursos académicos de la '{nombre_facultad}' ---")
        
        # Realizar join a través de Profesor, Carrera y Facultad para filtrar por el nombre de la facultad
        recursos = session.query(RecursoAcademico)\
            .join(Profesor)\
            .join(Carrera)\
            .join(Facultad)\
            .filter(Facultad.nombre == nombre_facultad)\
            .all()
            
        if recursos:
            for rec in recursos:
                print(f"Recurso: '{rec.titulo}' | Tipo: {rec.tipo}")
                print(f"  Profesor: {rec.profesor.nombres} {rec.profesor.apellidos} (Carrera: {rec.profesor.carrera.nombre})")
                print(f"  URL: {rec.url}")
                print("-" * 50)
        else:
            print(f"No se encontraron recursos académicos para la {nombre_facultad}")
    except Exception as e:
        print(f"Error en consulta_nueva: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    consulta_nueva()

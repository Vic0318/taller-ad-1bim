from sqlalchemy import and_
from configuracion import obtener_sesion
from crear_base_entidades import Profesor, Carrera

def consulta_and():
    session = obtener_sesion()
    try:
        print("--- CONSULTA: AND (Filtrar Profesores de la carrera 'Ingeniería en Software' Y especialidad 'Bases de Datos') ---")
        # Podemos hacer un join con Carrera para buscar por el nombre de la carrera
        profesores = session.query(Profesor).join(Carrera).filter(
            and_(
                Carrera.nombre == "Ingeniería en Software",
                Profesor.especialidad == "Bases de Datos"
            )
        ).all()
        
        for prof in profesores:
            print(f"Profesor: {prof.nombres} {prof.apellidos} | Correo: {prof.correo}")
            print(f"  Carrera: {prof.carrera.nombre} | Especialidad: {prof.especialidad}")
            print("-" * 50)
    except Exception as e:
        print(f"Error en consulta_and: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    consulta_and()

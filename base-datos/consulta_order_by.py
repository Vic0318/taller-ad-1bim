from configuracion import obtener_sesion
from crear_base_entidades import Profesor

def consulta_order_by():
    session = obtener_sesion()
    try:
        print("--- CONSULTA: ORDER BY (Listar Profesores ordenados alfabéticamente por apellido) ---")
        profesores = session.query(Profesor).order_by(Profesor.apellidos.asc()).all()
        for prof in profesores:
            print(f"Profesor: {prof.apellidos}, {prof.nombres} | Correo: {prof.correo} | Especialidad: {prof.especialidad}")
            print(f"  Carrera: {prof.carrera.nombre}")
            print("-" * 50)
    except Exception as e:
        print(f"Error en consulta_order_by: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    consulta_order_by()

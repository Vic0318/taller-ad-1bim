from sqlalchemy import or_
from configuracion import obtener_sesion
from crear_base_entidades import RecursoAcademico

def consulta_or():
    session = obtener_sesion()
    try:
        print("--- CONSULTA: OR (Filtrar Recursos Académicos de tipo 'Video' o 'Guia') ---")
        recursos = session.query(RecursoAcademico).filter(
            or_(
                RecursoAcademico.tipo == "Video",
                RecursoAcademico.tipo == "Guia"
            )
        ).all()
        for rec in recursos:
            print(f"Recurso ID: {rec.id} | Título: '{rec.titulo}' | Tipo: {rec.tipo} | Creador: {rec.profesor.nombres} {rec.profesor.apellidos}")
            print(f"  URL: {rec.url}")
            print("-" * 50)
    except Exception as e:
        print(f"Error en consulta_or: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    consulta_or()

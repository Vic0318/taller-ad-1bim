from configuracion import obtener_sesion
from crear_base_entidades import RecursoAcademico

def consulta_filter():
    session = obtener_sesion()
    try:
        print("--- CONSULTA: FILTER (Filtrar Recursos Académicos de tipo 'Libro') ---")
        recursos_libros = session.query(RecursoAcademico).filter_by(tipo="Libro").all()
        for rec in recursos_libros:
            print(f"Recurso ID: {rec.id} | Título: '{rec.titulo}' | Publicado: {rec.fecha_publicacion} | Creador: {rec.profesor.nombres} {rec.profesor.apellidos}")
            print(f"  URL: {rec.url}")
            print("-" * 50)
    except Exception as e:
        print(f"Error en consulta_filter: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    consulta_filter()

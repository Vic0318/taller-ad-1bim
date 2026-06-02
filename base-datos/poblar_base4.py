import os
import json
import datetime
from configuracion import obtener_sesion
from crear_base_entidades import RecursoAcademico, Profesor

# Resolver ruta absoluta al archivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "datos_universidad", "datos", "recursos_academicos.json")

def poblar_recursos():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    session = obtener_sesion()
    try:
        print(f"Cargando recursos académicos desde {JSON_PATH}...")
        for item in data:
            # Buscar al profesor concatenando nombres y apellidos
            nombre_completo_json = item["profesor"]
            profesor = session.query(Profesor).filter(
                (Profesor.nombres + " " + Profesor.apellidos) == nombre_completo_json
            ).first()
            
            if not profesor:
                print(f"Advertencia: No se encontró al profesor '{nombre_completo_json}' para el recurso '{item['titulo']}'")
                continue
                
            # Parsear fecha de publicación
            fecha_pub = datetime.datetime.strptime(item["fecha_publicacion"], "%Y-%m-%d").date()
            
            # Verificar si ya existe por ID
            existente = session.query(RecursoAcademico).filter_by(id=item["id"]).first()
            if not existente:
                nuevo_recurso = RecursoAcademico(
                    id=item["id"],
                    titulo=item["titulo"],
                    fecha_publicacion=fecha_pub,
                    tipo=item["tipo"],
                    url=item["url"],
                    profesor_id=profesor.id
                )
                session.add(nuevo_recurso)
                print(f"Agregando: {item['titulo']} (Tipo: {item['tipo']}, Profesor: {profesor.nombres} {profesor.apellidos})")
            else:
                print(f"Ya existe: {item['titulo']}")
        session.commit()
        print("Población de recursos académicos completada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al poblar recursos académicos: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    poblar_recursos()

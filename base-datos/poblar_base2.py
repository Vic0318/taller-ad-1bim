import os
import json
from configuracion import obtener_sesion
from crear_base_entidades import Carrera, Facultad

# Resolver ruta absoluta al archivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "datos_universidad", "datos", "carreras.json")

def poblar_carreras():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    session = obtener_sesion()
    try:
        print(f"Cargando carreras desde {JSON_PATH}...")
        for item in data:
            # Buscar la facultad por su nombre para obtener el id
            facultad = session.query(Facultad).filter_by(nombre=item["facultad"]).first()
            if not facultad:
                print(f"Advertencia: No se encontró la facultad '{item['facultad']}' para la carrera '{item['nombre']}'")
                continue
                
            # Verificar si ya existe por nombre o código
            existente = session.query(Carrera).filter_by(nombre=item["nombre"]).first()
            if not existente:
                nueva_carrera = Carrera(
                    id=item["id"],
                    nombre=item["nombre"],
                    codigo=item["codigo"],
                    facultad_id=facultad.id
                )
                session.add(nueva_carrera)
                print(f"Agregando: {item['nombre']} (Código: {item['codigo']}, Facultad: {facultad.nombre})")
            else:
                print(f"Ya existe: {item['nombre']}")
        session.commit()
        print("Población de carreras completada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al poblar carreras: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    poblar_carreras()

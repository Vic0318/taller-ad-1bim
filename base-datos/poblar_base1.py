import os
import json
from configuracion import obtener_sesion
from crear_base_entidades import Facultad

# Resolver ruta absoluta al archivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "datos_universidad", "datos", "facultades.json")

def poblar_facultades():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    session = obtener_sesion()
    try:
        print(f"Cargando facultades desde {JSON_PATH}...")
        for item in data:
            # Verificar si ya existe por nombre
            existente = session.query(Facultad).filter_by(nombre=item["nombre"]).first()
            if not existente:
                nueva_facultad = Facultad(
                    id=item["id"],
                    nombre=item["nombre"],
                    ubicacion=item["ubicacion"],
                    decano=item["decano"]
                )
                session.add(nueva_facultad)
                print(f"Agregando: {item['nombre']}")
            else:
                print(f"Ya existe: {item['nombre']}")
        session.commit()
        print("Población de facultades completada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al poblar facultades: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    poblar_facultades()

import os
import json
from configuracion import obtener_sesion
from crear_base_entidades import Profesor, Carrera

# Resolver ruta absoluta al archivo JSON
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "data", "datos_universidad", "datos", "profesores.json")

def poblar_profesores():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    session = obtener_sesion()
    try:
        print(f"Cargando profesores desde {JSON_PATH}...")
        for item in data:
            # Buscar la carrera por su nombre para obtener el id
            carrera = session.query(Carrera).filter_by(nombre=item["carrera"]).first()
            if not carrera:
                print(f"Advertencia: No se encontró la carrera '{item['carrera']}' para el profesor '{item['nombres']} {item['apellidos']}'")
                continue
                
            # Verificar si ya existe por correo
            existente = session.query(Profesor).filter_by(correo=item["correo"]).first()
            if not existente:
                nuevo_profesor = Profesor(
                    id=item["id"],
                    nombres=item["nombres"],
                    apellidos=item["apellidos"],
                    correo=item["correo"],
                    especialidad=item["especialidad"],
                    carrera_id=carrera.id
                )
                session.add(nuevo_profesor)
                print(f"Agregando: {item['nombres']} {item['apellidos']} (Especialidad: {item['especialidad']}, Carrera: {carrera.nombre})")
            else:
                print(f"Ya existe: {item['nombres']} {item['apellidos']}")
        session.commit()
        print("Población de profesores completada exitosamente.")
    except Exception as e:
        session.rollback()
        print(f"Error al poblar profesores: {e}")
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    poblar_profesores()

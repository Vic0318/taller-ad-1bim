from configuracion import obtener_sesion
from crear_base_entidades import Facultad

def consulta_all():
    session = obtener_sesion()
    try:
        print("--- CONSULTA: ALL (Listar todas las Facultades y sus Carreras) ---")
        facultades = session.query(Facultad).all()
        for fac in facultades:
            print(f"Facultad ID: {fac.id} | Nombre: {fac.nombre} | Decano: {fac.decano} | Ubicación: {fac.ubicacion}")
            if fac.carreras:
                print("  Carreras ofertadas:")
                for car in fac.carreras:
                    print(f"    - {car.nombre} (Código: {car.codigo})")
            else:
                print("  No tiene carreras registradas.")
            print("-" * 50)
    except Exception as e:
        print(f"Error en consulta_all: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    consulta_all()

import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from configuracion import engine, inicializar_base_datos

# Declaración de la clase base usando el estilo clásico sin anotaciones
Base = declarative_base()

class Facultad(Base):
    __tablename__ = "facultades"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), unique=True, nullable=False)
    ubicacion = Column(String(100), nullable=False)
    decano = Column(String(100), nullable=False)
    
    # Relación de uno a muchos con Carrera
    carreras = relationship(
        "Carrera", back_populates="facultad", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Facultad(id={self.id}, nombre='{self.nombre}', decano='{self.decano}')>"

class Carrera(Base):
    __tablename__ = "carreras"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(150), unique=True, nullable=False)
    codigo = Column(String(20), unique=True, nullable=False)
    facultad_id = Column(Integer, ForeignKey("facultades.id"), nullable=False)
    
    # Relaciones
    facultad = relationship("Facultad", back_populates="carreras")
    profesores = relationship(
        "Profesor", back_populates="carrera", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Carrera(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo}')>"

class Profesor(Base):
    __tablename__ = "profesores"
    
    id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    especialidad = Column(String(100), nullable=False)
    carrera_id = Column(Integer, ForeignKey("carreras.id"), nullable=False)
    
    # Relaciones
    carrera = relationship("Carrera", back_populates="profesores")
    recursos = relationship(
        "RecursoAcademico", back_populates="profesor", cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"<Profesor(id={self.id}, nombres='{self.nombres}', apellidos='{self.apellidos}')>"

class RecursoAcademico(Base):
    __tablename__ = "recursos_academicos"
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    fecha_publicacion = Column(Date, nullable=False)
    tipo = Column(String(50), nullable=False)
    url = Column(String(255), nullable=False)
    profesor_id = Column(Integer, ForeignKey("profesores.id"), nullable=False)
    
    # Relación
    profesor = relationship("Profesor", back_populates="recursos")
    
    def __repr__(self):
        return f"<RecursoAcademico(id={self.id}, titulo='{self.titulo}', tipo='{self.tipo}')>"

if __name__ == "__main__":
    print("Inicializando base de datos...")
    inicializar_base_datos()
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("Tablas creadas exitosamente.")

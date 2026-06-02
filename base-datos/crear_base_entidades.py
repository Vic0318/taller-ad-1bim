import datetime
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from configuracion import engine, inicializar_base_datos

class Base(DeclarativeBase):
    pass

class Facultad(Base):
    __tablename__ = "facultades"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    ubicacion: Mapped[str] = mapped_column(String(100), nullable=False)
    decano: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relación de uno a muchos con Carrera
    carreras: Mapped[list["Carrera"]] = relationship(
        back_populates="facultad", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Facultad(id={self.id}, nombre='{self.nombre}', decano='{self.decano}')>"

class Carrera(Base):
    __tablename__ = "carreras"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    facultad_id: Mapped[int] = mapped_column(ForeignKey("facultades.id"), nullable=False)
    
    # Relaciones
    facultad: Mapped["Facultad"] = relationship(back_populates="carreras")
    profesores: Mapped[list["Profesor"]] = relationship(
        back_populates="carrera", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Carrera(id={self.id}, nombre='{self.nombre}', codigo='{self.codigo}')>"

class Profesor(Base):
    __tablename__ = "profesores"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    especialidad: Mapped[str] = mapped_column(String(100), nullable=False)
    carrera_id: Mapped[int] = mapped_column(ForeignKey("carreras.id"), nullable=False)
    
    # Relaciones
    carrera: Mapped["Carrera"] = relationship(back_populates="profesores")
    recursos: Mapped[list["RecursoAcademico"]] = relationship(
        back_populates="profesor", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<Profesor(id={self.id}, nombres='{self.nombres}', apellidos='{self.apellidos}')>"

class RecursoAcademico(Base):
    __tablename__ = "recursos_academicos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_publicacion: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    profesor_id: Mapped[int] = mapped_column(ForeignKey("profesores.id"), nullable=False)
    
    # Relación
    profesor: Mapped["Profesor"] = relationship(back_populates="recursos")
    
    def __repr__(self) -> str:
        return f"<RecursoAcademico(id={self.id}, titulo='{self.titulo}', tipo='{self.tipo}')>"

if __name__ == "__main__":
    print("Inicializando base de datos...")
    inicializar_base_datos()
    print("Creando tablas en la base de datos...")
    Base.metadata.create_all(engine)
    print("Tablas creadas exitosamente.")

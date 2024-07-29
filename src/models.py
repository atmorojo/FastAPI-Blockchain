from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Float,
    String,
    DateTime
)
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")


class Juleha(Base):
    __tablename__ = "julehas"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    ms_sertifikat = Column(String, index=True)
    upload_sertifikat = Column(String)
    waktu_upload = Column(DateTime)
    # ternaks = relationship("Ternak", back_populates="juleha")


class Peternak(Base):
    __tablename__ = "peternaks"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    alamat = Column(String, index=True)
    status_usaha = Column(String, index=True)
    ternaks = relationship("Ternak", back_populates="peternak")


class Ternak(Base):
    __tablename__ = "ternaks"

    id = Column(Integer, primary_key=True)
    bobot = Column(Float, index=True)
    jenis = Column(String, index=True)
    kesehatan = Column(String, index=True)
    peternak_id = Column(Integer, ForeignKey("peternaks.id"))
    peternak = relationship("Peternak", back_populates="ternaks")
    # juleha_id = Column(Integer, ForeignKey("julehas.id"))
    # juleha = relationship("Juleha", back_populates="ternaks")

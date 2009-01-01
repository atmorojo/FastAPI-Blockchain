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
from sqlalchemy.sql import func

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
    nomor_sertifikat = Column(String, index=True)
    masa_sertifikat = Column(String, index=True)
    upload_sertifikat = Column(String)
    waktu_upload = Column(DateTime(timezone=True), server_default=func.now())
    ternaks = relationship("Ternak", back_populates="juleha")


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
    juleha_id = Column(Integer, ForeignKey("julehas.id"))
    juleha = relationship("Juleha", back_populates="ternaks")


class Rph(Base):
    __tablename__ = "rphs"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    alamat = Column(String, index=True)
    telepon = Column(String)
    status_sertifikasi = Column(String, index=True)
    file_sertifikasi = Column(String, index=True)
    waktu_upload = Column(DateTime(timezone=True), server_default=func.now())
    penyelias = relationship("Penyelia", back_populates="rph")


class Penyelia(Base):
    __tablename__ = "penyelias"

    id = Column(Integer, primary_key=True)
    nip = Column(String, index=True)
    name = Column(String, index=True)
    status = Column(String, index=True)
    tgl_berlaku = Column(String)
    file_sk = Column(String, index=True)
    rph_id = Column(Integer, ForeignKey("rphs.id"))
    rph = relationship("Rph", back_populates="penyelias")

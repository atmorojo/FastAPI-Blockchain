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
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    is_active = Column(Boolean, default=True)


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
    name = Column(String, index=True)
    bobot = Column(Float, index=True)
    jenis = Column(String, index=True)
    kesehatan = Column(String, index=True)
    waktu_sembelih = Column(String)
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


class Pasar(Base):
    __tablename__ = "pasars"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    alamat = Column(String, index=True)

    lapaks = relationship("Lapak", back_populates="pasar")


# Durung digawe mastere
class Lapak(Base):
    __tablename__ = "lapaks"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    no_lapak = Column(String)
    pasar_id = Column(Integer, ForeignKey("pasars.id"))
    pasar = relationship("Pasar", back_populates="lapaks")


class Transportasi(Base):
    __tablename__ = "transportasis"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    rph_id = Column(Integer, ForeignKey("rphs.id"))
    rph = relationship("Rph")


class Transaksi(Base):
    __tablename__ = "transaksis"

    id = Column(Integer, primary_key=True)
    jumlah = Column(Float)
    status = Column(String)
    validasi_1 = Column(Integer)
    validasi_2 = Column(Integer)
    transportasi_id = Column(Integer, ForeignKey("transportasis.id"))
    lapak_id = Column(Integer, ForeignKey("lapaks.id"))
    penyelia_id = Column(Integer, ForeignKey("penyelias.id"))
    juleha_id = Column(Integer, ForeignKey("julehas.id"))
    ternak_id = Column(Integer, ForeignKey("ternaks.id"))
    transportasi = relationship("Transportasi")
    lapak = relationship("Lapak")
    penyelia = relationship("Penyelia")
    juleha = relationship("Juleha")
    ternak = relationship("Ternak")


class Pengiriman(Base):
    __tablename__ = "pengirimans"

    id = Column(Integer, primary_key=True)
    waktu_kirim = Column(String)
    waktu_selesai = Column(String)
    status = Column(String)
    iot_id = Column(Integer, ForeignKey("iots.id"))
    transaksi_id = Column(Integer, ForeignKey("transaksis.id"))
    iot = relationship("IoT")
    transaksi = relationship("Transaksi")


class IoT(Base):
    __tablename__ = "iots"

    id = Column(Integer, primary_key=True)
    node = Column(String)
    rph_id = Column(Integer, ForeignKey("rphs.id"))
    rph = relationship("Rph")

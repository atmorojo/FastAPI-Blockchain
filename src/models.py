from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(Integer, nullable=True)
    tgl_update = Column(Integer, nullable=True)
    role = relationship(
        "Role", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Role(Base):
    __tablename__ = "role"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(Integer)  # 0 super, 1 admin, 2 penyelia, 3 juleha, 4 lapak
    acting_as = Column(Integer)
    user = relationship("User", back_populates="role")


class Juleha(Base):
    __tablename__ = "juleha"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    nomor_sertifikat = Column(String, index=True)
    masa_sertifikat = Column(String, index=True)
    upload_sertifikat = Column(String)
    waktu_upload = Column(DateTime(timezone=True))
    ternak = relationship("Ternak", back_populates="juleha")


class Peternak(Base):
    __tablename__ = "peternak"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    alamat = Column(String, index=True)
    status_usaha = Column(String, index=True)  # mandiri/badan usaha
    ternak = relationship("Ternak", back_populates="peternak")


class Ternak(Base):
    __tablename__ = "ternak"

    id = Column(Integer, primary_key=True)
    peternak_id = Column(Integer, ForeignKey("peternak.id"))
    juleha_id = Column(Integer, ForeignKey("juleha.id"))
    penyelia_id = Column(Integer, ForeignKey("penyelia.id"))
    img = Column(String)
    bobot = Column(Float, index=True)
    jenis = Column(String, index=True)  # Kambing, domba, kerbau, sapi
    waktu_daftar = Column(String)
    no_antri = Column(String)
    kesehatan = Column(String, index=True)  # sehat / layak
    waktu_sembelih = Column(String)
    karkas = Column(Float, index=True)
    validasi_1 = Column(Integer)
    validasi_2 = Column(Integer)
    peternak = relationship("Peternak", back_populates="ternak")
    juleha = relationship("Juleha", back_populates="ternak")
    penyelia = relationship("Penyelia")


class Rph(Base):
    __tablename__ = "rph"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    alamat = Column(String, index=True)
    telepon = Column(String)
    status_sertifikasi = Column(String, index=True)  # sudah/belum
    file_sertifikasi = Column(String, index=True)
    waktu_upload = Column(DateTime(timezone=True))
    penyelia = relationship("Penyelia", back_populates="rph")


class Penyelia(Base):
    __tablename__ = "penyelia"

    id = Column(Integer, primary_key=True)
    rph_id = Column(Integer, ForeignKey("rph.id"))
    name = Column(String, index=True)
    nip = Column(String, index=True)
    status = Column(String, index=True)  # aktif/tidak aktif tergantung tgl_berlaku
    tgl_berlaku = Column(String)
    file_sk = Column(String, index=True)
    rph = relationship("Rph", back_populates="penyelia")


class Pasar(Base):
    __tablename__ = "pasar"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    alamat = Column(String, index=True)

    lapak = relationship("Lapak", back_populates="pasar")


class Lapak(Base):
    __tablename__ = "lapak"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    no_lapak = Column(String)
    pasar_id = Column(Integer, ForeignKey("pasar.id"))
    telp = Column(String)
    pasar = relationship("Pasar", back_populates="lapak")


class Transaksi(Base):
    __tablename__ = "transaksi"

    id = Column(Integer, primary_key=True)
    iot_id = Column(Integer, ForeignKey("iot.id"))
    lapak_id = Column(Integer, ForeignKey("lapak.id"))
    ternak_id = Column(Integer, ForeignKey("ternak.id"))
    jumlah = Column(Float)
    waktu_kirim = Column(String)
    waktu_selesai_kirim = Column(String)
    status_kirim = Column(String)
    iot = relationship("IoT")
    lapak = relationship("Lapak")
    ternak = relationship("Ternak")


class IoT(Base):
    __tablename__ = "iot"

    id = Column(Integer, primary_key=True)
    node = Column(String)


class Konsumen(Base):
    __tablename__ = "konsumen"

    id = Column(Integer, primary_key=True)

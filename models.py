# models.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

# Tabel asosiasi many-to-many antara buku dan penulis
buku_penulis = Table(
    'buku_penulis', Base.metadata,
    Column('id_buku', Integer, ForeignKey('buku.id', ondelete='CASCADE'), primary_key=True),
    Column('id_penulis', Integer, ForeignKey('penulis.id', ondelete='CASCADE'), primary_key=True)
)

class Kategori(Base):
    __tablename__ = 'kategori'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(100), unique=True, nullable=False)

    # Relasi ke buku
    buku = relationship('Buku', back_populates='kategori', lazy='selectin')

class Penulis(Base):
    __tablename__ = 'penulis'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(150), nullable=False)
    asal = Column(String(100), nullable=True)

    # Relasi many-to-many ke buku melalui tabel buku_penulis
    buku = relationship('Buku', secondary=buku_penulis, back_populates='penulis', lazy='selectin')

class Penerbit(Base):
    __tablename__ = 'penerbit'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(150), nullable=False)
    kota = Column(String(100), nullable=True)

    buku = relationship('Buku', back_populates='penerbit', lazy='selectin')

class Buku(Base):
    __tablename__ = 'buku'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    judul = Column(String(200), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    tahun_terbit = Column(Integer, nullable=True)
    stok = Column(Integer, default=1)

    id_kategori = Column(Integer, ForeignKey('kategori.id'))
    id_penerbit = Column(Integer, ForeignKey('penerbit.id'))

    kategori = relationship('Kategori', back_populates='buku')
    penerbit = relationship('Penerbit', back_populates='buku')
    penulis = relationship('Penulis', secondary=buku_penulis, back_populates='buku', lazy='selectin')

    peminjaman = relationship('Peminjaman', back_populates='buku', lazy='selectin')

class Siswa(Base):
    __tablename__ = 'siswa'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nis = Column(String(20), unique=True, nullable=False)
    nama = Column(String(150), nullable=False)
    kelas = Column(String(20), nullable=False)
    nomor_telepon = Column(String(15), nullable=True)

    peminjaman = relationship('Peminjaman', back_populates='siswa', lazy='selectin')

class StatusPinjam(str, enum.Enum):
    dipinjam = 'dipinjam'
    dikembalikan = 'dikembalikan'

class Peminjaman(Base):
    __tablename__ = 'peminjaman'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_siswa = Column(Integer, ForeignKey('siswa.id'))
    id_buku = Column(Integer, ForeignKey('buku.id'))
    tanggal_pinjam = Column(Date, nullable=False)
    tanggal_jatuh_tempo = Column(Date, nullable=False)
    tanggal_kembali = Column(Date, nullable=True)
    
    status = Column(Enum(StatusPinjam), default=StatusPinjam.dipinjam)

    siswa = relationship('Siswa', back_populates='peminjaman')
    buku = relationship('Buku', back_populates='peminjaman')

    denda = relationship('Denda', back_populates='peminjaman', uselist=False)

class Denda(Base):
    __tablename__ = 'denda'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_peminjaman = Column(Integer, ForeignKey('peminjaman.id'))
    jumlah_denda = Column(Integer, nullable=True, default=0)
    status_bayar = Column(String(20), default='belum_bayar')
    tanggal_dibuat = Column(Date, nullable=False)

    peminjaman = relationship('Peminjaman', back_populates='denda')
# schemas.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime

# ---------- Kategori ----------
class KategoriBase(BaseModel):
    nama: str

class KategoriCreate(KategoriBase):
    pass

class KategoriOut(KategoriBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Penulis ----------
class PenulisBase(BaseModel):
    nama: str
    asal: Optional[str] = None

class PenulisCreate(PenulisBase):
    pass

class PenulisOut(PenulisBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Penerbit ----------
class PenerbitBase(BaseModel):
    nama: str
    kota: Optional[str] = None

class PenerbitCreate(PenerbitBase):
    pass

class PenerbitOut(PenerbitBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Buku ----------
class BukuBase(BaseModel):
    judul: str
    isbn: str
    tahun_terbit: Optional[int] = None
    stok: int = 1
    id_kategori: int
    id_penerbit: int
    id_penulis: List[int] = []

class BukuCreate(BukuBase):
    pass

class BukuOut(BaseModel):
    id: int
    judul: str
    isbn: str
    tahun_terbit: Optional[int]
    stok: int
    kategori: Optional[KategoriOut]
    penerbit: Optional[PenerbitOut]
    penulis: List[PenulisOut] = []
    class Config:
        from_attributes = True

# ---------- Siswa ----------
class SiswaBase(BaseModel):
    nis: str
    nama: str
    kelas: str
    nomor_telepon: Optional[str] = None

class SiswaCreate(SiswaBase):
    pass

class SiswaOut(SiswaBase):
    id: int
    class Config:
        from_attributes = True

# ---------- Peminjaman ----------
class PeminjamanCreate(BaseModel):
    id_siswa: int
    id_buku: int
    tanggal_pinjam: date

class PeminjamanOut(BaseModel):
    id: int
    id_siswa: int
    id_buku: int
    tanggal_pinjam: date
    tanggal_jatuh_tempo: date
    tanggal_kembali: Optional[date]
    denda: Optional[int]
    status: str
    siswa: Optional[SiswaOut]
    buku: Optional[BukuOut]

    class Config:
        from_attributes = True
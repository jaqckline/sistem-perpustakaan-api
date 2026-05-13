# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas
from datetime import date, timedelta
from typing import List, Optional

# ---------- Kategori ----------
def get_kategori(db: Session, kategori_id: int):
    return db.query(models.Kategori).filter(models.Kategori.id == kategori_id).first()

def get_all_kategori(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kategori).offset(skip).limit(limit).all()

def create_kategori(db: Session, kategori: schemas.KategoriCreate):
    db_kategori = models.Kategori(nama=kategori.nama)
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

def update_kategori(db: Session, kategori_id: int, nama: str):
    kat = get_kategori(db, kategori_id)
    if kat:
        kat.nama = nama
        db.commit()
        db.refresh(kat)
    return kat

def delete_kategori(db: Session, kategori_id: int):
    kat = get_kategori(db, kategori_id)
    if kat:
        # Cek apakah ada buku terkait
        if db.query(models.Buku).filter(models.Buku.id_kategori == kategori_id).count() > 0:
            return False
        db.delete(kat)
        db.commit()
        return True
    return False

# ---------- Penulis ----------
def get_penulis(db: Session, penulis_id: int):
    return db.query(models.Penulis).filter(models.Penulis.id == penulis_id).first()

def get_all_penulis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Penulis).offset(skip).limit(limit).all()

def create_penulis(db: Session, penulis: schemas.PenulisCreate):
    db_penulis = models.Penulis(**penulis.dict())
    db.add(db_penulis)
    db.commit()
    db.refresh(db_penulis)
    return db_penulis

def update_penulis(db: Session, penulis_id: int, penulis: schemas.PenulisCreate):
    p = get_penulis(db, penulis_id)
    if p:
        p.nama = penulis.nama
        p.asal = penulis.asal
        db.commit()
        db.refresh(p)
    return p

def delete_penulis(db: Session, penulis_id: int):
    p = get_penulis(db, penulis_id)
    if p:
        db.delete(p)
        db.commit()
        return True
    return False

# ---------- Penerbit ----------
def get_penerbit(db: Session, penerbit_id: int):
    return db.query(models.Penerbit).filter(models.Penerbit.id == penerbit_id).first()

def get_all_penerbit(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Penerbit).offset(skip).limit(limit).all()

def create_penerbit(db: Session, penerbit: schemas.PenerbitCreate):
    db_penerbit = models.Penerbit(**penerbit.dict())
    db.add(db_penerbit)
    db.commit()
    db.refresh(db_penerbit)
    return db_penerbit

def update_penerbit(db: Session, penerbit_id: int, penerbit: schemas.PenerbitCreate):
    p = get_penerbit(db, penerbit_id)
    if p:
        p.nama = penerbit.nama
        p.kota = penerbit.kota
        db.commit()
        db.refresh(p)
    return p

def delete_penerbit(db: Session, penerbit_id: int):
    p = get_penerbit(db, penerbit_id)
    if p:
        db.delete(p)
        db.commit()
        return True
    return False

# ---------- Buku ----------
def get_buku(db: Session, buku_id: int):
    return db.query(models.Buku).filter(models.Buku.id == buku_id).first()

def get_all_buku(db: Session, skip: int = 0, limit: int = 100,
                 kategori_id: Optional[int] = None, penulis_id: Optional[int] = None,
                 search: Optional[str] = None):
    query = db.query(models.Buku)
    if kategori_id:
        query = query.filter(models.Buku.id_kategori == kategori_id)
    if penulis_id:
        query = query.filter(models.Buku.penulis.any(models.Penulis.id == penulis_id))
    if search:
        query = query.filter(models.Buku.judul.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def create_buku(db: Session, buku: schemas.BukuCreate):
    db_buku = models.Buku(
        judul=buku.judul,
        isbn=buku.isbn,
        tahun_terbit=buku.tahun_terbit,
        stok=buku.stok,
        id_kategori=buku.id_kategori,
        id_penerbit=buku.id_penerbit
    )
    # Mengaitkan penulis
    if buku.id_penulis:
        penulis_list = db.query(models.Penulis).filter(models.Penulis.id.in_(buku.id_penulis)).all()
        db_buku.penulis = penulis_list
    db.add(db_buku)
    db.commit()
    db.refresh(db_buku)
    return db_buku

def update_buku(db: Session, buku_id: int, buku: schemas.BukuCreate):
    db_buku = get_buku(db, buku_id)
    if not db_buku:
        return None
    db_buku.judul = buku.judul
    db_buku.isbn = buku.isbn
    db_buku.tahun_terbit = buku.tahun_terbit
    db_buku.stok = buku.stok
    db_buku.id_kategori = buku.id_kategori
    db_buku.id_penerbit = buku.id_penerbit
    # Update penulis
    penulis_list = db.query(models.Penulis).filter(models.Penulis.id.in_(buku.id_penulis)).all()
    db_buku.penulis = penulis_list
    db.commit()
    db.refresh(db_buku)
    return db_buku

def delete_buku(db: Session, buku_id: int):
    db_buku = get_buku(db, buku_id)
    if db_buku:
        # Cek apakah buku masih dipinjam (status dipinjam)
        aktif = db.query(models.Peminjaman).filter(
            models.Peminjaman.id_buku == buku_id,
            models.Peminjaman.status == models.StatusPinjam.dipinjam
        ).count()
        if aktif > 0:
            return False
        db.delete(db_buku)
        db.commit()
        return True
    return False

# ---------- Siswa ----------
def get_siswa(db: Session, siswa_id: int):
    return db.query(models.Siswa).filter(models.Siswa.id == siswa_id).first()

def get_all_siswa(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Siswa).offset(skip).limit(limit).all()

def create_siswa(db: Session, siswa: schemas.SiswaCreate):
    db_siswa = models.Siswa(**siswa.dict())
    db.add(db_siswa)
    db.commit()
    db.refresh(db_siswa)
    return db_siswa

def update_siswa(db: Session, siswa_id: int, siswa: schemas.SiswaCreate):
    s = get_siswa(db, siswa_id)
    if s:
        s.nis = siswa.nis
        s.nama = siswa.nama
        s.kelas = siswa.kelas
        s.nomor_telepon = siswa.nomor_telepon
        db.commit()
        db.refresh(s)
    return s

def delete_siswa(db: Session, siswa_id: int):
    s = get_siswa(db, siswa_id)
    if s:
        db.delete(s)
        db.commit()
        return True
    return False

# ---------- Peminjaman ----------
TARIF_DENDA_PER_HARI = 1000  # Rupiah

def create_peminjaman(db: Session, peminjaman: schemas.PeminjamanCreate):
    # Cek stok buku
    buku = db.query(models.Buku).filter(models.Buku.id == peminjaman.id_buku).first()
    if not buku or buku.stok < 1:
        return None
    # Hitung tanggal jatuh tempo 7 hari setelah pinjam
    tgl_jatuh_tempo = peminjaman.tanggal_pinjam + timedelta(days=7)
    db_peminjaman = models.Peminjaman(
        id_siswa=peminjaman.id_siswa,
        id_buku=peminjaman.id_buku,
        tanggal_pinjam=peminjaman.tanggal_pinjam,
        tanggal_jatuh_tempo=tgl_jatuh_tempo,
        status=models.StatusPinjam.dipinjam
    )
    # Kurangi stok
    buku.stok -= 1
    db.add(db_peminjaman)
    db.commit()
    db.refresh(db_peminjaman)
    return db_peminjaman

def get_peminjaman(db: Session, peminjaman_id: int):
    return db.query(models.Peminjaman).filter(models.Peminjaman.id == peminjaman_id).first()

def get_all_peminjaman(db: Session, skip: int = 0, limit: int = 100,
                       status: Optional[str] = None, id_siswa: Optional[int] = None):
    query = db.query(models.Peminjaman)
    if status:
        query = query.filter(models.Peminjaman.status == status)
    if id_siswa:
        query = query.filter(models.Peminjaman.id_siswa == id_siswa)
    return query.offset(skip).limit(limit).all()

def kembalikan_buku(db: Session, peminjaman_id: int):
    peminjaman = get_peminjaman(db, peminjaman_id)
    if not peminjaman or peminjaman.status != models.StatusPinjam.dipinjam:
        return None
    # Set tanggal kembali hari ini
    today = date.today()
    peminjaman.tanggal_kembali = today
    # Hitung denda jika terlambat
    if today > peminjaman.tanggal_jatuh_tempo:
        selisih = (today - peminjaman.tanggal_jatuh_tempo).days
        denda_total = selisih * TARIF_DENDA_PER_HARI

        db_denda = models.Denda(
            id_peminjaman=peminjaman.id,
            jumlah_denda=denda_total,
            status_bayar='belum_bayar',
            tanggal_dibuat=today
        )
        db.add(db_denda)

    peminjaman.status = models.StatusPinjam.dikembalikan
    # Tambah stok buku
    buku = db.query(models.Buku).filter(models.Buku.id == peminjaman.id_buku).first()
    if buku:
        buku.stok += 1
    db.commit()

    db.refresh(peminjaman)
    return peminjaman

def delete_peminjaman(db: Session, peminjaman_id: int):
    peminjaman = get_peminjaman(db, peminjaman_id)
    if not peminjaman:
        return False
    # Jika status masih dipinjam, stok buku dikembalikan
    if peminjaman.status == models.StatusPinjam.dipinjam:
        buku = db.query(models.Buku).filter(
            models.Buku.id == peminjaman.id_buku
        ).first()

        if buku:
            buku.stok += 1
    db.delete(peminjaman)
    db.commit()
    return True
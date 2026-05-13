# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import models, schemas, crud
from database import engine, get_db

# Membuat semua tabel jika belum ada (harus dijalankan sekali)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Perpustakaan Sekolah", version="1.0.0")

# ---------- KATEGORI ---------- 
@app.get("/api/v1/kategori/", response_model=List[schemas.KategoriOut])
def baca_kategori(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    kategori = crud.get_all_kategori(db, skip=skip, limit=limit)
    return kategori

@app.post("/api/v1/kategori/", response_model=schemas.KategoriOut, status_code=201)
def tambah_kategori(kat: schemas.KategoriCreate, db: Session = Depends(get_db)):
    return crud.create_kategori(db, kat)

@app.get("/api/v1/kategori/{kategori_id}", response_model=schemas.KategoriOut)
def detail_kategori(kategori_id: int, db: Session = Depends(get_db)):
    kat = crud.get_kategori(db, kategori_id)
    if not kat:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    return kat

@app.put("/api/v1/kategori/{kategori_id}", response_model=schemas.KategoriOut)
def ubah_kategori(kategori_id: int, nama_baru: schemas.KategoriCreate, db: Session = Depends(get_db)):
    kat = crud.update_kategori(db, kategori_id, nama_baru.nama)
    if not kat:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
    return kat

@app.delete("/api/v1/kategori/{kategori_id}")
def hapus_kategori(kategori_id: int, db: Session = Depends(get_db)):
    berhasil = crud.delete_kategori(db, kategori_id)
    if not berhasil:
        raise HTTPException(status_code=400, detail="Kategori tidak dapat dihapus (mungkin masih ada buku terkait)")
    return {"message": "Kategori berhasil dihapus"}

# ---------- PENULIS ----------
@app.get("/api/v1/penulis/", response_model=List[schemas.PenulisOut])
def baca_penulis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_penulis(db, skip, limit)

@app.post("/api/v1/penulis/", response_model=schemas.PenulisOut, status_code=201)
def tambah_penulis(penulis: schemas.PenulisCreate, db: Session = Depends(get_db)):
    return crud.create_penulis(db, penulis)

@app.get("/api/v1/penulis/{penulis_id}", response_model=schemas.PenulisOut)
def detail_penulis(penulis_id: int, db: Session = Depends(get_db)):
    p = crud.get_penulis(db, penulis_id)
    if not p:
        raise HTTPException(status_code=404, detail="Penulis tidak ditemukan")
    return p

@app.put("/api/v1/penulis/{penulis_id}", response_model=schemas.PenulisOut)
def ubah_penulis(penulis_id: int, penulis: schemas.PenulisCreate, db: Session = Depends(get_db)):
    p = crud.update_penulis(db, penulis_id, penulis)
    if not p:
        raise HTTPException(status_code=404, detail="Penulis tidak ditemukan")
    return p

@app.delete("/api/v1/penulis/{penulis_id}")
def hapus_penulis(penulis_id: int, db: Session = Depends(get_db)):
    if not crud.delete_penulis(db, penulis_id):
        raise HTTPException(status_code=404, detail="Penulis tidak ditemukan")
    return {"message": "Penulis berhasil dihapus"}

# ---------- PENERBIT ----------
@app.get("/api/v1/penerbit/", response_model=List[schemas.PenerbitOut])
def baca_penerbit(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_penerbit(db, skip, limit)

@app.post("/api/v1/penerbit/", response_model=schemas.PenerbitOut, status_code=201)
def tambah_penerbit(penerbit: schemas.PenerbitCreate, db: Session = Depends(get_db)):
    return crud.create_penerbit(db, penerbit)

@app.get("/api/v1/penerbit/{penerbit_id}", response_model=schemas.PenerbitOut)
def detail_penerbit(penerbit_id: int, db: Session = Depends(get_db)):
    p = crud.get_penerbit(db, penerbit_id)
    if not p:
        raise HTTPException(status_code=404, detail="Penerbit tidak ditemukan")
    return p

@app.put("/api/v1/penerbit/{penerbit_id}", response_model=schemas.PenerbitOut)
def ubah_penerbit(penerbit_id: int, penerbit: schemas.PenerbitCreate, db: Session = Depends(get_db)):
    p = crud.update_penerbit(db, penerbit_id, penerbit)
    if not p:
        raise HTTPException(status_code=404, detail="Penerbit tidak ditemukan")
    return p

@app.delete("/api/v1/penerbit/{penerbit_id}")
def hapus_penerbit(penerbit_id: int, db: Session = Depends(get_db)):
    if not crud.delete_penerbit(db, penerbit_id):
        raise HTTPException(status_code=404, detail="Penerbit tidak ditemukan")
    return {"message": "Penerbit berhasil dihapus"}

# ---------- BUKU ----------
@app.get("/api/v1/buku/", response_model=List[schemas.BukuOut])
def baca_buku(
    skip: int = 0,
    limit: int = 100,
    kategori_id: Optional[int] = None,
    penulis_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_all_buku(db, skip, limit, kategori_id, penulis_id, search)

@app.post("/api/v1/buku/", response_model=schemas.BukuOut, status_code=201)
def tambah_buku(buku: schemas.BukuCreate, db: Session = Depends(get_db)):
    return crud.create_buku(db, buku)

@app.get("/api/v1/buku/{buku_id}", response_model=schemas.BukuOut)
def detail_buku(buku_id: int, db: Session = Depends(get_db)):
    b = crud.get_buku(db, buku_id)
    if not b:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    return b

@app.put("/api/v1/buku/{buku_id}", response_model=schemas.BukuOut)
def ubah_buku(buku_id: int, buku: schemas.BukuCreate, db: Session = Depends(get_db)):
    b = crud.update_buku(db, buku_id, buku)
    if not b:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    return b

@app.delete("/api/v1/buku/{buku_id}")
def hapus_buku(buku_id: int, db: Session = Depends(get_db)):
    if not crud.delete_buku(db, buku_id):
        raise HTTPException(status_code=400, detail="Buku tidak dapat dihapus (mungkin masih dipinjam)")
    return {"message": "Buku berhasil dihapus"}

# ---------- SISWA ----------
@app.get("/api/v1/siswa/", response_model=List[schemas.SiswaOut])
def baca_siswa(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_siswa(db, skip, limit)

@app.post("/api/v1/siswa/", response_model=schemas.SiswaOut, status_code=201)
def tambah_siswa(siswa: schemas.SiswaCreate, db: Session = Depends(get_db)):
    return crud.create_siswa(db, siswa)

@app.get("/api/v1/siswa/{siswa_id}", response_model=schemas.SiswaOut)
def detail_siswa(siswa_id: int, db: Session = Depends(get_db)):
    s = crud.get_siswa(db, siswa_id)
    if not s:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    return s

@app.put("/api/v1/siswa/{siswa_id}", response_model=schemas.SiswaOut)
def ubah_siswa(siswa_id: int, siswa: schemas.SiswaCreate, db: Session = Depends(get_db)):
    s = crud.update_siswa(db, siswa_id, siswa)
    if not s:
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    return s

@app.delete("/api/v1/siswa/{siswa_id}")
def hapus_siswa(siswa_id: int, db: Session = Depends(get_db)):
    if not crud.delete_siswa(db, siswa_id):
        raise HTTPException(status_code=404, detail="Siswa tidak ditemukan")
    return {"message": "Siswa berhasil dihapus"}

# ---------- PEMINJAMAN ----------
@app.post("/api/v1/peminjaman/", response_model=schemas.PeminjamanOut, status_code=201)
def pinjam_buku(peminjaman: schemas.PeminjamanCreate, db: Session = Depends(get_db)):
    result = crud.create_peminjaman(db, peminjaman)
    if result is None:
        raise HTTPException(status_code=400, detail="Stok buku tidak mencukupi atau buku tidak ditemukan")
    return result

@app.get("/api/v1/peminjaman/", response_model=List[schemas.PeminjamanOut])
def daftar_peminjaman(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    id_siswa: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_all_peminjaman(db, skip, limit, status, id_siswa)

@app.get("/api/v1/peminjaman/{peminjaman_id}", response_model=schemas.PeminjamanOut)
def detail_peminjaman(peminjaman_id: int, db: Session = Depends(get_db)):
    p = crud.get_peminjaman(db, peminjaman_id)
    if not p:
        raise HTTPException(status_code=404, detail="Data peminjaman tidak ditemukan")
    return p

@app.put("/api/v1/peminjaman/{peminjaman_id}/kembalikan", response_model=schemas.PeminjamanOut)
def pengembalian_buku(peminjaman_id: int, db: Session = Depends(get_db)):
    p = crud.kembalikan_buku(db, peminjaman_id)
    if not p:
        raise HTTPException(status_code=400, detail="Peminjaman tidak valid atau sudah dikembalikan")
    return p

@app.delete("/api/v1/peminjaman/{peminjaman_id}")
def hapus_peminjaman(peminjaman_id: int, db: Session = Depends(get_db)):
    berhasil = crud.delete_peminjaman(db, peminjaman_id)
    if not berhasil:
        raise HTTPException(
            status_code=404,
            detail="Data peminjaman tidak ditemukan"
        )
    return {"message": "Data peminjaman berhasil dihapus"}

# Untuk menjalankan: uvicorn main:app --reload
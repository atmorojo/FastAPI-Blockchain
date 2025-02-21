from fastapi import APIRouter, HTTPException, UploadFile, Form, File, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import aiofiles

from src import models, security
from controllers.crud import Crud
from repositories.penyelia import Penyelia_Repo
from src.database import engine, get_db
from templates import pages, penyelia

models.Base.metadata.create_all(bind=engine)

routes = APIRouter(prefix="/penyelia", dependencies=[Depends(security.auth_rph)])


penyelia_db = Crud(models.Penyelia, get_db())


@routes.get("/new", response_class=HTMLResponse)
def new_penyelia(user=Depends(security.get_current_user), db=Depends(get_db)):
    """
    TODO:
    """
    rph = Crud(models.Rph, db).get()
    return str(
        pages.detail_page(
            "Penyelia",
            penyelia.penyelia_form(
                penyelia=None, rph=rph, admin=user.role.acting_as, lock=False
            ),
        )
    )


@routes.post("/")
async def create_penyelia(
    nip: str = Form(...),
    name: str = Form(...),
    status: str = Form(...),
    tgl_berlaku: str = Form(...),
    file_sk: UploadFile = File(...),
    user=Depends(security.get_current_user),
):
    penyelia = models.Penyelia(
        nip=nip,
        name=name,
        status=status,
        tgl_berlaku=tgl_berlaku,
        rph_id=user.role.acting_as,
    )
    penyelia = penyelia_db.create(penyelia)

    if file_sk.filename != "":
        out_file_path = "./files/sk_penyelia/" + str(penyelia.id)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await file_sk.read(1024):
                await out_file.write(content)

    penyelia.file_sk = penyelia.id
    penyelia_db.update(penyelia)

    return RedirectResponse("/penyelia/", status_code=302)


# Read


@routes.get("/", response_class=HTMLResponse)
def read_penyelias(
    skip: int = 0,
    limit: int = 100,
    user=Depends(security.get_current_user),
    db=Depends(get_db),
):
    # penyelias = penyelia_db.get(skip=skip, limit=limit)
    print(user.role.acting_as)
    filtered = Penyelia_Repo(db).get_rph_filtered(user.role.acting_as)
    penyelias = [penyelia for penyelia, _, _ in filtered]
    return str(pages.table_page("Penyelia", penyelia.penyelias_table(penyelias)))


@routes.get("/{penyelia_id}", response_class=HTMLResponse)
def read_penyelia(penyelia_id: int):
    dt_penyelia = penyelia_db.get_by_id(penyelia_id)
    if dt_penyelia is None:
        raise HTTPException(status_code=404, detail="User not found")
    return str(
        pages.detail_page("Penyelia", penyelia.penyelia_form(dt_penyelia, None, True))
    )


# Update


@routes.get("/edit/{penyelia_id}", response_class=HTMLResponse)
def edit_penyelia(req: Request, penyelia_id: int, db=Depends(get_db)):
    """
    TODO:
    * Auto pilih RPH berdasarkan admin
    """
    dt_penyelia = penyelia_db.get_by_id(penyelia_id)
    list_rph = Crud(models.Rph, db).get()
    lock = False

    if dt_penyelia is None:
        raise HTTPException(status_code=404, detail="User not found")

    form = penyelia.penyelia_form(dt_penyelia, list_rph, lock)

    if req.headers.get("HX-Request"):
        return str(form)
    else:
        return str(pages.detail_page("Penyelia", form))


@routes.put("/{penyelia_id}", response_class=HTMLResponse)
async def update_penyelia(
    penyelia_id: int,
    nip: str = Form(...),
    name: str = Form(...),
    status: str = Form(...),
    tgl_berlaku: str = Form(...),
    rph_id: int = Form(...),
    file_sk: UploadFile = File(None),  # Remember to give that None
    db=Depends(get_db),
):
    dt_penyelia = penyelia_db.get_by_id(penyelia_id)
    dt_penyelia.nip = nip
    dt_penyelia.name = name
    dt_penyelia.status = status
    dt_penyelia.tgl_berlaku = tgl_berlaku
    dt_penyelia.rph_id = rph_id

    if file_sk is not None:
        dt_penyelia.file_sk = penyelia_id
        out_file_path = "./files/sk_penyelia/" + str(penyelia_id)
        async with aiofiles.open(out_file_path, "wb") as out_file:
            while content := await file_sk.read(1024):
                await out_file.write(content)

    dt_penyelia = penyelia_db.update(dt_penyelia)
    list_rph = Crud(models.Rph, db).get()

    return str(penyelia.penyelia_form(dt_penyelia, list_rph, True))


# Delete


@routes.delete("/{penyelia_id}", response_class=HTMLResponse)
def remove_penyelia(penyelia_id: int):
    dt_penyelia = penyelia_db.get_by_id(penyelia_id)
    if dt_penyelia is None:
        raise HTTPException(status_code=404, detail="User not found")
    penyelias = penyelia_db.remove(dt_penyelia)
    return str(penyelia.penyelias_table(penyelias))

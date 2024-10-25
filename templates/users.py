import src.security as security
from templates.components import (
    table_builder,
    edit_btn,
    inlabel,
    combo_gen,
    update_btn,
    submit_btn,
    secure_action_buttons,
    dropdown_gen,
)

from htpy import (
    dialog, article, footer, button, small, header,
    h4,
    blockquote,
    render_node,
    form,
    div,
    Element,
    tr,
    td,
    a,
)

role_list = ["Super Admin", "Admin RPH", "Penyelia", "Juleha", "Lapak"]


def user_form(user=None, role=None, actors=None, lock: bool = False) -> Element:
    if lock:
        form_btn = edit_btn("/users/", user.username)
        role = inlabel("Role", "text", "role",
                       (role_list[user.role.role] if user else ""),
                       lock)
        actor = inlabel("Acting As", "text", "acting_as",
                        (name_fetcher(actors, user) if user else ""),
                        lock)
    else:
        role = dropdown_gen(
            "Role", "role", ["0", "1", "2", "3", "4"],
            (user.role.role if user else None),
            "Pilih role", role_list,
            hx={
                "hx-target": "next <label/>",
                "hx-get": "/users/acting_as",
                "hx-swap": "outerHTML"
            }
        )
        actor = inlabel("Acting As", "text", "acting_as", "", True)
        form_btn = (update_btn(
            "/users/", user.username
        ) if user else submit_btn)

    return form(
        "#form",
        action="/users",
        method="post",
        enctype="multipart/form-data"
    )[
        (None if user else inlabel("Username", "text", "username", "", lock)),
        inlabel("E-mail", "email", "email",
                (user.email if user else ""),
                lock),
        (a(role="button",
            hx_get=f"/users/{user.username}/pass",
            hx_target="#pass_dialog"
           )["Ubah Password"] if user else None),
        div("#pass_dialog"),
        (None if user else inlabel("Password", "password", "password", "", lock)),
        inlabel("Phone", "text", "phone",
                (user.phone if user else ""),
                lock),
        role,
        actor,
        form_btn
    ]


def users_table(actors, users) -> Element:
    col_headers = ["Username", "E-Mail", "Role", "Acting As", "Actions"]
    rows = (tr[
        td[user.username],
        td[user.email],
        td[role_list[user.role.role]],
        td[name_fetcher(actors, user)],
        td[secure_action_buttons("users", user.username, user.username)],
    ] for user in users)

    return table_builder(
        col_headers,
        rows
        )


def name_fetcher(big_list, user):
    name = "No name found"
    match security.get_role(user):
        case 0:
            return "Super Admin"
        case 1:
            persons = big_list["rph"]
        case 2:
            persons = big_list["penyelia"]
        case 3:
            persons = big_list["juleha"]
        case 4:
            persons = big_list["lapak"]

    for person in persons:
        print(person.id, user.role.acting_as)
        if person.id == user.role.acting_as:
            name = person.name

    return name


def super_admin():
    return render_node(inlabel("Acting As", "text", "acting_as", "0", False, ro=True))


def actors_dropdown(actors) -> Element:
    return combo_gen("Acting as", "acting_as", actors, None, "Pilih pemilik akun")


def unauthorized(prev_link):
    return div[
        a(href=prev_link)["← Kembali ke tabel user"],
        blockquote["Unauthorized"]
    ]


def change_password_form(username):
    return dialog("#ubah_password", open=True)[
        form(
            autocomplete="off",
            hx_put=f"/users/{username}/pass",
            hx_target="#form",
            hx_indicator="#form",
            _="on keyup[event.key=='Enter'] halt the event"
        )[
            article[
                header[
                    button(aria_label="Close",
                           _="on click toggle @open on #ubah_password",
                           rel="prev"),
                    h4["Ubah Password"],
                ],
                inlabel("Password Lama", "password",
                        "password"),
                inlabel("Password Baru", "password",
                        "password_new"),
                inlabel("Konfirmasi Password Baru", "password",
                        "password_new_confirm",
                        hs="""
on input
    if <[name='password_new']/>'s value is not my value then
        hide #pass_submit
        show #error
        halt the event
    else
        hide #error
        if <[name='password']/>'s value is not "" show #pass_submit
    end
                        """
                        ),
                small("#error", style="color: red; display: none;",
                      )["Password baru tidak sesuai"],
                footer[
                    button(".secondary", type_="button",
                           _="on click toggle @open on #ubah_password"
                           )["Cancel"],
                    button("#pass_submit", type_="submit", style="width: auto; display: none;",
                           )["Confirm"]
                ]]]
    ]

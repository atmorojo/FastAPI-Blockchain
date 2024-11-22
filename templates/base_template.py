from htpy import (
    html,
    head,
    meta,
    link,
    title,
    body,
    div,
    main,
    a,
    Node,
    Element,
    style,
    script,
)


def base_page(
    *,
    page_title: str | None = None,
    extra_head: Node = None,
    content: Node = None,
    body_class: str | None = None,
) -> Element:
    return html(lang="en", data_theme="light")[
        head[
            meta(charset="utf-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1"),
            meta(name="color-scheme", content="light dark"),
            link(rel="icon", href="/files/favicon.png", type_="image/png"),
            link(rel="stylesheet", href="/static/pico.blue.min.css"),
            link(rel="stylesheet", href="/static/bootstrap-icons.min.css"),
            link(rel="stylesheet", href="/static/style.css"),
            script(src="/static/htmx.min.js"),
            script(src="/static/hyperscript.org.0.9.12.js", defer=True),
            title[page_title],
            extra_head,
        ],
        body[main("#content")[content],],
    ]

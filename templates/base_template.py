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
    style
)


def base_page(*,
              page_title: str | None = None,
              extra_head: Node = None,
              content: Node = None,
              body_class: str | None = None,
              ) -> Element:
    return html(lang="en", data_theme="light")[
        head[
            meta(charset="utf-8"),
            meta(
                name="viewport",
                content="width=device-width, initial-scale=1"
            ),
            meta(name="color-scheme", content="light dark"),
            link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.sand.min.css"
            ),
            style["""
                  body {
                  display: flex;
                  width: inherit;
                  justify-content: center;
                  }
                  """],
            title[page_title],
            extra_head
        ],
        body[
            main("#content")[content],
            div("#footer")[
                "© Copyright 2024 by ",
                a(href="#")["me"]
            ]
        ]
    ]

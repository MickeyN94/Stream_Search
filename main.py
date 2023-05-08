from nicegui import ui
from backend import get_shows, get_service_logo


def get_logo(stream):
    url = get_service_logo(stream)
    return ui.html(f"<img src='{url}' width='30'>") 


def search_for_shows(search_field, search_row):
    
    shows = get_shows(search_field)  
    search_row.clear()
    create_row(shows, search_row)


def add_card(show):
    with ui.card() as card:
        card.props('style="width:250px;height:450px;"')
        card.classes('hover:scale-110 hover:z-10')
        card.tailwind.background_color('[#f9fafb]').padding('pt-0').align_items('center')

        ui.image(show['poster']).props('style="width:250px"').classes('-mx-4')
        with ui.card_section():
            with ui.row().classes('-my-4'):
                if show['streams']:
                    for stream, links in show['streams'].items():
                        with ui.link(target=links, new_tab=True).classes('hover:scale-110 hover:z-10'):
                            get_logo(stream)
                else:
                    ui.markdown(f"None available")


def create_row(shows, search_row):
    with search_row:
        for show in shows:
            if show['poster']:
                add_card(show)


def add_background():
    BACKGROUND_COLOUR = 'background-color: #242424'

    ui.left_drawer().style(BACKGROUND_COLOUR)
    ui.right_drawer().style(BACKGROUND_COLOUR)
    ui.query('body').style(BACKGROUND_COLOUR)

    with ui.footer(fixed=False).style(BACKGROUND_COLOUR).classes('gap-px'):
        ui.label("www.github.com/MickeyN94").classes('justify-center flex w-full')
        ui.label("Est. 2023").classes('justify-center flex w-full ')


def add_headers():
    with ui.column().classes('gap-4 md:gap-8 pt-10'):
        ui.markdown('WHERE 2 STREAM').classes('text-4xl sm:text-5xl md:text-6xl font-medium text-white')
        ui.markdown('Search to find where to stream your shows').classes('text-xl sm:text-2xl md:text-3xl leading-7 text-white') \
        .classes('max-w-[20rem] sm:max-w-[24rem] md:max-w-[30rem]')


@ui.page('/')
async def index_page():
    add_background()
    add_headers()
   # add_search_row()
    with ui.row().classes('justify-center item-center w-full'):
        search_field = ui.input().props('outlined v-model="text"; dense="dense"')
        search_field.tailwind.width('64').background_color('white')
        
        shows = ui.button('Search', on_click=lambda: search_for_shows(search_field.value, search_results))
        shows.tailwind.background_color('red').height('full').place_self('center')
    # blank row initially to be populated once search begins
    search_results = ui.row().classes('justify-between item-center w-full')


ui.run(show=True, 
    title="Where2Stream",
    favicon='📺')

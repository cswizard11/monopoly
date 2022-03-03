import asyncio
from random import randint
from Game import Game
from Action import Action
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import starlette.status as status
import uuid
from datetime import datetime

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory='templates')

game_saves = {}

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    today = datetime.today()
    to_remove = []
    for i in game_saves.keys():
        if (today - game_saves[i][1]).days > 14:
            to_remove.append(i)
    for i in to_remove:
        del game_saves[i]
    message = Action(None, '')
    monopoly = Game(message)
    game_id = uuid.uuid4().hex
    game_saves[game_id] = (monopoly, today)
    return templates.TemplateResponse('landing-page.html', {'request': request, 'game_id':game_id})

@app.post('/setup/{game}', response_class=HTMLResponse)
async def get_setup(request: Request, game: str):
    current_game = game_saves[game][0]
    if current_game.web_info.type == None:
        current_loop = asyncio.get_running_loop()
        current_loop.create_task(current_game.setup())
        await asyncio.sleep(0)
        buttons = current_game.web_info.type
        return templates.TemplateResponse('num-players-template.html', {'request': request, 'dialog' : current_game.web_info.information, 'nums': buttons, 'game_id':game})
    elif current_game.num_players == 0:
        form_data = await request.form()
        current_game.player_choice = int(form_data['choice'])
        text_fields = ['Player ' + str(x) for x in range(1, current_game.player_choice + 1)]
        await asyncio.sleep(0.01)
        return templates.TemplateResponse('naming-template.html', {'request': request, 'dialog' : current_game.web_info.information, 'names': text_fields, 'game_id':game})
    elif current_game.player_array == []:
        form_data = await request.form()
        players = []
        for i in range(0, current_game.num_players):
            players.append(form_data['Player ' + str(i + 1)])
        current_game.player_choice = players
        await asyncio.sleep(0.01)
        buttons = current_game.web_info.type
        return templates.TemplateResponse('roll-template.html', {'request': request, 'dialog' : current_game.web_info.information, 'nums': buttons, 'game_id':game})
    elif not(current_game.setup_complete):
        form_data = await request.form()
        current_game.player_choice = form_data['roll']
        await asyncio.sleep(0.01)
        buttons = current_game.web_info.type
        return templates.TemplateResponse('roll-template.html', {'request': request, 'dialog' : current_game.web_info.information, 'nums': buttons, 'game_id':game})
    else:
        form_data = await request.form()
        current_game.player_choice = form_data['roll']
        current_loop = asyncio.get_running_loop()
        current_loop.create_task(current_game.play())
        await asyncio.sleep(0)
        buttons = current_game.web_info.type
        return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : current_game.web_info.information,
                                                                'nums': buttons, 'game_id':game})

@app.get('/play/{game}', response_class=HTMLResponse)
async def get_play(request: Request, game: str):
    if not(game in game_saves.keys()):
        return RedirectResponse('/', status_code=404)
    else:
        current_game = game_saves[game][0]
        await asyncio.sleep(0.01)
        buttons = current_game.web_info.type
        return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : current_game.web_info.information,
                                                                'nums': buttons, 'game_id':game})

@app.post('/play/{game}', response_class=HTMLResponse)
async def post_play(request: Request, game: str):
    current_game = game_saves[game][0]
    form_data = await request.form()
    if not(form_data['choice'] in current_game.web_info.type):
        return RedirectResponse('/play/' + str(game), status_code=status.HTTP_302_FOUND)
    else:
        current_game.player_choice = form_data['choice']
        await asyncio.sleep(0.01)
        buttons = current_game.web_info.type
        return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : current_game.web_info.information,
                                                                'nums': buttons, 'game_id':game})
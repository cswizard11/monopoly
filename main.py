import asyncio
from Game import Game
from Action import Action
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

message = Action(None, '')
monopoly = Game(message)

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('landing-page.html', {'request': request})

@app.post('/setup', response_class=HTMLResponse)
async def get_setup(request: Request):
    if monopoly.web_info.type == None:
        current_loop = asyncio.get_running_loop()
        current_loop.create_task(monopoly.setup())
        await asyncio.sleep(0)
        buttons = monopoly.web_info.type
        return templates.TemplateResponse('num-players-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})
    elif monopoly.num_players == 0:
        form_data = await request.form()
        monopoly.player_choice = int(form_data['choice'])
        text_fields = ['Player ' + str(x) for x in range(1, monopoly.player_choice + 1)]
        await asyncio.sleep(0.01)
        return templates.TemplateResponse('naming-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'names': text_fields})
    elif monopoly.player_array == []:
        form_data = await request.form()
        players = []
        for i in range(0, monopoly.num_players):
            players.append(form_data['Player ' + str(i + 1)])
        monopoly.player_choice = players
        await asyncio.sleep(0.01)
        buttons = monopoly.web_info.type
        return templates.TemplateResponse('roll-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})
    elif not(monopoly.setup_complete):
        form_data = await request.form()
        monopoly.player_choice = form_data['roll']
        await asyncio.sleep(0.01)
        buttons = monopoly.web_info.type
        return templates.TemplateResponse('roll-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})
    else:
        form_data = await request.form()
        monopoly.player_choice = form_data['roll']
        current_loop = asyncio.get_running_loop()
        current_loop.create_task(monopoly.play())
        await asyncio.sleep(0)
        buttons = monopoly.web_info.type
        return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})

@app.post('/play', response_class=HTMLResponse)
async def post_play(request: Request):
    form_data = await request.form()
    monopoly.player_choice = form_data['choice']
    await asyncio.sleep(0.01)
    buttons = monopoly.web_info.type
    return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})


#monopoly.setup()

#monopoly.play()
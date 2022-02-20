import asyncio
from Game import Game
from Action import Action
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory='templates')

message = Action(0, '')
monopoly = Game(message)

@app.get("/enter-num/{num}", response_class=HTMLResponse)
async def make_buttons(request: Request, num: int):
    return templates.TemplateResponse('main-template.html', {'request': request, 'nums': [x for x in range(1, num + 1)]})

@app.get('/setup', response_class=HTMLResponse)
async def get_setup(request: Request):
    current_loop = asyncio.get_running_loop()
    current_loop.create_task(monopoly.setup())
    await asyncio.sleep(0)
    buttons = [x for x in range(1, monopoly.web_info.type + 1)]
    return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})

@app.post('/setup-pt2')
async def post_play(request: Request, next_number: int = Form(...)):
    monopoly.player_choice = next_number
    await asyncio.sleep(0.01)
    text_fields = ['Player ' + str(x) for x in range(1, monopoly.player_choice + 1)]
    return templates.TemplateResponse('naming-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'names': text_fields})

@app.post('/play')
async def post_play(request: Request, next_number: int = Form(...)):
    monopoly.player_choice = next_number
    await asyncio.sleep(0.01)
    buttons = [x for x in range(1, monopoly.player_choice + 1)]
    return templates.TemplateResponse('main-template.html', {'request': request, 'dialog' : monopoly.web_info.information, 'nums': buttons})


#monopoly.setup()

#monopoly.play()
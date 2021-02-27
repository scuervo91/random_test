import typer

app = typer.Typer()

@app.command()
def create(username:str = typer.Option(...,'--username','-u', prompt='Choose username?'), password:str=typer.Option(...,'--password','-p',prompt=True, confirmation_prompt=True,hide_input=True)):
	typer.secho(f"You've created new user", bold=True)
	typer.secho(f' {username}', fg = typer.colors.GREEN)
	typer.secho(f' {password}', fg = typer.colors.WHITE, bg = typer.colors.MAGENTA, blink=True)


if __name__== "__main__":
	app()

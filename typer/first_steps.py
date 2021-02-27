import typer
from typing import Optional
def main(name:str, lastname:str=typer.Argument(''), age:Optional[int]=typer.Option(...,prompt='How old are you', confirmation_prompt=True),  formal:bool=False):
	"""
	Say hi to NAME, Optionally with a --lastname.
	If --formal is used. the greeting is very formal
	"""
	if formal:
		message = 'Good Day'
		ending =typer.style(f'{name} {lastname}. You have {age} years old', fg=typer.colors.GREEN, bold=True)
	else:
		message = 'whats up nigga'
		ending = typer.style(f"{name} {lastname}. You have {age} years old", fg=typer.colors.WHITE, bg=typer.colors.RED)
	plus = typer.style(' some new features', blink=True, underline=True)

	typer.echo(message + ending + plus)

if __name__ == "__main__":
	typer.run(main)

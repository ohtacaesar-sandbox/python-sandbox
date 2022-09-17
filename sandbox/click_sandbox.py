import click


@click.group()
@click.option("--option")
@click.pass_context
def main(ctx: click.Context, option):
    ctx.ensure_object(dict)
    ctx.obj['option'] = option


@main.command()
@click.option("--option")
@click.pass_context
def command(ctx: click.Context, option):
    o = ctx.obj.get('option')
    click.echo(f"main.option == '{o}', command.option == '{option}'")


if __name__ == '__main__':
    main()

import click


def validate_recv_window(ctx, param, value):
    if value is None:
        raise click.BadParameter('recv_window cannot be null')

    if int(value) > 60000:
        raise click.BadParameter(str(value) + '. Cannot exceed 60000')

    return value


def validate_locked_free(ctx, param, value):
    if value is None:
        return

    value = str(value).upper()
    if value not in ['L', 'F', 'B']:
        raise click.BadParameter(value + '. Possible values: A | L | F | B')

    return value


def validate_side(ctx, param, value):
    value = str(value).upper()

    if value not in ['BUY', 'SELL']:
        raise click.BadParameter(value + '. Possible values: BUY | SELL')

    return value


def validate_time_in_force(ctx, param, value):
    if value is None:
        return value

    value = str(value).upper()

    if value not in ['GTC', 'IOC', 'FOK']:
        raise click.BadParameter(value + '. Possible values: GTC | IOC | FOK')

    return value

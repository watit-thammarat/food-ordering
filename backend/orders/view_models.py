def get_menu(entry):
    return {'id': entry.id, 'name': entry.name}


def get_menu_list(entries):
    return [get_menu(entry) for entry in entries]


def get_order(entry):
    return {'id': entry.id, 'menu': get_menu(entry.menu)}


def get_order_summary(entries):
    return [{'id': entry['menu__id'], 'name': entry['menu__name'],
             'total': entry['total']} for entry in entries]

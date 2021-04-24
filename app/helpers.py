import app.dbconnection as db
from operator import itemgetter


def check_if_login_exists(login):
    logins = db.find_row('konta', 'login', login)
    if len(logins) > 0:
        return True
    return False


def find_rights(login):
    return db.find_parameter('konta', 'uprawnienia', 'login', login)


def create_service_view(form):
    companies = db.find_table('firma')
    companies = [(item[0], item[1]) for item in companies]
    services = db.find_table('rodzaj_uslugi')
    form.company.choices = companies
    form.service.choices = services
    return form


def add_service_to_db(form):
    services = form.service.data
    time = form.time.data
    status = 1
    date = form.date.data
    company = form.company.data
    for service in services:
        db.insert_planned_service([company, service, date, time, status])


def create_orders_list_view():
    data = []
    services = db.find_table('usluga')
    for service in services:
        id = service[0]
        company_name = db.find_parameter('firma', 'nazwa', 'id', service[1])
        service_type = db.find_parameter('rodzaj_uslugi', 'nazwa', 'id', service[2])
        date = service[3]
        time = service[4]
        status = db.find_parameter('status_uslugi', 'status', 'id', service[5])
        data.append([id, company_name, service_type, date, time, status])
    return data


def find_name_by_id(data, id):
    for chunk in data:
        if chunk[0] == id:
            return chunk[1]
    return None


def return_supply_sign_and_producent(supply, id):
    for chunk in supply:
        if chunk[0] == id:
            return chunk[2], chunk[3]
    return None


def return_supply_full_name(supply, supply_sign, supply_producent, id):
    sign_id, producent_id = return_supply_sign_and_producent(supply, id)
    sign = find_name_by_id(supply_sign, sign_id)
    producent = find_name_by_id(supply_producent, producent_id)
    name = sign + " " + producent
    return name


def convert_supplies_list_into_string(data):
    companies = db.find_table('firma')
    supply_table = db.find_table('sprzet')
    powder_type = db.find_table('typ_proszku')
    supply_sign = db.find_table('oznaczenie_sprzetu')
    supply_producent = db.find_table('producent_sprzetu')

    final_data = []

    for company_id, room, supplies in data:
        name = find_name_by_id(companies, company_id)
        converted_supplies = []
        for supply in supplies:
            sup_name = return_supply_full_name(supply_table, supply_sign, supply_producent, supply[0])
            powder = find_name_by_id(powder_type, supply[1])
            if powder is None:
                powder = ''
            year = supply[2]
            converted_supplies.append(sup_name + ' ' + powder + ' ' + str(year))
        final_data.append([name, room, converted_supplies])
    return final_data


def create_supplies_list_view():
    data, final_data = [], []
    supplies = sorted(db.find_table('sprzet_firma'), key=itemgetter(2))

    current_company_id = supplies[0][2]
    current_room = supplies[0][3]
    current_supplies = []
    for id, supply_id, company_id, room, year, powder_type in supplies:
        if current_company_id != company_id:
            data.append([current_company_id, current_room, current_supplies])
            current_supplies = [[supply_id, powder_type, year]]
            current_room = room
            current_company_id = company_id
        else:
            if current_room == room:
                current_supplies.append([supply_id, powder_type, year])
            else:
                data.append([current_company_id, current_room, current_supplies])
                current_room = room
                current_supplies = [[supply_id, powder_type, year]]

    data.append([current_company_id, current_room, current_supplies])
    return convert_supplies_list_into_string(data)

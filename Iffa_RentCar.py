#!/opt/anaconda3/bin/python3
from tabulate import tabulate
import csv

CarList = {
    'B 3 ST': {
        'plate_number': 'B 3 ST',
        'type': 'Toyota Avanza',
        'color': 'Off-White',
        'owner': 'Iffa',
        'contact': '08126660808',
        'status': 'Available',
        'price': 450000
    },
    'B 34 UT': {
        'plate_number': 'B 34 UT',
        'type': 'Honda Brio',
        'color': 'Silver',
        'owner': 'Aulia',
        'contact': '08110008989',
        'status': 'In for service',
        'price': 350000
    },
    'B 4 DD': {
        'plate_number': 'B 4 DD',
        'type': 'Daihatsu Ayla',
        'color': 'Red',
        'owner': 'Ayu',
        'contact': '0812000999',
        'status': 'Available',
        'price': 350000
    }
}

def _input_int(prompt, default=None):
    while True:
        raw = input(prompt).strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("Please enter a valid number.")

def _confirm(prompt):
    while True:
        ans = input(f"{prompt} (y/n): ").strip().lower()
        if ans in ("y", "n"):
            return ans == "y"
        print("Please answer with 'y' or 'n'.")

def _input_with_default(prompt, default_str):
    raw = input(f"{prompt} [{default_str}]: ").strip()
    return raw if raw != "" else default_str

def _list_cars():
    return list(CarList.values())

def _display_single_by_index(index1_based):
    cars = _list_cars()
    if index1_based < 1 or index1_based > len(cars):
        print("\n<<< Index out of range >>>")
        return
    display([cars[index1_based - 1]])

CSV_HEADERS = ["plate_number", "type", "color", "owner", "contact", "status", "price"]

def export_csv(filepath="carlist.csv"):
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for plate, car in CarList.items():
                writer.writerow({
                    "plate_number": car["plate_number"],
                    "type": car["type"],
                    "color": car["color"],
                    "owner": car["owner"],
                    "contact": car["contact"],
                    "status": car["status"],
                    "price": car["price"],
                })
        print(f'\n<<< Exported {len(CarList)} records to "{filepath}" >>>')
    except Exception as e:
        print(f"\n<<< Failed to export CSV: {e} >>>")

def main_menu():
    while True:
        try:
            req = int(input(''' 
<<<<< WELCOME TO RUSSELL RENT CAR >>>>>

Menu:
    1. Display Car Data
    2. Add Car Data
    3. Update Car Data
    4. Delete Car Data
    5. Export to CSV
    6. Exit

Enter the menu number you want to run: ''')) 
            if req in (1, 2, 3, 4, 5, 6):
                return req
            print('Please enter 1-6 only.')
        except ValueError:
            print('Please enter a number.')

def display(data):
    print('\nCar List at Russell Rent Car')
    print('-' * 130)
    iterable = data.values() if isinstance(data, dict) else data
    rows = []
    for idx, car in enumerate(iterable, start=1):
        rows.append([
            idx,
            car['plate_number'],
            car['type'],
            car['color'],
            car['owner'],
            car['contact'],
            car['status'],
            f"{car['price']:,}"
        ])
    headers = ["Index", "Plate Number", "Type", "Color", "Owner", "Contact", "Status", "Rent Price"]
    align = ("right", "left", "left", "left", "left", "left", "left", "right")
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid", colalign=align))
    print('-' * 130)

def menu_read():
    while True:
        try:
            option = int(input('''
------------------------------------------------------------------------------------------------
Display Data Options:
    1. Show all cars
    2. View car by INDEX number
    3. View car by LICENSE PLATE
    4. Back to Main Menu

Choose: ''').strip())
        except ValueError:
            print('Please enter 1/2/3/4.')
            continue
        if len(CarList) == 0:
            print('\n<<< No car data available >>>')
            if option == 4:
                break
            else:
                continue
        if option == 1:
            display(CarList)
        elif option == 2:
            display(CarList)
            idx = _input_int('\nEnter the car INDEX number you want to view: ')
            _display_single_by_index(idx)
        elif option == 3:
            find_plate_number = input('\nInsert the car LICENSE PLATE: ').upper().strip()
            if find_plate_number in CarList:
                display([CarList[find_plate_number]])
            else:
                print('\n<<< No car data available >>>')
        elif option == 4:
            break
        else:
            print('Please enter 1/2/3/4.')

def menu_create():
    while True:
        option = input('\nAdd a new car? (y/n): ').lower().strip()
        if option == 'y':
            new_plate_number = input('\nEnter License Plate: ').upper().strip()
            if new_plate_number in CarList:
                print(f'\n<<< Car with plate {new_plate_number} already exists >>>')
                continue
            new_type    = input('Enter The Car Type: ').strip().title()
            new_color   = input('Enter The Car Color: ').strip().title()
            new_owner   = input('Enter The Car Owner: ').strip().title()
            new_contact = input('Enter The Car Contact Owner: ').strip()
            new_status  = input('Enter The Car Status: ').strip().title()
            new_price   = _input_int('Enter The Rent Price: ')
            temp = {
                'plate_number': new_plate_number,
                'type': new_type,
                'color': new_color,
                'owner': new_owner,
                'contact': new_contact,
                'status': new_status,
                'price': new_price
            }
            print("\nSummary (New Record):")
            display([temp])
            if _confirm('Save this new car?'):
                CarList[new_plate_number] = temp
                print('\n<<< Data has been saved successfully! >>>')
                display(CarList)
            else:
                print('\n<<< Data has not been recorded! >>>')
        elif option == 'n':
            break

def menu_update():
    while True:
        option = input('\nDo you want to update a car’s information? (y/n): ').lower().strip()
        if option == 'y':
            find_plate_number = input('\nEnter The Car License Plate: ').upper().strip()
            if find_plate_number not in CarList:
                print(f'\n<<< No car found with license plate {find_plate_number} >>>')
                continue
            current = CarList[find_plate_number]
            print("\nCurrent data:")
            display([current])
            try:
                column = int(input('''
Column Index:
    1. Car Type
    2. Car Color
    3. Owner Name
    4. Owner Contact
    5. Car Status
    6. Rent Price
    7. All Fields

Enter the column index you want to edit: ''').strip())
            except ValueError:
                print('Please enter 1-7.')
                continue
            draft = current.copy()
            if column == 1:
                draft['type'] = _input_with_default('New Car Type', current['type']).title()
            elif column == 2:
                draft['color'] = _input_with_default('New Car Color', current['color']).title()
            elif column == 3:
                draft['owner'] = _input_with_default('New Owner Name', current['owner']).title()
            elif column == 4:
                draft['contact'] = _input_with_default('New Owner Contact', current['contact'])
            elif column == 5:
                draft['status'] = _input_with_default('New Car Status', current['status']).title()
            elif column == 6:
                draft['price'] = _input_int('New Rent Price (press Enter to keep current): ', default=current['price'])
            elif column == 7:
                draft['type']    = _input_with_default('Car Type', current['type']).title()
                draft['color']   = _input_with_default('Car Color', current['color']).title()
                draft['owner']   = _input_with_default('Owner Name', current['owner']).title()
                draft['contact'] = _input_with_default('Owner Contact', current['contact'])
                draft['price']   = _input_int('Rent Price (press Enter to keep current): ', default=current['price'])
                draft['status']  = _input_with_default('Car Status', current['status']).title()
            else:
                print('Please enter 1-7.')
                continue
            print("\nProposed changes:")
            display([draft])
            if _confirm('Apply these changes?'):
                CarList[find_plate_number] = draft
                print('\n<<< Data has been updated successfully! >>>')
                display(CarList)
            else:
                print('\n<<< Data has not been recorded! >>>')
        elif option == 'n':
            break

def menu_delete():
    while True:
        option = input('\nDo you want to delete a car record? (y/n): ').lower().strip()
        if option == 'y':
            find_plate_number = input('Enter the Car License Plate: ').upper().strip()
            if find_plate_number not in CarList:
                print(f'\n<<< No car found with license plate {find_plate_number} >>>')
                continue
            print("\nSelected record to delete:")
            display([CarList[find_plate_number]])
            if _confirm('Are you sure you want to delete this car data?'):
                del CarList[find_plate_number]
                print('\n<<< Data has been deleted successfully! >>>')
                display(CarList)
            else:
                print('\n<<< Data has not been deleted! >>>')
        elif option == 'n':
            break

def menu_exit():
    print('\n<<< You have logged out of the Russell Rent Car application! >>>\n')

if __name__ == "__main__":
    while True:
        req = main_menu()
        if req == 1:
            menu_read()
        elif req == 2:
            menu_create()
        elif req == 3:
            menu_update()
        elif req == 4:
            menu_delete()
        elif req == 5:
            filename = _input_with_default("Filename to export", "carlist.csv")
            export_csv(filename)
        elif req == 6:
            menu_exit()
            break

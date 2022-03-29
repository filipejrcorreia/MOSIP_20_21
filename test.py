import PySimpleGUI as sg    

sg.theme('DarkAmber')
tab1_layout = [
            [sg.Text('Number of patients:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('Number of receptionists')],
            [sg.Text('Admission:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('Reception:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('Number of Health Professionals')],
            [sg.Text('Triage:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('Orthopedists:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('General Practioners:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('Cardiologists:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('Pneumologists:')],
            [sg.Input(size=(10,1), enable_events=True)],
            [sg.Text('X-Ray Specialists:')],
            [sg.Input(size=(10,1), enable_events=True)]
]    

tab2_layout = [
            [sg.Text('Arrival time')],
            [sg.InputText("1.9",size=(10,1),enable_events=True)],
            [sg.Text('Admission time')],
            [sg.Text('Alpha'),sg.InputText("0.5",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("28.99466",size=(10,1),enable_events=True)],
            [sg.Text('Triage time')],
            [sg.Text('Alpha'),sg.InputText("1.40",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("14.73",size=(10,1),enable_events=True)],
            [sg.Text('Attendance time (orthopedy)')],
            [sg.Text('Alpha'),sg.InputText("1.40",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("14.73",size=(10,1),enable_events=True)],
            [sg.Text('Attendance time (general office')],
            [sg.Text('Alpha'),sg.InputText("1.025693",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("50.48364",size=(10,1),enable_events=True)],
            [sg.Text('Attendance time (cardiology)')],
            [sg.Text('Alpha'),sg.InputText("2.020726",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("17.84471",size=(10,1),enable_events=True)],
            [sg.Text('Attendance time (pulmonology)')],
            [sg.Text('Alpha'),sg.InputText("0.596",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("21.96504",size=(10,1),enable_events=True)],
            [sg.Text('X-Ray time')],
            [sg.Text('Alpha'),sg.InputText("1.820375",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("35.56721",size=(10,1),enable_events=True)],
            [sg.Text('Dismission time')],
            [sg.Text('Alpha'),sg.InputText("4.645811",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("0.02025451",size=(10,1),enable_events=True)]
            [sg.Text('Bracelet colour')],
            [sg.Input(size=(10,1), enable_events=True)],
]  

layout = [[sg.TabGroup([[sg.Tab('Population', tab1_layout), 
        sg.Tab('Distributions', tab2_layout)]])],    
        [sg.Button('Confirm'), sg.Button('Cancel')]]

window = sg.Window('Simulation Form', layout, default_element_size=(30,1))    

while True:
    event, values = window.read()
    print(values) #debug clicks
    if event in (sg.WIN_CLOSED, 'Cancel'):
        break
    if event == 'Confirm':
        invalid_values = list()
        for i in values:
            if values[i] != values[len(values)-1]: # the last value is always the tab name
                current_value = values[i]
                if not current_value.replace('.','',1).isdigit(): # validate non numeric values
                    if values[i] == '':
                        values[i] = 'Field number ' + str(i+1) + ' is empty'
                    invalid_values.append(values[i])
        # display the invalid input if there is any
        if invalid_values: 
            errors = ""
            for error in invalid_values:
                errors += error + ', '
            sg.popup_no_wait('Invalid input: ' + errors)
        else:
            print('a') #save variables
window.close()
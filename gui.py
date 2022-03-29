import PySimpleGUI as sg    
from simulation import Simulation
from settings import Settings

class GUI:
    def __init__(self):
        sg.theme('DarkAmber')
        tab1_layout = [
                    [sg.Text('Number of receptionists')],
                    [sg.Text('Admission:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('Dismission:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('Number of Health Professionals')],
                    [sg.Text('Triage:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('Orthopedists:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('General Practioners:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('Cardiologists:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('Pneumologists:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('X-Ray Specialists:')],
                    [sg.Input("2",size=(10,1), enable_events=True)],
                    [sg.Text('Simulation time:')],
                    [sg.InputText("250",size=(10,1),enable_events=True)]
        ]    

        tab2_layout = [
                    [sg.Text('Admission time')],
                    [sg.Text('Alpha'),sg.InputText("28.99466",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("0.5",size=(10,1),enable_events=True)],
                    [sg.Text('Triage time')],
                    [sg.Text('Alpha'),sg.InputText("1.401984",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("12.43832",size=(10,1),enable_events=True)],
                    [sg.Text('Attendance time (orthopedy)')],
                    [sg.Text('Alpha'),sg.InputText("37.57723",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("1.0155",size=(10,1),enable_events=True)],
                    [sg.Text('Attendance time (general office')],
                    [sg.Text('Alpha'),sg.InputText("50.48364",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("1.025693",size=(10,1),enable_events=True)],
                    [sg.Text('Attendance time (cardiology)')],
                    [sg.Text('Alpha'),sg.InputText("17.84471",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("2.020726",size=(10,1),enable_events=True)],
                    [sg.Text('Attendance time (pulmonology)')],
                    [sg.Text('Alpha'),sg.InputText("21.96504",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("0.596",size=(10,1),enable_events=True)],
                    [sg.Text('X-Ray time')],
                    [sg.Text('Alpha'),sg.InputText("35.56721",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("1.820375",size=(10,1),enable_events=True)],
                    [sg.Text('Dismission time')],
                    [sg.Text('Alpha'),sg.InputText("4.645811",size=(10,1),enable_events=True),sg.Text('Beta'),sg.InputText("49.37173",size=(10,1),enable_events=True)],
                    [sg.Text('Armband colour')],
                    [sg.InputText("1.97",size=(10,1),enable_events=True)],
                    [sg.Text('Arrival time')],
                    [sg.InputText("1.9",size=(10,1),enable_events=True)]
        ]

        self.layout = [[sg.TabGroup([[sg.Tab('Population', tab1_layout), 
                sg.Tab('Distributions', tab2_layout)]])],    
                [sg.Button('Confirm'), sg.Button('Cancel')]]
        
        #self.simulation = Simulation()


    def start(self):
        window = sg.Window('Simulation Form', self.layout, default_element_size=(30,1))    

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
                    settings = Settings()
                    settings.number_of_admission_personel = int(values[0])
                    settings.number_of_dismission_personel = int(values[1])
                    settings.number_of_triage_personel = int(values[2])
                    settings.number_of_orthopedists = int(values[3])
                    settings.number_of_general_pratictioners = int(values[4])
                    settings.number_of_general_cardiologists = int(values[5])
                    settings.number_of_general_pulmonologists = int(values[6])
                    settings.number_of_general_xray_specialists = int(values[7])
                    settings.max_clock = int(values[8])

                    settings.admission_duration_alpha_setting = float(values[9])
                    settings.triage_duration_alpha_setting = float(values[11])
                    settings.orthopedy_duration_alpha_setting = float(values[13])
                    settings.general_office_duration_alpha_setting = float(values[15])
                    settings.cardiology_duration_alpha_setting = float(values[17])
                    settings.pulmonology_duration_alpha_setting = float(values[19])
                    settings.xray_duration_alpha_setting = float(values[21])
                    settings.dismission_duration_alpha_setting = float(values[23])

                    settings.admission_duration_beta_setting = float(values[10])
                    settings.triage_duration_beta_setting  = float(values[12])
                    settings.orthopedy_duration_beta_setting = float(values[14])
                    settings.general_office_duration_beta_setting  = float(values[16])
                    settings.cardiology_duration_beta_setting = float(values[18])
                    settings.pulmonology_duration_beta_setting = float(values[20])
                    settings.xray_duration_beta_setting = float(values[22])
                    settings.dismission_duration_beta_setting = float(values[24])

                    settings.armband_setting = float(values[25])
                    settings.arrival_time_setting = float(values[26])
                    #run simulation
                    self.simulation = Simulation(settings)
                    self.simulation.run()
        window.close()
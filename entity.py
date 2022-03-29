from event import Event
from enum import Enum


class Entity:

    def __init__(self):
        self.is_available = True

    def set_free(self):
        self.is_available = True

    def set_occupied(self):
        self.is_available = False

    def get_state(self):
        return self.is_available

class Emergency_Color(Enum):

    GREEN = 0
    YELLOW = 1
    ORANGE = 2
    RED = 3


class Patient(Entity):

    def __init__(self):
        Entity.__init__(self)
        self.emergency_color = None
        self.is_brought_by_ambulance = None
        self.speciality_origin = None
        self.event_list = []
        self.id = -1
        self.has_been_in_xray = False

    def set_green_armband(self):
        self.emergency_color = Emergency_Color.GREEN

    def set_yellow_armband(self):
        self.emergency_color = Emergency_Color.YELLOW

    def set_orange_armband(self):
        self.emergency_color = Emergency_Color.ORANGE

    def set_red_armband(self):
        self.emergency_color = Emergency_Color.RED

    def set_brought_by_ambulance(self):
        self.is_brought_by_ambulance = True

    def set_not_brought_by_ambulance(self):
        self.is_brought_by_ambulance = False

    def get_armband_color(self):
        return self.emergency_color

    def get_ambulance_status(self):
        return self.is_brought_by_ambulance

    def set_orthpedist_origin(self):
        self.speciality_origin = Speciality.ORTHOPEDIST

    def set_pulmonologist_origin(self):
        self.speciality_origin = Speciality.PULMONOLOGIST

    def set_cardiologist_origin(self):
        self.speciality_origin = Speciality.CARDIOLOGIST

    def set_general_practitioner_origin(self):
        self.speciality_origin = Speciality.GENERAL_PRATICTIONER
    
    def print_workflow(self):
        for item in self.event_list:
            print(item)



class Speciality(Enum):

    TRIAGE = 0
    ORTHOPEDIST = 1
    GENERAL_PRATICTIONER = 2
    CARDIOLOGIST = 3
    PULMONOLOGIST = 4
    X_RAY_SPECIALIST = 5


class Health_Professional(Entity):

    def __init__(self, speciality, identification_number):
        self.speciality = speciality
        self.identification = str(speciality.value) + "_" + str(identification_number)
        Entity.__init__(self)

    def set_triage(self):
        self.speciality = Speciality.TRIAGE

    def set_orthpedist(self):
        self.speciality = Speciality.ORTHOPEDIST

    def set_pulmonologist(self):
        self.speciality = Speciality.PULMONOLOGIST

    def set_cardiologist(self):
        self.speciality = Speciality.CARDIOLOGIST

    def set_general_practitioner(self):
        self.speciality = Speciality.GENERAL_PRATICTIONER

    def set_x_ray_specialist(self):
        self.speciality = Speciality.X_RAY_SPECIALIST

    def get_speciality(self):
        return self.speciality


class Receptionist(Entity):

    def __init__(self, office, identification_number):
        Entity.__init__(self)
        self.office = office
        self.identification = office + str(identification_number)

    def set_entry_office(self):
        self.office = 'Entry'

    def set_exit_office(self):
        self.office = 'Exit'

    def get_office(self):
        return self.office
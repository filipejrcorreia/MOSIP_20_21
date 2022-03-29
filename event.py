import time
import numpy as np
from enum import Enum
from random import expovariate, weibullvariate, gammavariate

class Event_type(Enum):

    PATIENT_ARRIVES = 0
    PATIENT_ENDS_ADMISSION = 1
    PATIENT_ENDS_TRIAGE = 2
    PATIENT_ENDS_ORTHOPEDY = 3
    PATIENT_ENDS_GENERAL_OFFICE = 4
    PATIENT_ENDS_CARDIOLOGY = 5
    PATIENT_ENDS_PULOMONLOGY = 6
    PATIENT_ENDS_X_RAY = 7
    PATIENT_ENDS_DISMISSION = 8


class Event:

    def __init__(self,settings):
        self.time_of_occurence = 0
        self.event_type = None
        self.settings = settings
        #np.random.seed(int(time.time()))

    def scale_patient_arrives(self, clock):
        lambda_value = self.settings.arrival_time_setting
        self.time_of_occurence = expovariate(lambda_value)+clock
        self.event_type = Event_type.PATIENT_ARRIVES

    def scale_patient_ends_admission(self, clock):
        alpha_value = self.settings.admission_duration_alpha_setting
        beta_value = self.settings.admission_duration_beta_setting
        self.time_of_occurence = weibullvariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_ADMISSION

    def scale_patient_ends_triage(self, clock):
        alpha_value = self.settings.triage_duration_alpha_setting
        beta_value = self.settings.triage_duration_beta_setting
        self.time_of_occurence = gammavariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_TRIAGE

    def scale_patient_ends_orthopedy(self, clock):
        alpha_value = self.settings.orthopedy_duration_alpha_setting
        beta_value = self.settings.orthopedy_duration_beta_setting
        self.time_of_occurence = weibullvariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_ORTHOPEDY

    def scale_patient_ends_general_office(self, clock):
        alpha_value = self.settings.general_office_duration_alpha_setting
        beta_value = self.settings.general_office_duration_beta_setting
        self.time_of_occurence = weibullvariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_GENERAL_OFFICE

    def scale_patient_ends_cardiology(self, clock):
        alpha_value = self.settings.cardiology_duration_alpha_setting
        beta_value = self.settings.cardiology_duration_beta_setting
        self.time_of_occurence = weibullvariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_CARDIOLOGY

    def scale_patient_ends_pulmonology(self, clock):
        alpha_value = self.settings.pulmonology_duration_alpha_setting
        beta_value = self.settings.pulmonology_duration_beta_setting
        self.time_of_occurence = weibullvariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_PULOMONLOGY

    def scale_patient_ends_xray(self, clock):
        alpha_value = self.settings.xray_duration_alpha_setting
        beta_value = self.settings.xray_duration_beta_setting
        self.time_of_occurence = weibullvariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_X_RAY

    def scale_patient_ends_dismission(self, clock):
        alpha_value = self.settings.dismission_duration_alpha_setting
        beta_value = self.settings.dismission_duration_beta_setting
        self.time_of_occurence = gammavariate(alpha_value, beta_value)+clock
        self.event_type = Event_type.PATIENT_ENDS_DISMISSION

    def next_event(self):
        if self.event_type == Event_type.PATIENT_ARRIVES:
            return Event_type.PATIENT_ENDS_ADMISSION

        if self.event_type == Event_type.PATIENT_ENDS_ADMISSION:
            return Event_type.PATIENT_ENDS_TRIAGE

        if self.event_type == Event_type.PATIENT_ENDS_TRIAGE:
            distribution = np.random.random_integers(1, 4)
            if distribution == 1:
                return Event_type.PATIENT_ENDS_CARDIOLOGY
            if distribution == 2:
                return Event_type.PATIENT_ENDS_GENERAL_OFFICE
            if distribution == 3:
                return Event_type.PATIENT_ENDS_ORTHOPEDY
            if distribution == 4:
                return Event_type.PATIENT_ENDS_PULOMONLOGY

        if self.event_type == Event_type.PATIENT_ENDS_GENERAL_OFFICE:
            distribution = np.random.binomial(n=1, p= 0.5)
            if distribution == 1:
                return Event_type.PATIENT_ENDS_X_RAY
            else:
                return Event_type.PATIENT_ENDS_DISMISSION

        if self.event_type == Event_type.PATIENT_ENDS_CARDIOLOGY:
            distribution = np.random.binomial(n=1, p= 0.5)
            if distribution == 1:
                return Event_type.PATIENT_ENDS_X_RAY
            else:
                return Event_type.PATIENT_ENDS_DISMISSION

        if self.event_type == Event_type.PATIENT_ENDS_ORTHOPEDY:
            distribution = np.random.binomial(n=1, p= 0.5)
            if distribution == 1:
                return Event_type.PATIENT_ENDS_X_RAY
            else:
                return Event_type.PATIENT_ENDS_DISMISSION

        if self.event_type == Event_type.PATIENT_ENDS_PULOMONLOGY:
            distribution = np.random.binomial(n=1, p= 0.5)
            if distribution == 1:
                return Event_type.PATIENT_ENDS_X_RAY
            else:
                return Event_type.PATIENT_ENDS_DISMISSION
                
        if self.event_type == Event_type.PATIENT_ENDS_X_RAY:
            return Event_type.PATIENT_ENDS_DISMISSION

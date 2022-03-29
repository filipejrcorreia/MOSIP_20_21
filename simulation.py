import event
from report import Report
import numpy as np
import time
import entity
import report
from entity import Patient, Speciality, Emergency_Color
from event import Event
from event import Event_type

#Read simulation params
#Call init routine
#Execute simulation
#Call report generator
#Make the reports available

class Simulation:
 
    def __init__(self,settings):
        self.report = Report()
        self.settings = settings
        #Initialize medical professionals and administration personel

        self.admission_personel = self.start_entity_list(entity.Receptionist, "Entry", settings.number_of_admission_personel) #magic numbers must be editable
        self.report.setup_usage_stats(self.admission_personel,"Admission")

        self.triage_personel = self.start_entity_list(entity.Health_Professional, entity.Speciality.TRIAGE, settings.number_of_triage_personel)
        self.report.setup_usage_stats(self.triage_personel,entity.Speciality.TRIAGE.name)

        self.general_practitioners = self.start_entity_list(entity.Health_Professional, entity.Speciality.GENERAL_PRATICTIONER, settings.number_of_general_pratictioners)
        self.report.setup_usage_stats(self.general_practitioners,entity.Speciality.GENERAL_PRATICTIONER.name)

        self.orthopedists = self.start_entity_list(entity.Health_Professional, entity.Speciality.ORTHOPEDIST, settings.number_of_orthopedists)
        self.report.setup_usage_stats(self.orthopedists,entity.Speciality.ORTHOPEDIST.name)

        self.cardiologists = self.start_entity_list(entity.Health_Professional, entity.Speciality.CARDIOLOGIST, settings.number_of_general_cardiologists)
        self.report.setup_usage_stats(self.cardiologists,entity.Speciality.CARDIOLOGIST.name)

        self.pulmonologists = self.start_entity_list(entity.Health_Professional, entity.Speciality.PULMONOLOGIST, settings.number_of_general_pulmonologists)
        self.report.setup_usage_stats(self.pulmonologists,entity.Speciality.PULMONOLOGIST.name)

        self.x_ray_specialists = self.start_entity_list(entity.Health_Professional, entity.Speciality.X_RAY_SPECIALIST, settings.number_of_general_xray_specialists)
        self.report.setup_usage_stats(self.x_ray_specialists,entity.Speciality.X_RAY_SPECIALIST.name)

        self.dismission_personel = self.start_entity_list(entity.Receptionist, "Exit", settings.number_of_dismission_personel) #magic numbers must be editable
        self.report.setup_usage_stats(self.dismission_personel,"Dismission")


        # System state
        self.clock = self.start_clock()
        self.max_clock = settings.max_clock
        self.wait_queues = self.start_server_status()
        self.event_queues = []
        self.event_queues.append(self.scale_first_event())
        # Statistical Variables
        self.num_patients_received, self.num_global_patients_delays, self.total_delay, self.area_num_in_q, self.area_server_status, self.last_event_time = self.start_statistical_counters()
        
    #Startup Routine Methods

    def start_clock(self):
        return 0.0

    def start_server_status(self):
        wait_queues = {"admission_queue": [], #{patient:time}
                  "triage_queue": [],
                  "orthopedist_queue": [],
                  "general_practitioner_queue": [],
                  "cardiologist_queue": [],
                  "pulmonologist_queue": [],
                  "x_ray_queue": [],
                  "dismission_queue": []}
        return wait_queues

    def start_statistical_counters(self):
        num_patients_received = 0
        num_global_patients_delays = 0
        total_delay = 0
        area_num_in_q = 0
        area_server_status = 0
        last_event_time = 0
        return num_patients_received, num_global_patients_delays, total_delay, area_num_in_q, area_server_status, last_event_time

    def start_event_list(self):
        return 0

    def start_entity_list(self,entity,init_params,number):
        entities = []
        for num in range(number):
            entities.append(entity(init_params,num))
        return entities

    def scale_first_event(self):
        e = Event(self.settings)
        e.scale_patient_arrives(self.clock)
        p = Patient()
        return {"event":e,"patient":None}

    # Event Routine Methods

    def get_available(self,entity_list):
        for entity in entity_list:
            if entity.is_available:
                return entity
        return False

    def arrival_event_routine(self,ambulance_distribution,limit):
        p = Patient()
        p.id = self.num_patients_received
        if ambulance_distribution == limit:
            p.event_list.append("Arrived by ambulance at " + str(self.clock))
            p.set_brought_by_ambulance()
            triage = self.get_available(self.triage_personel)
            if triage:
                e = Event(self.settings)
                e.scale_patient_ends_triage(self.clock)
                self.event_queues.append({"event":e,"patient":p,"personel":triage})
                triage.set_occupied()
                p.event_list.append("Entered Triage at " + str(self.clock))
                
                self.report.increase_usage_area(triage,self.clock,0)
            else:
                self.wait_queues["triage_queue"].append({"patient":p,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                p.event_list.append("Waiting for Triage at " + str(self.clock))

        else:
            p.event_list.append("Arrived by foot at " + str(self.clock))
            p.set_not_brought_by_ambulance()
            admission = self.get_available(self.admission_personel)
            if admission:
                e = Event(self.settings)
                e.scale_patient_ends_admission(self.clock)
                self.event_queues.append({"event":e,"patient":p,"personel":admission})
                p.event_list.append("Entered Admission at " + str(self.clock))
                admission.set_occupied()

                self.report.increase_usage_area(admission,self.clock,0)
            else:
                self.wait_queues["admission_queue"].append({"patient":p,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                p.event_list.append("Waiting for Admission at " + str(self.clock))
    
        e = Event(self.settings)
        e.scale_patient_arrives(self.clock)
        self.event_queues.append({"event":e,"patient":None, "personel":None})

    def admission_event_routine(self, patient, personel):
        patient.event_list.append("Ended Admission at " + str(self.clock))
        personel.set_free()

        triage = self.get_available(self.triage_personel)
        if triage:
            e = Event(self.settings)
            e.scale_patient_ends_triage(self.clock)
            self.event_queues.append({"event":e,"patient":patient,"personel":triage})
            triage.set_occupied()
            patient.event_list.append("Entered Triage at " + str(self.clock))
                
            self.report.increase_usage_area(triage,self.clock,0)
        else:
            self.wait_queues["triage_queue"].append({"patient":patient,"time_of_arrival":self.clock})
            self.num_global_patients_delays += 1
            patient.event_list.append("Waiting for Triage at " + str(self.clock))

        next_patient = self.get_next_patient_from_queue("admission_queue",patient)
        if next_patient != None:
            e = Event(self.settings)
            e.scale_patient_ends_admission(self.clock)
            self.event_queues.append({"event":e,"patient":next_patient,"personel":personel})
            self.remove_patient_from_queue("admission_queue",next_patient)
            personel.set_occupied()
        

    def triage_event_routine(self,patient,urgency_distribution,limits,personel):
        personel.set_free()

        if urgency_distribution == limits[3]:
            patient.set_red_armband()
        elif urgency_distribution == limits[1]:
            patient.set_yellow_armband()
        elif urgency_distribution == limits[2]:
            patient.set_orange_armband()
        else:
           patient.set_green_armband()
        
        patient.event_list.append("Ended Triage at " + str(self.clock) + ". Got a " + str(patient.get_armband_color()))
        e = Event(self.settings)
        e.event_type = Event_type.PATIENT_ENDS_TRIAGE
        next_event = e.next_event()
        if next_event == Event_type.PATIENT_ENDS_CARDIOLOGY:
            cardiologist = self.get_available(self.cardiologists)
            patient.speciality_origin=Speciality.CARDIOLOGIST
            if cardiologist:
                e.scale_patient_ends_cardiology(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":cardiologist})
                cardiologist.set_occupied()
                patient.event_list.append("Entered Cardiology at " + str(self.clock))
                
                self.report.increase_usage_area(cardiologist,self.clock,0)
            else:
                self.wait_queues["cardiologist_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Cardiology at " + str(self.clock))
        
        if next_event == Event_type.PATIENT_ENDS_GENERAL_OFFICE:
            general_practitioner = self.get_available(self.general_practitioners)
            patient.speciality_origin=Speciality.GENERAL_PRATICTIONER
            if general_practitioner:
                e.scale_patient_ends_general_office(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":general_practitioner})
                general_practitioner.set_occupied()
                patient.event_list.append("Entered General Office at " + str(self.clock))
                
                self.report.increase_usage_area(general_practitioner,self.clock,0)
            else:
                self.wait_queues["general_practitioner_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for General Office at " + str(self.clock))
        
        if next_event == Event_type.PATIENT_ENDS_ORTHOPEDY:
            orthopedist = self.get_available(self.orthopedists)
            patient.speciality_origin=Speciality.ORTHOPEDIST
            if orthopedist:
                e.scale_patient_ends_orthopedy(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":orthopedist})
                orthopedist.set_occupied()
                patient.event_list.append("Entered Orthopedist at " + str(self.clock))
                
                self.report.increase_usage_area(orthopedist,self.clock,0)
            else:
                self.wait_queues["orthopedist_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Orthopedist at " + str(self.clock))

        if next_event == Event_type.PATIENT_ENDS_PULOMONLOGY:
            pulmonologist = self.get_available(self.pulmonologists)
            patient.speciality_origin=Speciality.PULMONOLOGIST
            if pulmonologist:
                e.scale_patient_ends_pulmonology(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":pulmonologist})
                pulmonologist.set_occupied()
                patient.event_list.append("Entered Pneumologist at " + str(self.clock))
                
                self.report.increase_usage_area(pulmonologist,self.clock,0)
            else:
                self.wait_queues["pulmonologist_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Pneumologist at " + str(self.clock))

        next_patient = self.get_next_patient_from_queue("triage_queue",patient)

        if next_patient is not None:
            e = Event(self.settings)
            e.scale_patient_ends_triage(self.clock)
            self.event_queues.append({"event":e,"patient":next_patient,"personel":personel})
            personel.set_occupied()
            self.remove_patient_from_queue("triage_queue",next_patient)

    def speciality_event_routine(self,patient, personel):
        personel.set_free()

        e = Event(self.settings)
        #check current personnel speciality
        if patient.speciality_origin == Speciality.GENERAL_PRATICTIONER:
                patient.event_list.append("Ended General Office at " + str(self.clock))
                e.event_type = Event_type.PATIENT_ENDS_GENERAL_OFFICE

        if patient.speciality_origin ==  Speciality.CARDIOLOGIST:
                patient.event_list.append("Ended Cardiologist at " + str(self.clock))
                e.event_type = Event_type.PATIENT_ENDS_CARDIOLOGY

        if patient.speciality_origin == Speciality.ORTHOPEDIST:
                patient.event_list.append("Ended Orthopedist at " + str(self.clock))
                e.event_type = Event_type.PATIENT_ENDS_ORTHOPEDY

        if patient.speciality_origin == Speciality.PULMONOLOGIST:
                patient.event_list.append("Ended Pulmonologist at " + str(self.clock))
                e.event_type = Event_type.PATIENT_ENDS_PULOMONLOGY
                
        next_event = e.next_event()

        if next_event == Event_type.PATIENT_ENDS_X_RAY and patient.has_been_in_xray==False:
            x_ray_specialist = self.get_available(self.x_ray_specialists)
            if x_ray_specialist:
                e.scale_patient_ends_xray(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":x_ray_specialist})
                x_ray_specialist.set_occupied()
                patient.event_list.append("Entered X-Ray at " + str(self.clock))
                
                self.report.increase_usage_area(x_ray_specialist,self.clock,0)
            else:
                self.wait_queues["x_ray_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for X-Ray at " + str(self.clock))

        if next_event == Event_type.PATIENT_ENDS_DISMISSION or patient.has_been_in_xray==True:
            dismission = self.get_available(self.dismission_personel)
            if dismission:
                e.scale_patient_ends_dismission(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":dismission})
                patient.event_list.append("Entered Dismission at " + str(self.clock))
                dismission.set_occupied()
                
                self.report.increase_usage_area(dismission,self.clock,0)
            else:
                self.wait_queues["dismission_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Dismission at " + str(self.clock))
            

        e_next = Event(self.settings)
        next_patient = self.get_next_patient_from_queue("",patient)
        if next_patient != None:
            if patient.speciality_origin == Speciality.GENERAL_PRATICTIONER:
                e_next.scale_patient_ends_general_office(self.clock)

            if patient.speciality_origin ==  Speciality.CARDIOLOGIST:
                e_next.scale_patient_ends_cardiology(self.clock)

            if patient.speciality_origin == Speciality.ORTHOPEDIST:
                e_next.scale_patient_ends_orthopedy(self.clock)

            if patient.speciality_origin == Speciality.PULMONOLOGIST:
                e_next.scale_patient_ends_pulmonology(self.clock)

            self.event_queues.append({"event":e_next,"patient":next_patient,"personel":personel})
            self.remove_patient_from_queue("",next_patient)
            personel.set_occupied()

    def xray_event_routine(self,patient, personel):
        personel.set_free()
        patient.event_list.append("Ended X-Ray at " + str(self.clock))
        patient.has_been_in_xray = True

        speciality_origin = patient.speciality_origin
        e = Event(self.settings)
        if speciality_origin == Speciality.GENERAL_PRATICTIONER:
            general_practitioner = self.get_available(self.general_practitioners)
            if general_practitioner:
                e.scale_patient_ends_general_office(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":general_practitioner})
                general_practitioner.set_occupied()
                patient.event_list.append("Entered General Office at " + str(self.clock))
                
                self.report.increase_usage_area(general_practitioner,self.clock,0)
            else:
                self.wait_queues["general_practitioner_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for General Office at " + str(self.clock))

        if speciality_origin ==  Speciality.CARDIOLOGIST:
            cardiologist = self.get_available(self.cardiologists)
            if cardiologist:
                e.scale_patient_ends_cardiology(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":cardiologist})
                patient.event_list.append("Entered Cardiologist at " + str(self.clock))
                cardiologist.set_occupied()
                
                self.report.increase_usage_area(cardiologist,self.clock,0)
            else:
                self.wait_queues["cardiologist_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Cardiologist at " + str(self.clock))

        if speciality_origin == Speciality.ORTHOPEDIST:
            orthopedist = self.get_available(self.orthopedists)
            if orthopedist:
                e.scale_patient_ends_orthopedy(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":orthopedist})
                orthopedist.set_occupied()
                patient.event_list.append("Entered Orthopedist at " + str(self.clock))
                
                self.report.increase_usage_area(orthopedist,self.clock,0)
            else:
                self.wait_queues["orthopedist_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Orthopedist at " + str(self.clock))

        if speciality_origin == Speciality.PULMONOLOGIST:
            pulmonologist = self.get_available(self.pulmonologists)
            if pulmonologist:
                e.scale_patient_ends_pulmonology(self.clock)
                self.event_queues.append({"event":e,"patient":patient,"personel":pulmonologist})
                pulmonologist.set_occupied()
                patient.event_list.append("Entered Pulmonologist at " + str(self.clock))
                
                self.report.increase_usage_area(pulmonologist,self.clock,0)
            else:
                self.wait_queues["pulmonologist_queue"].append({"patient":patient,"time_of_arrival":self.clock})
                self.num_global_patients_delays += 1
                patient.event_list.append("Waiting for Pulmonologist at " + str(self.clock))

        next_patient = self.get_next_patient_from_queue("x_ray_queue",patient)
        if next_patient != None:
            e = Event(self.settings)
            e.scale_patient_ends_xray(self.clock)
            self.event_queues.append({"event":e,"patient":next_patient,"personel":personel})
            personel.set_occupied()
            self.remove_patient_from_queue("x_ray_queue",next_patient)


    def dismission_event_routine(self,patient, personel):
        patient.event_list.append("Patient " + str(patient.id) + " ended Dismission at " + str(self.clock))
        personel.set_free()
        print("patient " + str(patient.id) + " :")
        patient.print_workflow()
        print("")
        # TODO Destroy patient
        #print ("removed patient with " + str(res))
        next_patient = self.get_next_patient_from_queue("dismission_queue", patient)
        if next_patient != None:
            e = Event(self.settings)
            e.scale_patient_ends_dismission(self.clock)
            self.event_queues.append({"event":e,"patient":next_patient,"personel":personel})
            personel.set_occupied()
            self.remove_patient_from_queue("dismission_queue",next_patient)


    # Event Routine Methods  
    def advance_time_routine(self):
        next_events = None

        min_clock = None
        for x in self.event_queues:
            if x["event"].time_of_occurence>self.clock:
                if min_clock==None or min_clock>x["event"].time_of_occurence:
                    min_clock = x["event"].time_of_occurence

        next_events = [item for item in self.event_queues if item['event'].time_of_occurence == min_clock]
        if len(next_events)==0:
            return False
        #advance clock to the next event
        self.clock = min_clock

        for next_event in next_events:
            # execute event routines

            
            #report update
            if next_event["event"].event_type != Event_type.PATIENT_ARRIVES:
                self.report.increase_usage_area(next_event["personel"],self.clock,1)

            if next_event["event"].event_type == Event_type.PATIENT_ARRIVES:
                if self.clock < self.max_clock:
                    self.num_patients_received+=1
                    ambulance_arrival = np.random.binomial(n=1, p= 0.5)
                    ambulance_limit = 1
                    self.arrival_event_routine(ambulance_arrival,ambulance_limit)

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_ADMISSION:
                self.admission_event_routine(next_event["patient"],next_event["personel"])

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_TRIAGE:
                armband_lambda = self.settings.armband_setting
                armband_color_number = np.random.poisson(lam=armband_lambda)
                self.triage_event_routine(next_event["patient"],armband_color_number,[1,2,3,4],next_event["personel"])
                #TODO METER DISTRIBUICAO DAS PULSEIRAS

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_ORTHOPEDY:
                self.speciality_event_routine(next_event["patient"],next_event["personel"])

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_GENERAL_OFFICE:
                self.speciality_event_routine(next_event["patient"],next_event["personel"])

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_CARDIOLOGY:
                self.speciality_event_routine(next_event["patient"],next_event["personel"])

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_PULOMONLOGY:
                self.speciality_event_routine(next_event["patient"],next_event["personel"])
            
            if next_event["event"].event_type == Event_type.PATIENT_ENDS_X_RAY:
                self.xray_event_routine(next_event["patient"],next_event["personel"])

            if next_event["event"].event_type == Event_type.PATIENT_ENDS_DISMISSION:
                self.dismission_event_routine(next_event["patient"],next_event["personel"])


        return True

    # auxiliary queues methods
    
    def get_next_patient_from_queue(self,queue_type,patient):
        if queue_type=="":
            if patient.speciality_origin == Speciality.GENERAL_PRATICTIONER:
                queue_type = "general_practitioner_queue"

            if patient.speciality_origin ==  Speciality.CARDIOLOGIST:
                queue_type = "cardiologist_queue"

            if patient.speciality_origin == Speciality.ORTHOPEDIST:
                queue_type = "orthopedist_queue"

            if patient.speciality_origin == Speciality.PULMONOLOGIST:
                queue_type = "pulmonologist_queue"

        colors_time_limits = {Emergency_Color.GREEN:65,Emergency_Color.YELLOW:40,Emergency_Color.ORANGE:25,Emergency_Color.RED:15}

        next_patient = None
        current_time_of_arrival = None
        
        # check the patients that have surpasses the limit waiting times
        for item in self.wait_queues[queue_type]:
            time_waiting = self.clock - item["time_of_arrival"]
            # if the patient has been waiting longer that it should
            if queue_type != "admission_queue" and queue_type != "triage_queue" and queue_type != "":
                if time_waiting>colors_time_limits[item["patient"].get_armband_color()]:
                    if next_patient==None:
                        next_patient = item["patient"]
                    else:
                        #if the patient has a higher priority wraist that the previous selected one
                        if next_patient.get_armband_color().value<item["patient"].get_armband_color().value:
                            next_patient = item["patient"]
        
        # report log
        if next_patient is not None and  queue_type != "admission_queue" and queue_type != "triage_queue" and queue_type != "dismission_queue" :
            self.report.increase_timeout_armband_by_location(queue_type,next_patient.get_armband_color())
        
        # No patients have surpassed the limit waiting time
        current_time_of_arrival = None
        if next_patient == None:
            for item in self.wait_queues[queue_type]:
                if next_patient==None:
                    next_patient = item["patient"]
                    current_time_of_arrival = item["time_of_arrival"]
                else:
                    # if the patient has a higher priority waist
                    if next_patient.get_armband_color() is not None and item["patient"].get_armband_color() is not None:
                        if next_patient.get_armband_color().value<item["patient"].get_armband_color().value:
                            next_patient = item["patient"]
                            current_time_of_arrival = item["time_of_arrival"]

                        else:
                            # is the waist is the same
                            if next_patient.get_armband_color()==item["patient"].get_armband_color():
                                #if the patient has been waiting longer that the previous selected one
                                if current_time_of_arrival<item["time_of_arrival"]:
                                    next_patient = item["patient"]
                                    current_time_of_arrival = item["time_of_arrival"]
                    else:
                        #if the patient has been waiting longer that the previous selected one
                        if current_time_of_arrival<item["time_of_arrival"]:
                            next_patient = item["patient"]
                            current_time_of_arrival = item["time_of_arrival"]

        return next_patient
                           
    def remove_patient_from_queue(self,queue_type,patient):
        if queue_type=="":
            if patient.speciality_origin == Speciality.GENERAL_PRATICTIONER:
                queue_type = "general_practitioner_queue"

            if patient.speciality_origin ==  Speciality.CARDIOLOGIST:
                queue_type = "cardiologist_queue"

            if patient.speciality_origin == Speciality.ORTHOPEDIST:
                queue_type = "orthopedist_queue"

            if patient.speciality_origin == Speciality.PULMONOLOGIST:
                queue_type = "pulmonologist_queue"
        
        if queue_type=="":
            pass

        try:
            if len(self.wait_queues[queue_type])>0:
                for item in self.wait_queues[queue_type]:
                    if item["patient"].id==patient.id:
                        self.wait_queues[queue_type].remove(item)
            return True
        except:
            return False
                
    def change_personel_state(self,personel_list,id):
        for personel in personel_list:
            if personel.identification == id:
                personel.is_available = not personel.is_available

    def run(self):
        while self.advance_time_routine():
            pass
        print("num patients: " + str(self.num_patients_received))
        print("num patients delayed: " + str(self.num_global_patients_delays))

        self.report.print_report(self.clock)


  

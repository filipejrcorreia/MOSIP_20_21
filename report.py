from entity import Emergency_Color
class Report:
    def __init__(self):
        self.x = 0
        self.timeout_armband_by_location = {"general_practitioner_queue":{Emergency_Color.GREEN:0,Emergency_Color.YELLOW:0,Emergency_Color.ORANGE:0,Emergency_Color.RED:0}
        ,"cardiologist_queue":{Emergency_Color.GREEN:0,Emergency_Color.YELLOW:0,Emergency_Color.ORANGE:0,Emergency_Color.RED:0}
        ,"orthopedist_queue":{Emergency_Color.GREEN:0,Emergency_Color.YELLOW:0,Emergency_Color.ORANGE:0,Emergency_Color.RED:0}
        ,"pulmonologist_queue":{Emergency_Color.GREEN:0,Emergency_Color.YELLOW:0,Emergency_Color.ORANGE:0,Emergency_Color.RED:0}
        ,"x_ray_queue":{Emergency_Color.GREEN:0,Emergency_Color.YELLOW:0,Emergency_Color.ORANGE:0,Emergency_Color.RED:0}}

        self.usage_stats=[]

    def generate_report(self):
        return 0

    def setup_usage_stats(self,personel_list,speciality):
        for personel in personel_list:
            self.usage_stats.append({"id":personel.identification,"speciality":speciality,"time_since_last_event":0,"cumulative_usage_area":0})

    def increase_timeout_armband_by_location(self,location,armband_color):
        (self.timeout_armband_by_location[location])[armband_color]+=1
    
    def increase_usage_area(self,personel,current_time,status):
        for stat in self.usage_stats:
            if stat["id"]==personel.identification:
                stat["cumulative_usage_area"]+=((current_time-stat["time_since_last_event"])*status)
                stat["time_since_last_event"] = current_time
    
    def print_report(self,simulation_time):
        print("######### STATS REPORT #########")
        print("Armband timeout by queue (queue|color|qty)")
        print("General Practitioner|GREEN|"+str((self.timeout_armband_by_location["general_practitioner_queue"])[Emergency_Color.GREEN]))
        print("General Practitioner|YELLOW|"+str((self.timeout_armband_by_location["general_practitioner_queue"])[Emergency_Color.YELLOW]))
        print("General Practitioner|ORANGE|"+str((self.timeout_armband_by_location["general_practitioner_queue"])[Emergency_Color.ORANGE]))
        print("General Practitioner|RED|"+str((self.timeout_armband_by_location["general_practitioner_queue"])[Emergency_Color.RED]))
        
        print("Cardiologist|GREEN|"+str((self.timeout_armband_by_location["cardiologist_queue"])[Emergency_Color.GREEN]))
        print("Cardiologist|YELLOW|"+str((self.timeout_armband_by_location["cardiologist_queue"])[Emergency_Color.YELLOW]))
        print("Cardiologist|ORANGE|"+str((self.timeout_armband_by_location["cardiologist_queue"])[Emergency_Color.ORANGE]))
        print("Cardiologist|RED|"+str((self.timeout_armband_by_location["cardiologist_queue"])[Emergency_Color.RED]))

        print("Orthopedist|GREEN|"+str((self.timeout_armband_by_location["orthopedist_queue"])[Emergency_Color.GREEN]))
        print("Orthopedist|YELLOW|"+str((self.timeout_armband_by_location["orthopedist_queue"])[Emergency_Color.YELLOW]))
        print("Orthopedist|ORANGE|"+str((self.timeout_armband_by_location["orthopedist_queue"])[Emergency_Color.ORANGE]))
        print("Orthopedist|RED|"+str((self.timeout_armband_by_location["orthopedist_queue"])[Emergency_Color.RED]))

        print("Pulmonologist|GREEN|"+str((self.timeout_armband_by_location["pulmonologist_queue"])[Emergency_Color.GREEN]))
        print("Pulmonologist|YELLOW|"+str((self.timeout_armband_by_location["pulmonologist_queue"])[Emergency_Color.YELLOW]))
        print("Pulmonologist|ORANGE|"+str((self.timeout_armband_by_location["pulmonologist_queue"])[Emergency_Color.ORANGE]))
        print("Pulmonologist|RED|"+str((self.timeout_armband_by_location["pulmonologist_queue"])[Emergency_Color.RED]))

        print("\nUsage stats by personnel:")
        for stat in self.usage_stats:
            print(str(stat["id"]) + "("+str(stat["speciality"])+")|"+str(stat["cumulative_usage_area"])+"|"+str(-(-((stat["cumulative_usage_area"]*100)/simulation_time)//.01) * .01)+"%")

class StatisticUpdateRoutine(Report):

    def __init__(self):
        Report.__init__(self)

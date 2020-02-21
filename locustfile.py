import resource
import random
import urllib3

from locust import HttpLocust, TaskSet, task, between
import yaml

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
resource.setrlimit(resource.RLIMIT_NOFILE, (10240, 9223372036854775807))

# Load config file
with open('config.yaml', 'r') as config_file:
    try:
        config = yaml.load(config_file)
        api_base_url = config['api_base_url']
        auth = (config['user'], config['password'])
        multiple_courses = config['multiple_courses']
        multiple_majors = config['multiple_majors']
        balance_due = config['balance_due']
        student_employee = config['student_employee']
        with_holds = config['with_holds']
        financial_aid = config['financial_aid']
        bend_campus = config['bend_campus']
        international = config['international']
    except yaml.YAMLError as error:
        exit(error)


class UserBehavior(TaskSet):
    @task(3)
    def get_academic_status_by_osuId_id(self):
        osu_id = random.choice(multiple_courses + multiple_majors)
        url = f'{api_base_url}/{osu_id}/academic-status'
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_account_balance_by_osuId_id(self):
        osu_id = random.choice(balance_due)
        url = f'{api_base_url}/{osu_id}/account-balance'
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_account_transactions_by_osuId_id(self):
        osu_id = random.choice(balance_due + financial_aid)
        url = f'{api_base_url}/{osu_id}/account-transactions'
        self.client.get(url, verify=False, auth=auth)

    @task(3)
    def get_class_schedule_by_osuId_id(self):
        osu_id = random.choice(multiple_courses + multiple_majors)
        url = f'{api_base_url}/{osu_id}/class-schedule'
        self.client.get(url, verify=False, auth=auth)

    @task(2)
    def get_degrees_by_osuId_id(self):
        osu_id = random.choice(multiple_courses + multiple_majors)
        url = f'{api_base_url}/{osu_id}/degrees'
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_dual_enrollment_by_osuId_id(self):
        osu_id = random.choice(bend_campus + international)
        url = f'{api_base_url}/{osu_id}/dual-enrollment'
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_emergency_contacts_by_osuId_id(self):
        osu_id = random.choice(multiple_courses + international)
        url = f'{api_base_url}/{osu_id}/emergency-contacts'
        self.client.get(url, verify=False, auth=auth)

    @task(3)
    def get_gpa_by_osuId_id(self):
        osu_id = random.choice(multiple_courses + multiple_majors)
        url = f'{api_base_url}/{osu_id}/gpa'
        self.client.get(url, verify=False, auth=auth)

    @task(3)
    def get_grades_by_osuId_id(self):
        osu_id = random.choice(multiple_courses + multiple_majors)
        url = f'{api_base_url}/{osu_id}/grades'
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_holds_by_osuId_id(self):
        osu_id = random.choice(with_holds)
        url = f'{api_base_url}/{osu_id}/holds'
        self.client.get(url, verify=False, auth=auth)

    @task(1)
    def get_work_study_by_osuId_id(self):
        osu_id = random.choice(student_employee)
        url = f'{api_base_url}/{osu_id}/work-study'
        self.client.get(url, verify=False, auth=auth)


class ApiUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(0.100, 5)

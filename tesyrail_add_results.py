from testrail import *
from datetime import datetime


add_result = {
    'assignedto_id': None,
    'comment': None,
    'custom_baseline_stdev': None,
    'custom_baseline_throughput': None,
    'custom_launchpad_bug': None,
    'custom_stdev': None,
    'custom_test_case_steps_results': [{
        'actual': '',
        'content': '',
        'expected': ''
    }],
    'custom_throughput': None,
    'defects': None,
    'elapsed': None,
    'status_id': None,
    'version': None
}
client = APIClient('https://mirantis.testrail.com')

class Base():

    def __init__(self):
        self.client = APIClient('https://mirantis.testrail.com')
        self.client.user = ''
        self.client.password = ''

    def get_plans(self, project_id):#!
        return self.client.send_get('get_plans/{0}'.format(project_id))

    def get_plan(self, plan_id):#!
        return self.client.send_get('get_plan/{0}'.format(plan_id))

    def get_tests(self, plan_id):#!
        return self.client.send_get('get_tests/{0}'.format(plan_id))

    def get_tempest_runs(self, plan_id):
        all_run = self.get_plan(plan_id)#!get_plans
        tempest_runs = []
        for run in all_run['entries']:
            if 'Tempest 9.0' in run['name']:
                tempest_runs.append(run)
        return tempest_runs

    def get_id_of_tempest_runs(self, tempest_runs):
        tempest_runs_ids = {}#[]
        for i in tempest_runs:
            for item in i['runs']:
                tempest_runs_ids.update({item['id']:item['name']})#append(item['id']:item['name'])
        return tempest_runs_ids

    def get_id_of_failed_tests(self, tempest_run_id):#!
        all_tests = self.get_tests(tempest_run_id)
        test_ids = []
        for test in all_tests:
            if test['status_id'] == 5:
                test_ids.append(test['id'])
        return test_ids

    def get_test_result(self, test_id):
        return self.client.send_get('get_results/{0}'.format(test_id))

    def get_test_results_for_run(self, run_id):
        return self.client.send_get('get_results_for_run/{0}'.format(run_id))

    def get_results_for_case(self, run_id, case_id):
        return self.client.send_get('get_results_for_case/{0}/{1}'.format(run_id, case_id))

    def get_test(self, test_id):
        return self.client.send_get('get_test/{0}'.format(test_id))

    def get_runs(self, run_id):
        return self.client.send_get('get_runs/{0}'.format(run_id))

    def get_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def add_result(self,test_id , result_to_add):
        return self.client.send_post('add_result/{0}'.format(test_id['id']), result_to_add)

    def get_plan_with_tempest(self):#!
        get_plans = self.get_plans(3)
        for plans in get_plans:
            if plans.get(u'passed_count') > 1000:
                get_plan = self.get_plan(str(plans.get(u'id')))

    def get_link_on_bugs(self, test_port):
        get_plans = self.get_plans(3)
        for plans in get_plans:
            if plans.get(u'passed_count') > 1000:
                get_plan = self.get_plan(str(plans.get(u'id')))
                for plan in get_plan['entries']:
                    plan = plan['runs'][0]
                    if 'Tempest' in plan['name']:
                        send_get_tests = 'get_tests/' + str(plan[u'id'])
                        get_tests = self.client.send_get(send_get_tests)
                        for test in get_tests:

                            if test[u'title'] == test_port \
                                    and test[u'status_id'] == 8:
                                send_get_results = 'get_results/' + str(
                                    test[u'id'])
                                get_results = client.send_get(send_get_results)
                                return get_results[0][u'custom_launchpad_bug']
        return 0

plans = 11200

call = Base()

get_plan = call.get_plan(plans)

now = str(datetime.now())
now = now.split('.')[0]
file = open(now + ' add_bug_result ' + get_plan[u'name'] + ".txt", "w")
print get_plan[u'name']
file.write("\n " + get_plan[u'name'] + '\n')
tempest_runs = call.get_tempest_runs(plans)
id_of_tempest_runs = call.get_id_of_tempest_runs(tempest_runs)
for id_run in id_of_tempest_runs:
    print
    print id_of_tempest_runs.get(id_run), id_run
    file.write('\n ' + str(id_of_tempest_runs.get(id_run)) + str(id_run) + '\n')
    get_tests = call.get_tests(id_run)
    for test in get_tests:
        if test[u'status_id'] == 5:
            launchpad_bug = call.get_link_on_bugs(test[u'title'])
            #print launchpad_bug
            print test[u'title'], test['id']
            file.write(str(test[u'title']) + str(test['id']) + '\n')
            if launchpad_bug == 0:
                print "This test is failed at first"
                file.write("This test is failed at first" + '\n')
            else:
                add_result['status_id'] = 8
                add_result['custom_launchpad_bug'] = launchpad_bug
                send_add_result = 'add_result/' + str(test['id'])
                #result = client.send_post(send_add_result, add_result)
                #print result
                #file.write(str(result) + '\n')

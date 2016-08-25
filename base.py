from testrail import *

class Base():

    def __init__(self):
        self.client = APIClient('https://mirantis.testrail.com')
        self.client.user = ''
        self.client.password = ''

    def send_post_add_result (self, id, bug, status_id, add_result):
        add_result['status_id'] = status_id
        add_result['custom_launchpad_bug'] = bug
        send_add_result = 'add_result/' + str(id)
        return self.client.send_post(send_add_result, add_result)

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
            if 'Tempest' in run['name']:
                tempest_runs.append(run)
        return tempest_runs

    def get_id_of_tempest_runs(self, tempest_runs):
        tempest_runs_ids = {}#[]
        for i in tempest_runs:
            for item in i['runs']:
                tempest_runs_ids.update({item['id']:item['name']})
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
        return self.client.send_get('get_results_for_case/{0}/{1}'.
                                    format(run_id, case_id))

    def get_test(self, test_id):
        return self.client.send_get('get_test/{0}'.format(test_id))

    def get_runs(self, run_id):
        return self.client.send_get('get_runs/{0}'.format(run_id))

    def get_run(self, run_id):
        return self.client.send_get('get_run/{0}'.format(run_id))

    def get_last_tempest_run(self, get_plans):
        for plans in get_plans:
            # print dict
            if (plans.get(u'passed_count') > 1000 or plans.get(
                    u'blocked_count') > 1000 )and '9.1' in plans.get(u'name'):
                return plans.get(u'id')

    def add_result(self,test_id , result_to_add):
        return self.client.send_post('add_result/{0}'.format(test_id['id']),
                                     result_to_add)

    def get_plan_with_tempest(self):#!
        get_plans = self.get_plans(3)
        for plans in get_plans:
            if plans.get(u'passed_count') > 1000:
                get_plan = self.get_plan(str(plans.get(u'id')))

    def get_info_about_bugs(self, description):
        get_plans = self.get_plans(3)
        for plans in get_plans:
            if plans.get(u'passed_count') > 1000 and '9.1' in plans.get(u'name'):
                get_plan = self.get_plan(str(plans.get(u'id')))
                for plan in get_plan['entries']:
                    plan = plan['runs'][0]
                    if 'Tempest' in plan['name']:
                        send_get_tests = 'get_tests/' + str(plan[u'id'])
                        get_tests = self.client.send_get(send_get_tests)
                        for test in get_tests:
                            if test['custom_test_case_description'] == description \
                                    and (len( self.get_test_result (test[u'id']))) > 1  \
                                    and (test[u'status_id'] == 8
                                     or test[ u'status_id'] == 9
                                     or test[u'status_id'] == 6):
                                send_get_results = 'get_results/' + str(
                                    test[u'id'])
                                get_results = self.client.send_get(
                                    send_get_results)
                                return test[u'status_id'], get_results[0][
                                    u'custom_launchpad_bug']
        return 0, 0

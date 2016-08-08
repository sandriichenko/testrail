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
                # print plans.get(u'id')
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


# i = [{u'assignedto_id': None, u'comment': None, u'custom_baseline_stdev': None, u'status_id': 6, u'custom_launchpad_bug': u'https://bugs.launchpad.net/mos/+bug/1442193', u'custom_stdev': None, u'created_by': 85, u'elapsed': None,
#       u'custom_baseline_throughput': None, u'created_on': 1470324528, u'version': None, u'custom_test_case_steps_results': [{u'content': u'', u'expected': u'', u'actual': u'', u'status_id': 3}], u'defects': None, u'custom_throughput': None,
#       u'test_id': 10696624, u'id': 24849666},
#      {u'assignedto_id': None, u'comment': None, u'custom_baseline_stdev': None, u'status_id': 8, u'custom_launchpad_bug': u'https://bugs.launchpad.net/mos/+bug/1442193', u'custom_stdev': None, u'created_by': 85,
#       u'elapsed': None, u'custom_baseline_throughput': None, u'created_on': 1470324505, u'version': None, u'custom_test_case_steps_results': [{u'content': u'', u'expected': u'', u'actual': u'', u'status_id': 3}],
#       u'defects': None, u'custom_throughput': None, u'test_id': 10696624, u'id': 24849664},
#      {u'assignedto_id': None, u'comment': u'test failed\n\nEnv: **Tempest-9.0_Ceph_DVR_Sahara_Ceilometer_Ironic**\n\n[Jenkins Job Result](http://cz7776.bud.mirantis.net:8080/jenkins/view/Tempest_9.%D0%A5/job/9.0_Tempest_Ceph_no_ssl/lastSuccessfulBuild/artifact/report.xmltestReport/tempest.api.orchestration.stacks.test_swift_resources/SwiftResourcesTestJSON/test_metadata_id_fda06135_6777_4594_aefa_0f6107169698_object_storage_/)\n\n\n[Trace, logs](http://paste.openstack.org/show/548088/)\n\n\n---\n\n**Trace:**\n\n    Traceback (most recent call last):\n\n      File "/home/rally/.rally/tempest/for-deployment-670f63eb-2e7f-4f4a-b48b-4c3466935722/tempest/test.py", line 273, in setUpClass\n\n        six.reraise(etype, value, trace)\n\n      File "/home/rally/.rally/tempest/for-deployment-670f63eb-2e7f-4f4a-b48b-4c3466935722/tempest/test.py", line 266, in setUpClass\n\n        cls.resource_setup()\n\n      File "/home/rally/.rally/tempest/for-deployment-670f63eb-2e7f-4f4a-b48b-4c3466935722/tempest/api/orchestration/stacks/test_swift_resources.py", line 56, in resource_setup\n\n        cls.client.wait_for_stack_status(cls.stack_id, \'CREATE_COMPLETE\')\n\n      File "/home/rally/.rally/tempest/for-deployment-670f63eb-2e7f-4f4a-b48b-4c3466935722/tempest/services/orchestration/json/orchestration_client.py", line 174, in wait_for_stack_status\n\n        stack_status_reason=body[\'stack_status_reason\'])\n\n    tempest.exceptions.StackBuildErrorException: Stack e76a2be1-1a30-47db-8c0c-0b86f8b49877 is in CREATE_FAILED status due to \'Resource CREATE failed: ClientException: resources.SwiftContainerWebsite: Container PUT failed: http://10.109.4.6:8080/swift/v1/tempest-heat-1732870417-SwiftContainerWebsite-a7spb2zwffpk 401 Unauthorized   AccessDenied\'\n\n',
#       u'custom_baseline_stdev': None, u'status_id': 5, u'custom_launchpad_bug': None, u'custom_stdev': None, u'created_by': 48, u'elapsed': u'', u'custom_baseline_throughput': None, u'created_on': 1470304543, u'version': None,
#       u'custom_test_case_steps_results': None, u'defects': None, u'custom_throughput': None, u'test_id': 10696624, u'id': 24835909}]
from base import *

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

if __name__ == '__main__':
    call = Base()
    get_plans = call.get_plans(3)
    # plans =17350 #16911
    plans = call.get_last_tempest_run(get_plans)
    tempest_runs = call.get_tempest_runs(plans)
    id_of_tempest_runs = call.get_id_of_tempest_runs(tempest_runs)
    for id_run in id_of_tempest_runs:
        get_tests = call.get_tests(id_run)
        if 'Ceph' in id_of_tempest_runs.get(id_run):
            print id_of_tempest_runs.get(id_run), id_run
            for test in get_tests:
                if test['status_id'] == 5 and test['custom_test_case_description'] == 'test_container_synchronization[id-ea4645a1-d147-4976-82f7-e5a7a3065f80,slow]':  #'test_container_synchronization':
                    result = call.send_post_add_result(test['id'], 'https://bugs.launchpad.net/mos/+bug/1591175', 8, add_result)
                    print result
                elif test['status_id'] == 5 and 'tempest.api.object_storage' in test['custom_test_group']:
                    result = call.send_post_add_result(test['id'], 'https://bugs.launchpad.net/mos/+bug/1442193', 6, add_result)
                    print result
        elif 'LVM' in id_of_tempest_runs.get(id_run) or 'Separated_Components' in id_of_tempest_runs.get(id_run):
            print id_of_tempest_runs.get(id_run), id_run
            for test in get_tests:
                if test['status_id'] == 5 and test['custom_test_case_description'] == 'test_container_synchronization[id-ea4645a1-d147-4976-82f7-e5a7a3065f80,slow]': # test_web_listing_css[id-bc37ec94-43c8-4990-842e-0e5e02fc8926]
                    result = call.send_post_add_result(test['id'], 'https://bugs.launchpad.net/mos/+bug/1591175', 8, add_result)
                    print result
                elif test['status_id'] == 5  and (test['custom_test_case_description'] == 'test_web_index[id-c1f055ab-621d-4a6a-831f-846fcb578b8b]'
                                                  or test['custom_test_case_description'] == 'test_web_listing_css[id-bc37ec94-43c8-4990-842e-0e5e02fc8926]'):
                    result = call.send_post_add_result(test['id'], 'https://bugs.launchpad.net/mos/+bug/1537071', 8, add_result)
                    print result
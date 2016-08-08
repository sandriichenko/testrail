from datetime import datetime
import logging
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


    plans =  17828


    call = Base()

    get_plan = call.get_plan(plans)

    time = str(datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S"))
    time = time + ' add_bug_result ' + get_plan[u'name'] + ".log"

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.DEBUG, filename=time)
    print get_plan[u'name']
    logging.info(get_plan[u'name'])
    tempest_runs = call.get_tempest_runs(plans)
    id_of_tempest_runs = call.get_id_of_tempest_runs(tempest_runs)
    for id_run in id_of_tempest_runs:
        print
        print id_of_tempest_runs.get(id_run), id_run
        logging.info(str(id_of_tempest_runs.get(id_run)) + str(id_run))
        get_tests = call.get_tests(id_run)
        for test in get_tests:
            # if test[u'status_id'] == 6 and (len( call.get_test_result (test[u'id']))) ==1 :# (len(get_results = call.get_test_result (test[u'id'] )) ==1 ):#test[u'status_id'] == 6 or test[u'status_id'] == 5 or test[u'status_id'] == 8
            #     #get_results = call.get_test_result (test[u'id'] )
            #     print test
            if test[u'status_id'] == 5 or \
                    (test[u'status_id'] == 6
                     and (len( call.get_test_result (test[u'id']))) ==1 ):#test[u'status_id'] == 6 or test[u'status_id'] == 9 or test[u'status_id'] == 8:
                status_id, bug_info = call.get_info_about_bugs(test['custom_test_case_description'])
                print test[u'title'], test['id']
                logging.info(str(test[u'title']) + str(test['id']))
                if status_id == 6 or status_id == 9 or status_id == 8:
                    add_result['status_id'] = status_id
                    add_result['custom_launchpad_bug'] = bug_info
                    send_add_result = 'add_result/' + str(test['id'])
                    print add_result['status_id'],  add_result['custom_launchpad_bug'], test['id'], test['custom_test_case_description']
                    result = call.client.send_post(send_add_result, add_result)
                    print result
                    logging.info(str(result))
                else:
                    print "This test is failed at first"
                    logging.info("This test is failed at first")


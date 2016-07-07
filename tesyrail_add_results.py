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


    plans = *****

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
            if test[u'status_id'] == 5:
                launchpad_bug = call.get_link_on_bugs(test[u'title'])
                print test[u'title'], test['id']
                logging.info(str(test[u'title']) + str(test['id']))
                if launchpad_bug == 0:
                    print "This test is failed at first"
                    logging.info("This test is failed at first")
                else:
                    add_result['status_id'] = 8
                    add_result['custom_launchpad_bug'] = launchpad_bug
                    send_add_result = 'add_result/' + str(test['id'])
                    result = call.client.send_post(send_add_result, add_result)
                    print result
                    logging.info(str(result))

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager

from collections import namedtuple

loader = DataLoader()

class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))

results_callback = ResultCallback()

# options = Options(connection='ssh', module_path=['./custom_ansible/action_plugins', './custom_ansible/library'], forks=500, become=None, become_method=None, become_user=None, check=False, diff=False)
Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
options = Options(connection='local', module_path=['/to/mymodules'], forks=10, become=None, become_method=None, become_user=None, check=False, diff=False)
passwords = dict(vault_pass='secret')

inventory = InventoryManager(loader=loader, sources=['production'])
variable_manager = VariableManager(loader=loader, inventory=inventory)

play_source = dict(
        name="get_some_PDU_data",
        hosts='pdus',
        gather_facts='no',
        tasks=[
            dict(action=dict(module='ping', args=dict(data='pong')), register='my_output'),
        ]
    )
play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

tqm = None
try:
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        # options=options,
        stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        # passwords={}
        passwords=passwords
    )
    tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()

# import ansible.runner
# import ansible.playbook
# from ansible import callbacks
# from ansible import utils
#
# stats = callbacks.AggregateStats()
# playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
# runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
#
#
# pb = ansible.playbook.PlayBook(
#     playbook="nseries.yml",
#     stats=stats,
#     callbacks=playbook_cb,
#     runner_callbacks=runner_cb,
#     check=True
# )
# for (play_ds, play_basedir) in zip(pb.playbook, pb.play_basedirs):
#     import ipdb
#     ipdb.set_trace()
#     # Can play around here to see what's going on.
#    
#
# pb.run()  # This runs the playbook

# from ansible.playbook import PlayBook
# pb = PlayBook(playbook='/path/to/book.yml')
# pb.run()

# TODO: Como sistema debo ejecutar un playbook desde python

# from ansible import playbook, callbacks

# uncomment the following to enable silent running on the playbook call
# this monkey-patches the display method on the callbacks module
# callbacks.display = lambda *a,**ka: None

# the meat of the meal.  run a playbook on a path with a hosts file and ssh key
# def run_playbook(playbook_path, hosts_path, key_file):
#     stats = callbacks.AggregateStats()
#     playbook_cb = callbacks.PlaybookCallbacks(verbose=0)
#     runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=0)
#     playbook.PlayBook(
#         playbook=playbook_path,
#         host_list=hosts_path,
#         stats=stats,
#         forks=4,
#         callbacks=playbook_cb,
#         runner_callbacks=runner_cb,
#         private_key_file=key_file
#         ).run()
#     return stats
#
#
# if __name__ == '__main__':
#     stats = run_playbook(
#         playbook_path='/SOME/PATH/book.yml',
#         hosts_path='/SOME/OTHER/PATH/ansible_hosts',
#         key_file='/OTHER/PATH/keys/id_rsa.pub'
#         )

    # print "PROC", stats.processed
    # print "FAIL", stats.failures
    # print "OK  ", stats.ok
    # print "DARK", stats.dark
    # print "CHGD", stats.changed
    # print "SKIP", stats.skipped


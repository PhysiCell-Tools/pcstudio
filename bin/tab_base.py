"""
tab_base.py - parent class of tabbed classes to share data and possibly methods.

Authors:
Randy Heiland (heiland@iu.edu)
Dr. Paul Macklin (macklinp@iu.edu)
Rf. Credits.md
"""

class TabBase():

    # def __init__(self, nanohub_flag, config_tab, run_tab, model3D_flag, tensor_flag, **kw):
    def __init__(self, **kw):
        # super().__init__()
        # global self.config_params
        # super(TabBase,self).__init__(**kw)

        self.update_rules_for_custom_data = True  # used by Rules tab

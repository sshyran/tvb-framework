# -*- coding: utf-8 -*-
#
#
# TheVirtualBrain-Framework Package. This package holds all Data Management, and 
# Web-UI helpful to run brain-simulations. To use it, you also need do download
# TheVirtualBrain-Scientific Package (for simulators). See content of the
# documentation-folder for more details. See also http://www.thevirtualbrain.org
#
# (c) 2012-2013, Baycrest Centre for Geriatric Care ("Baycrest")
#
# This program is free software; you can redistribute it and/or modify it under 
# the terms of the GNU General Public License version 2 as published by the Free
# Software Foundation. This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details. You should have received a copy of the GNU General 
# Public License along with this program; if not, you can download it here
# http://www.gnu.org/licenses/old-licenses/gpl-2.0
#
#
#   CITATION:
# When using The Virtual Brain for scientific publications, please cite it as follows:
#
#   Paula Sanz Leon, Stuart A. Knock, M. Marmaduke Woodman, Lia Domide,
#   Jochen Mersmann, Anthony R. McIntosh, Viktor Jirsa (2013)
#       The Virtual Brain: a simulator of primate brain network dynamics.
#   Frontiers in Neuroinformatics (7:10. doi: 10.3389/fninf.2013.00010)
#
#

"""
Entities transient and related to a Burst Configuration.

.. moduleauthor:: Bogdan Neacsa <bogdan.neacsa@codemart.ro>
"""

from copy import deepcopy
from datetime import datetime
from tvb.core.entities.storage import dao
from tvb.basic.logger.builder import get_logger
from tvb.basic.profile import TvbProfile

LOGGER = get_logger(__name__)


class BaseExportHelp(object):
    """
    Base class for all export helper entities. Wraps over a dictionary that is used
    to later convert entities to / from json.
    """
    KEY_VERSION = 'code_version'
    KEY_EXPORT_DATE = 'export_date'


    def __init__(self, input_data):
        input_data = input_data or {}

        # Export as part of the dictionary the current code version and the local time when the export happened.
        # The code version has the potential to be later used for validating compatibility, in case of version changes.
        if BaseExportHelp.KEY_VERSION not in input_data:
            input_data[BaseExportHelp.KEY_VERSION] = TvbProfile.current.version.CURRENT_VERSION
            input_data[BaseExportHelp.KEY_EXPORT_DATE] = datetime.now().strftime('%Y/%m/%d %H:%M')

        self._data_dict = input_data


    @property
    def data(self):
        """
        Property so you can easily access the dictionary as if it was a public attribute.
        """
        return self._data_dict



class BurstInformation(BaseExportHelp):
    """
    Helper entity that hold all the information needed to build a complete burst entity
    with all workflows, and workflow steps.
    """
    KEY_BI_WORKFLOWS = "--BI_workflows--"


    def __init__(self, data_dict):
        super(BurstInformation, self).__init__(data_dict)
        if self.KEY_BI_WORKFLOWS not in self._data_dict:
            self._data_dict[self.KEY_BI_WORKFLOWS] = []


    def add_workflow(self, workflow):
        """
        Append a WorkflowInformation entity to the list of workflows attached to this burst.
        """
        self._data_dict[self.KEY_BI_WORKFLOWS].append(workflow)


    def set_workflows(self, wf_list):
        """
        Set the entire list of workflows attached to this burst as WorkflowInformation entities.
        """
        self._data_dict[self.KEY_BI_WORKFLOWS] = wf_list


    def get_workflows(self):
        """
        Return a list of WorkflowInformation entities.
        """
        return self._data_dict[self.KEY_BI_WORKFLOWS]


    def to_dict(self):
        """
        Convert this entities to python dictionary ready to be dumped to json. Also make
        sure to recursively go through all the WorkflowInformation entities.
        Can later be used to rebuild the BurstInformation entity.
        """
        workflows = [wf.to_dict() for wf in self.get_workflows()]
        dict_data = deepcopy(self._data_dict)
        dict_data[self.KEY_BI_WORKFLOWS] = workflows
        return dict_data


    @staticmethod
    def load_from_dict(input_dict):
        """
        From a input dictionary try to rebuild a BurstInformation entity. The dictionary must have
        specific informations about the burst and it's constituent workflows. 
        Such a dictionary can be generated by calling 'to_dict' on existing BurstInformation.
        """
        LOGGER.debug("Loading BurstInformation from " + str(input_dict))
        workflows = [WorkflowInformation.load_from_dict(data)
                     for data in input_dict[BurstInformation.KEY_BI_WORKFLOWS]]
        input_dict[BurstInformation.KEY_BI_WORKFLOWS] = workflows
        return BurstInformation(input_dict)



class WorkflowInformation(BaseExportHelp):
    """
    Helper entity that hold all the information needed to build a complete workflow entity
    with all it's workflow steps.
    """
    KEY_WF_STEPS = '--WI_workflow_steps--'
    KEY_VIEW_STEPS = '--WI_view_steps--'


    def __init__(self, data_dict):
        super(WorkflowInformation, self).__init__(data_dict)
        if self.KEY_VIEW_STEPS not in self._data_dict:
            self._data_dict[self.KEY_VIEW_STEPS] = []
        if self.KEY_WF_STEPS not in self._data_dict:
            self._data_dict[self.KEY_WF_STEPS] = []


    def add_workflow_step(self, wf_step):
        """
        Append a WorkflowStepInformation entity to the list of steps for this workflow.
        """
        self._data_dict[self.KEY_WF_STEPS].append(wf_step)


    def add_view_step(self, view_step):
        """
        Append a WorkflowViewStepInformation entity to the list of view steps for this workflow.
        """
        self._data_dict[self.KEY_VIEW_STEPS].append(view_step)


    def set_workflow_steps(self, steps_list):
        """
        Set the list of steps for this workflow as WorkflowStepInformation entities.
        """
        self._data_dict[self.KEY_WF_STEPS] = steps_list


    def set_view_steps(self, steps_list):
        """
        Set the list of view steps for this workflow as WorkflowViewStepInformation entities.
        """
        self._data_dict[self.KEY_VIEW_STEPS] = steps_list


    def get_workflow_steps(self):
        """
        Return the list of steps for this workflow as WorkflowStepInformation entities.
        """
        return self._data_dict[self.KEY_WF_STEPS]


    def get_view_steps(self):
        """
        Return the list of view steps for this workflow as WorkflowViewStepInformation entities.
        """
        return self._data_dict[self.KEY_VIEW_STEPS]


    def to_dict(self):
        """
        Convert this entities to python dictionary ready to be dumped to json. Also make
        sure to recursively go through all the WorkflowStepInformation entities.
        Can later be used to rebuild the WorkflowInformation entity.
        """
        view_steps = [view_step.to_dict() for view_step in self.get_view_steps()]
        wf_steps = [wf_step.to_dict() for wf_step in self.get_workflow_steps()]
        dict_data = deepcopy(self._data_dict)
        dict_data[self.KEY_VIEW_STEPS] = view_steps
        dict_data[self.KEY_WF_STEPS] = wf_steps
        return dict_data


    @staticmethod
    def load_from_dict(input_dict):
        """
        From a input dictionary try to rebuild a WorkflowInformation entity. The dictionary must have
        specific informations about the workflow and it's constituent workflow steps. 
        Such a dictionary can be generated by calling 'to_dict' on existing WorkflowInformation.
        """
        view_steps = [WorkflowViewStepInformation.load_from_dict(data)
                      for data in input_dict[WorkflowInformation.KEY_VIEW_STEPS]]
        wf_steps = [WorkflowStepInformation.load_from_dict(data)
                    for data in input_dict[WorkflowInformation.KEY_WF_STEPS]]
        input_dict[WorkflowInformation.KEY_VIEW_STEPS] = view_steps
        input_dict[WorkflowInformation.KEY_WF_STEPS] = wf_steps
        return WorkflowInformation(input_dict)



class StepInfo(BaseExportHelp):
    """
    Base class for workflow steps.
    """
    ALGO_INFO = '--WVSI_algorighm_info--'


    def __init__(self, data_dict):
        super(StepInfo, self).__init__(data_dict)


    def set_algorithm(self, algorithm):
        """
        Save required info about algorithm to quickly rebuild it.
        Recieves a model.Algorithm entity and makes sure to store just what is needed to
        later be able to re-create that entity (even if with different id).
        """
        self._data_dict[self.ALGO_INFO] = {'module': algorithm.module,
                                           'class': algorithm.classname}


    def get_algorithm(self):
        """
        Return the algorithm saved in this entity.
        Should be used only if previously an algorithm was saved on this entity by
        calling 'set_algorithm' method.
        """
        if self.ALGO_INFO not in self._data_dict:
            return None
        return dao.get_algorithm_by_module(self._data_dict[self.ALGO_INFO]['module'],
                                           self._data_dict[self.ALGO_INFO]['class'])


    def to_dict(self):
        """
        In case of workflow steps, the to_dict is simply returning it's data dictionary, since
        no other complex entities should be present in dictionary at this point.
        """
        return self._data_dict


    def index(self):
        """
        Returned a tuple of the form (tab_index, index_in_tab) that can uniquely identify a workflow
        step in the context of a given workflow. Used to remove the view step in case the algorithm
        for the workflow step no longer exists in project we are imported to.
        """
        return self._data_dict.get('tab_index', -1), self._data_dict.get('index_in_tab', -1)



class WorkflowViewStepInformation(StepInfo):
    """
    Helper entity that hold all the information needed to build a complete workflow step entity
    """
    PORTLET_IDENT = '--WSI_portlet_id--'


    def __init__(self, input_data):
        super(WorkflowViewStepInformation, self).__init__(input_data)


    def set_portlet(self, portlet):
        """
        Having as input a model.Portlet entity, store what is required in order to
        later recreate that entity even in 'id' from database differs.
        """
        self._data_dict[self.PORTLET_IDENT] = portlet.algorithm_identifier


    def get_portlet(self):
        """
        Return the portlet that was saved on this entity. Should only be called if 
        beforehand 'set_portlet' was called on this entity.
        """
        if self.PORTLET_IDENT not in self._data_dict:
            return None
        return dao.get_portlet_by_identifier(self._data_dict[self.PORTLET_IDENT])


    @staticmethod
    def load_from_dict(input_dict):
        """
        Just create a new WorkflowViewStepInformation entity with the given input dictionary.
        """
        return WorkflowViewStepInformation(input_dict)



class WorkflowStepInformation(StepInfo):
    """
    Helper entity that hold all the information needed to build a complete workflow view step entity
    """
    OP_GID = '--WVSI_operation_gid--'


    def __init__(self, input_data):
        super(WorkflowStepInformation, self).__init__(input_data)


    def set_operation(self, operation):
        """
        Having a model.Operation entity as input, store it's gid so we can later
        return it even if 'id' in db has changed.
        """
        self._data_dict[self.OP_GID] = operation.gid


    def get_operation_id(self):
        """
        Return the operation that was saved on this entity. Should only be called if 
        beforehand 'set_operation' was called on this entity.
        """
        if self.OP_GID not in self._data_dict:
            return None

        operation_gid = self._data_dict.get(self.OP_GID, None)
        operation = dao.get_operation_by_gid(operation_gid)

        if operation:
            return operation.id

        LOGGER.warning("When restoring Workflow Step %s, we could not find operation "
                       "for GID %s" % (self.get_algorithm().name, operation_gid))
        return None


    @staticmethod
    def load_from_dict(input_dict):
        """
        Just create a new WorkflowStepInformation entity with the given input dictionary.
        """
        return WorkflowStepInformation(input_dict)
    
    
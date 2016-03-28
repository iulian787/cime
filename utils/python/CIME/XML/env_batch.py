"""
Interface to the env_batch.xml file.  This class inherits from EnvBase
"""
from standard_module_setup import *

from env_base import EnvBase

logger = logging.getLogger(__name__)

class EnvBatch(EnvBase):

    def __init__(self, case_root=os.getcwd(), infile="env_batch.xml"):
        """
        initialize an object interface to file env_batch.xml in the case directory
        """
        EnvBase.__init__(self, case_root, infile)

    def set_value(self, item, value, subgroup=None, ignore_type=False):
        val = None
        # allow the user to set all instances of item if subgroup is not provided
        if subgroup is None:
            nodes = self.get_nodes("entry", {"id":item})
            for node in nodes:
                self._set_value(node, item, value, ignore_type)
                val = value
        else:
            nodes = self.get_nodes("job",{"name":subgroup})
            for node in nodes:
                vnode = self.get_optional_node("entry", {"id":item}, root=node)
                if vnode is not None:
                    val = EnvBase.set_value(self, vnode, value, ignore_type)

        return val

    def get_value(self, item, attribute={}, resolved=True, subgroup="run"):
        """
        Must default subgroup to something in order to provide single return value
        """
        value = None

        job_node = self.get_optional_node("job", {"name":subgroup})
        if job_node is not None:
            node = self.get_optional_node(item, attribute, root=job_node)
            if node is not None:
                value = self.get_resolved_value(node.text)

                # Return value as right type if we were able to fully resolve
                # otherwise, we have to leave as string.
                if "$" not in value:
                    type_str = self._get_type_info(node)
                    value = convert_to_type(value, type_str, item)

        return value

    def get_type_info(self, vid):
        nodes = self.get_nodes("entry",{"id":vid})
        type_info = None
        for node in nodes:
            new_type_info = self._get_type_info(node)
            if type_info is None:
                type_info = new_type_info
            else:
                expect( type_info == new_type_info,
                        "Inconsistent type_info for entry id=%s %s %s" % (vid, new_type_info, type_info))
        return type_info

    def get_jobs(self):
        result = []
        for node in self.get_nodes("job"):
            result.append(node.attrib["name"])

        return result

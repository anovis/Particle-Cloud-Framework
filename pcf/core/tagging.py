# Copyright 2018 Capital One Services, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pcf.core.particle import StatelessParticle


class Tagging(StatelessParticle):
    """


    """

    flavor = "tagging"

    def __init__(self, particle_definition):
        super(Tagging, self).__init__(particle_definition)
        self.tag_definition = particle_definition["tags"]

    def _validate_config(self):
        return isinstance(self.tag_definition, dict)



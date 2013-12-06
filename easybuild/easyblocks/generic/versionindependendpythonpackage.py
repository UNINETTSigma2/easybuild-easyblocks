##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing VSC-tools, implemented as an easyblock

@author: Kenneth Hoste, Jens Timmerman (Ghent University)
"""
import os

import easybuild.tools.environment as env
from easybuild.easyblocks.generic.pythonpackage import PythonPackage
from easybuild.tools.filetools import run_cmd


class EB_VersionIndependendPythonPackage(PythonPackage):
    """Support for building/installing python packages without requiring a specific python package."""

    def build_step(self):
        """No build procedure."""
        pass

    def prepare_step(self):
        """Set pylibdir"""
        self.pylibdir = 'lib'
        super(EB_VSC_minus_tools, self).prepare_step()

    def install_step(self):
        """Custom install procedure to skip selection of python package versions."""
        pylibdir = "%s/%s" % (self.installdir, self.pylibdir)
        args = "install --prefix=%(path)s --install-lib=%(path)s/%(pylibdir)s" % {'path': self.installdir,
                                                                                  'pylibdir': self.pylibdir}

        env.setvar('PYTHONPATH', '%s:%s' % (pylibdir, os.getenv('PYTHONPATH')))

        try:
            os.mkdir(pylibdir)

            cmd = "python setup.py %s" % args
            run_cmd(cmd, log_all=True, simple=True, log_output=True)
        except OSError, err:
            self.log.error("Failed to install: %s" % err)

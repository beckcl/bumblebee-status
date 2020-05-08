"""Check updates to Arch Linux.

Requires the following executable:
    * checkupdates (from pacman-contrib)

contributed by `lucassouto <https://github.com/lucassouto>`_ - many thanks!
"""

import logging

import core.module
import core.widget
import core.decorators

import util.cli


class Module(core.module.Module):
    @core.decorators.every(minutes=60)
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.utilization))
        self.__packages = 0

    @property
    def __format(self):
        return self.parameter("format", "Update Arch: {}")

    def utilization(self, widget):
        return self.__format.format(self.__packages if self.__packages >= 0 else "n/a")

    def hidden(self):
        return self.__packages == 0

    def update(self):
        try:
            result = util.cli.execute("checkupdates")
            self.__packages = len(result.split("\n")) - 1
        except Exception as e:
            logging.exception(e)
            self.__packages = -1

    def state(self, widget):
        return self.threshold_state(self.__packages, 1, 100)


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

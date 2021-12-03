#!/usr/bin/env python3
import sys

sys.path.append("lib")

from charms.osm.sshproxy import SSHProxyCharm
from ops.main import main


class SampleProxyCharm(SSHProxyCharm):
    def __init__(self, framework, key):
        super().__init__(framework, key)

        # Listen to charm events
        self.framework.observe(self.on.config_changed, self.on_config_changed)
        self.framework.observe(self.on.install, self.on_install)
        self.framework.observe(self.on.start, self.on_start)
        # self.framework.observe(self.on.upgrade_charm, self.on_upgrade_charm)

        # Listen to the touch action event
        # self.framework.observe(self.on.configure_remote_action, self.configure_remote)
        # self.framework.observe(self.on.start_service_action, self.start_service)
        self.framework.observe(self.on.touch_action, self.touch)
    def on_config_changed(self, event):
        """Handle changes in configuration"""
        super().on_config_changed(event)

    def on_install(self, event):
        """Called when the charm is being installed"""
        super().on_install(event)

    def on_start(self, event):
        """Called when the charm is being started"""
        super().on_start(event)

    def touch(self, event):
        """Touch action."""

        if self.model.unit.is_leader():
            stderr = None
            try:
                filename = event.params["filename"]
                cmd = "touch {}".format(filename)
                proxy = self.get_ssh_proxy()
                stdout, stderr = proxy.run(cmd)
                event.set_results({"output": stdout})
            except Exception as e:
                event.fail("Action failed {}. Stderr: {}".format(e, stderr))
        else:
            event.fail("Touch Action failed")

    # def configure_remote(self, event):
    #     """Configure remote action."""

    #     if self.model.unit.is_leader():
    #         stderr = None
    #         try:
    #             mgmt_ip = self.model.config["ssh-hostname"]
    #             destination_ip = event.params["destination_ip"]
    #             cmd = "vnfcli set license {} server {}".format(
    #                 mgmt_ip,
    #                 destination_ip
    #             )
    #             proxy = self.get_ssh_proxy()
    #             stdout, stderr = proxy.run(cmd)
    #             event.set_results({"output": stdout})
    #         except Exception as e:
    #             event.fail("Action failed {}. Stderr: {}".format(e, stderr))
    #     else:
    #         event.fail("Unit is not leader")

    # def start_service(self, event):
    #     """Start service action."""

    #     if self.model.unit.is_leader():
    #         stderr = None
    #         try:
    #             cmd = "sudo service vnfoper start"
    #             proxy = self.get_ssh_proxy()
    #             stdout, stderr = proxy.run(cmd)
    #             event.set_results({"output": stdout})
    #         except Exception as e:
    #             event.fail("Action failed {}. Stderr: {}".format(e, stderr))
    #     else:
    #         event.fail("Unit is not leader")


if __name__ == "__main__":
    main(SampleProxyCharm)
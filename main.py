# coding:utf-8
import datetime
import os
import signal
import subprocess
import sys
import time
from roslibpy import Ros, Topic

VMSTAT = './scripts/vmstat.sh'
IOSTAT = './scripts/iostat.sh'
VTUNE = './scripts/vtune.sh'

stop = False

argvs = sys.argv
argc = len(argvs)


def handler(signal, frame):
    global stop
    stop = True


class rosbridge_client:
    def __init__(self, duration: int):
        self.running = False
        self.duration = str(duration)
        self.operation_mode = None
        self.vmstat = None
        self.iostat = None
        self.vtune = None

        signal.signal(signal.SIGINT, handler)

        self.ros_client = Ros("127.0.0.1", 9090)

        self.listener = Topic(
            self.ros_client,
            "/api/external/get/rosbag_logging_mode",
            "tier4_external_api_msgs/msg/RosbagLoggingMode",
        )
        self.listener.subscribe(self.callback)
        self.run()

    def callback(self, message):
        mode = message["is_operation_mode"]
        if self.operation_mode != mode:
            self.operation_mode = mode
            mode_str = "operation" if self.operation_mode else "always"
            print('New logging mode received. ' + mode_str)

            time = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            path = time + "_" + mode_str
            self.run_proc(path)

    def run(self):
        try:
            print('Running ros client...')
            self.ros_client.run()
        except Exception as e:
            self.terminate()
            print(e)
            exit(1)

        while stop is False:
            if self.running:
                if self.is_proc_alive(self.vmstat) is False:
                    if self.is_proc_alive(self.iotat) is False:
                        if self.is_proc_alive(self.vtune) is False:
                            print("All processes not running...")
                            break

            time.sleep(1.0)

        self.terminate()

    def run_proc(self, path: str):
        self.terminate_proc()
  
        if not os.path.isdir(path):
            os.mkdir(path)

        self.vmstat = subprocess.Popen([VMSTAT, self.duration, path], stdout=subprocess.PIPE)
        self.iotat = subprocess.Popen([IOSTAT, self.duration, path], stdout=subprocess.PIPE)
        self.vtune = subprocess.Popen([VTUNE, self.duration, path], stdout=subprocess.PIPE)

        self.running = True

        print('Running...')

    def is_proc_alive(self, proc):
        if proc:
            poll = proc.poll()
            if poll is None:
                return True

        return False

    def kill_proc(self, proc):
        if proc:
            proc.kill()

    def terminate_proc(self):
        self.kill_proc(self.vmstat)
        self.kill_proc(self.iostat)
        self.kill_proc(self.vtune)

    def terminate(self):
        self.terminate_proc()
        self.listener.unsubscribe()
        self.ros_client.terminate()


if __name__ == "__main__":
    duration = 600

    if (argc == 2):
        duration = int(argvs[1])

    rosbridge_client(duration)

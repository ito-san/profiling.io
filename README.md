# :hammer_and_pick: profiling.io
A tool for profiling I/O performance.

This tool runs `vmstat`, `iostat`, and  Intel VTune's memory access analysis at the same time.

## :point_up: How to use

### Preparation

1. Install Intel VTune

   Please follow this instructions provided by Intel: 
   [Intel® VTune™ Profiler Installation Guide](https://www.intel.com/content/www/us/en/develop/documentation/vtune-install-guide/top/linux/package-managers.html)

1. Add the path to VTune executable in your `~/.bashrc`

    ex.)

    ```text
    export PATH="${PATH}:/opt/intel/oneapi/vtune/latest/bin64"
    ```

1. Type the following commands in your terminal as root user.

   ```console
   sudo su
   echo 0 > /proc/sys/kernel/perf_event_paranoid
   echo 0 > /proc/sys/kernel/kptr_restrict
   echo 0 > /proc/sys/kernel/yama/ptrace_scope
   echo 0 > /proc/sys/dev/i915/perf_stream_paranoid
   ```

### :zap: How to run

1. Clone this repository.

   ```console
   git clone git@github.com:ito-san/profiling.io.git
   ```

1. Type the following command in your terminal.

   ```console
   cd profiling.io
   python3 main.py
   ```

   The profiling duration is 10 minites by default.<br>
   You can specify any duration seconds to profile.<br>
   ex.) 1 minute

   ```console
   python3 main.py 60
   ```

1. Profiling will automatically start when receiving the ROS topic `/api/external/get/rosbag_logging_mode`.

### :open_file_folder: Data to be generated

Data will be stored in the directory with stored in the directory of <br>
`YYYYMMDDhhmmss_operation` when rosbag_logging_mode is operation mode,<br>
`YYYYMMDDhhmmss_always` when the mode is always mode.

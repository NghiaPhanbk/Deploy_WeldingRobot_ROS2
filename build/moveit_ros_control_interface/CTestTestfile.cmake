# CMake generated Testfile for 
# Source directory: /home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface
# Build directory: /home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test([=[cppcheck]=] "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/test_results/moveit_ros_control_interface/cppcheck.xunit.xml" "--package-name" "moveit_ros_control_interface" "--output-file" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/ament_cppcheck/cppcheck.txt" "--command" "/opt/ros/humble/bin/ament_cppcheck" "--xunit-file" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/test_results/moveit_ros_control_interface/cppcheck.xunit.xml" "--include_dirs" "/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/include")
set_tests_properties([=[cppcheck]=] PROPERTIES  LABELS "cppcheck;linter" TIMEOUT "300" WORKING_DIRECTORY "/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_cppcheck/cmake/ament_cppcheck.cmake;66;ament_add_test;/opt/ros/humble/share/ament_cmake_cppcheck/cmake/ament_cmake_cppcheck_lint_hook.cmake;87;ament_cppcheck;/opt/ros/humble/share/ament_cmake_cppcheck/cmake/ament_cmake_cppcheck_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/CMakeLists.txt;105;ament_package;/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/CMakeLists.txt;0;")
add_test([=[lint_cmake]=] "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/test_results/moveit_ros_control_interface/lint_cmake.xunit.xml" "--package-name" "moveit_ros_control_interface" "--output-file" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/ament_lint_cmake/lint_cmake.txt" "--command" "/opt/ros/humble/bin/ament_lint_cmake" "--xunit-file" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/test_results/moveit_ros_control_interface/lint_cmake.xunit.xml")
set_tests_properties([=[lint_cmake]=] PROPERTIES  LABELS "lint_cmake;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_lint_cmake/cmake/ament_lint_cmake.cmake;47;ament_add_test;/opt/ros/humble/share/ament_cmake_lint_cmake/cmake/ament_cmake_lint_cmake_lint_hook.cmake;21;ament_lint_cmake;/opt/ros/humble/share/ament_cmake_lint_cmake/cmake/ament_cmake_lint_cmake_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/CMakeLists.txt;105;ament_package;/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/CMakeLists.txt;0;")
add_test([=[xmllint]=] "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/test_results/moveit_ros_control_interface/xmllint.xunit.xml" "--package-name" "moveit_ros_control_interface" "--output-file" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/ament_xmllint/xmllint.txt" "--command" "/opt/ros/humble/bin/ament_xmllint" "--xunit-file" "/home/nghiaphanbk/WeldingRobot_ws/build/moveit_ros_control_interface/test_results/moveit_ros_control_interface/xmllint.xunit.xml")
set_tests_properties([=[xmllint]=] PROPERTIES  LABELS "xmllint;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_xmllint/cmake/ament_xmllint.cmake;50;ament_add_test;/opt/ros/humble/share/ament_cmake_xmllint/cmake/ament_cmake_xmllint_lint_hook.cmake;18;ament_xmllint;/opt/ros/humble/share/ament_cmake_xmllint/cmake/ament_cmake_xmllint_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/CMakeLists.txt;105;ament_package;/home/nghiaphanbk/WeldingRobot_ws/src/moveit2/moveit_plugins/moveit_ros_control_interface/CMakeLists.txt;0;")

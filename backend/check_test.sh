#!/bin/bash

check_logs() {
  local container_name=$1
  output=$(docker logs --tail 10 "$container_name" | grep failed)

  if [[ $? -ne 0 ]]; then
    echo "No failures found in logs of $container_name."
  else
    echo "Failures found in logs of $container_name:"
    echo "$output"
    return 1
  fi
}

check_logs task_manager_container_test
task_manager_status=$?

check_logs user_manager_container_test
user_manager_status=$?

if [[ $task_manager_status -ne 0 || $user_manager_status -ne 0 ]]; then
  exit 1
else
  exit 0
fi
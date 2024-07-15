#!/bin/bash

# Функция для проверки логов контейнера и записи их в файл
check_logs() {
  local container_name=$1
  local log_file="${container_name}_logs.txt"

  docker logs --tail 10 "$container_name" > "$log_file"
  
  # Проверка наличия ключевых слов в логах
  if grep -q "failed" "$log_file"; then
    echo "Failures found in logs of $container_name. See $log_file for details."
    echo "$log_file"
  else
    echo "No failures found in logs of $container_name."
    rm "$log_file"
    echo ""
  fi
}

# Проверка логов каждого контейнера
check_logs task_manager_container_test
task_manager_logs=$?

check_logs user_manager_container_test
user_manager_logs=$?

# Возвращаем соответствующий код выхода
if [[ $task_manager_logs -ne 0 || $user_manager_logs -ne 0 ]]; then
  exit 1
else
  exit 0
fi

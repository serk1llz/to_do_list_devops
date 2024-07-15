#!/bin/bash

curl -F chat_id=${TELEGRAM_CHAT_ID} -F document=@task_manager.txt https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendDocument
curl -F chat_id=${TELEGRAM_CHAT_ID} -F document=@user_manager.txt https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendDocument

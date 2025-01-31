import os
from pathlib import Path

from google.cloud import pubsub_v1

from .constants import (
    CRYPTOBLOTTER,
    GCP_APPLICATION_CREDENTIALS,
    LOCAL_ENV_VARS,
    PRODUCTION_ENV_VARS,
    PROJECT_ID,
)


def set_environment():
    if not os.path.exists("/.dockerenv"):
        with open("env.yaml", "r") as env:
            for line in env:
                key, value = line.split(": ")
                if key in LOCAL_ENV_VARS:
                    v = value.strip()
                    if key in GCP_APPLICATION_CREDENTIALS:
                        path = Path.cwd().parents[0] / "keys" / v
                        v = str(path.resolve())
                    os.environ[key] = v


def get_env_vars():
    env_vars = {}
    with open("env.yaml", "r") as env:
        for line in env:
            key, value = line.split(": ")
            env_vars[key] = value.strip()
    return env_vars


def get_deploy_env_vars(pre="", sep=",", keys=PRODUCTION_ENV_VARS):
    env_vars = [
        f"{pre}{key}={value}" for key, value in get_env_vars().items() if key in keys
    ]
    return f"{sep}".join(env_vars)


def is_local():
    return all([os.environ.get(key) is None for key in LOCAL_ENV_VARS])


def get_topic_path():
    return pubsub_v1.PublisherClient().topic_path(os.getenv(PROJECT_ID), CRYPTOBLOTTER)


def get_subscription_path(topic):
    return pubsub_v1.SubscriberClient().subscription_path(os.getenv(PROJECT_ID), topic)


def get_container_name(hostname="asia.gcr.io", image=CRYPTOBLOTTER, tag=None):
    project_id = os.environ[PROJECT_ID]
    container_name = f"{hostname}/{project_id}/{image}"
    if tag:
        container_name += f":{tag}"
    return container_name

import yaml
import re

import streamlit as st
from tools.k8s_tool import K8s

k8s = K8s()

class Kafkaui:
    def __init__(self):
        self.SECRET_KEY = "kafkaui"
        config = st.secrets[self.SECRET_KEY]
        self.NAMESPACE = config.namespace
        self.POD = config.pod
        self.RBAC_CONFIGMAP = config.rbac_configmap
        self.ENV_CONFIGMAP = config.env_configmap

    def get_env_configmap(self) -> str:
        configmap_list: list = k8s.read_configmap_list(self.NAMESPACE)
        for config in configmap_list:
            if config == self.ENV_CONFIGMAP:
                return config
                    
    def get_rbac_configmap(self) -> str:
        configmap_list: list = k8s.read_configmap_list(self.NAMESPACE)
        for config in configmap_list:
            if config == self.RBAC_CONFIGMAP:
                return config

    def get_pod(self) -> str:
        pod_list: list = k8s.read_pod_list(self.NAMESPACE)
        for pod in pod_list:
            if pod.startswith(self.POD):
                return pod
    
    def add(self, new_role):
        role_raw: yaml = self.get_role_raw()
        role_dict: dict = yaml.safe_load(role_raw)
        role_dict["rbac"]["roles"].append(new_role)
        self.save_configmap(role_dict)

    def change(self, role_edited):
        role_raw: yaml = self.get_role_raw()
        role_dict: dict = yaml.safe_load(role_raw)
        role_dict["rbac"]["roles"] = role_edited
        self.save_configmap(role_dict)

    def save_configmap(self, role_dict):
        new_yaml: yaml = yaml.dump(role_dict)
        new_json = {
            "config.yml" : new_yaml
        }
        configmap: str = self.get_rbac_configmap()
        k8s.patch_configmap(self.NAMESPACE, configmap, new_json)
               
    def restart_pod(self):
        pod: str = self.get_pod()
        k8s.delete_pod(self.NAMESPACE, pod)

    def get_role_raw(self) -> str:
        configmap: str = self.get_rbac_configmap()
        kafkaui_V1ConfigMap = k8s.read_configmap(self.NAMESPACE, configmap)
        auth_config: str = kafkaui_V1ConfigMap.data.get("config.yml")
        return auth_config
    
    def get_role(self) -> list:
        role_raw: yaml = self.get_role_raw()
        role_list: list = yaml.safe_load(role_raw).get("rbac").get("roles")
        for role in role_list:
            for permission in role["permissions"]:
                if type(permission["actions"]) != list:
                    permission["actions"] = [permission["actions"]]
                permission["actions"] = [x.lower() for x in permission["actions"]]
        return role_list

    def get_resource(self):
        return self.NAMESPACE, self.get_pod(), self.get_rbac_configmap()
    
    def get_kafka_clusters(self):
        configmap: str = self.get_env_configmap()
        kafkaui_V1ConfigMap = k8s.read_configmap(self.NAMESPACE, configmap)
        env_list: str = kafkaui_V1ConfigMap.data
        pattern = "(KAFKA_CLUSTERS_)[0-9](_NAME)"
        clusters = []
        for key, value in env_list.items():
            if re.match(pattern, key):
                clusters.append(value)
        return clusters

import logging

from kubernetes import config, client
from kubernetes.client.rest import ApiException

class K8s:
    def __init__(self) -> None:
        self.K8S_CONFIG_PATH = "./config/kubeconfig"
        config.load_kube_config(self.K8S_CONFIG_PATH)
        self.corev1, self.appsv1 = client.CoreV1Api(), client.AppsV1Api()
        
    def patch_configmap(self, namespace, configmap, data):
        try:
            body = client.V1ConfigMap(
                data=data,
            )
            res_V1ConfigMap = self.corev1.patch_namespaced_config_map(
                name=configmap,
                namespace=namespace,
                body=body)

        except ApiException as e:
            logging.error("Exception when calling CoreV1Api->patch_namespaced_config_map: %s\n" % e)

    def delete_pod(self, namespace, pod):
        try:
            res_V1Pod = self.corev1.delete_namespaced_pod(
                name=pod,
                namespace=namespace)
        except ApiException as e:
            logging.error("Exception when calling CoreV1Api->delete_namespaced_pod: %s\n" % e)

    def read_configmap_list(self, namespace) -> list:
        try:
            res_V1ConfigMapList = self.corev1.list_namespaced_config_map( 
                namespace=namespace)
            configmap_list =[]
            for configmap in res_V1ConfigMapList.items:
                configmap_list.append(configmap.metadata.name)
            return configmap_list

        except ApiException as e:
            logging.error("Exception when calling CoreV1Api->list_namespaced_config_map: %s\n" % e)

    def read_pod_list(self, namespace) -> list:
        try:
            res_V1PodList = self.corev1.list_namespaced_pod( 
                namespace=namespace)
            pod_list =[]
            for pod in res_V1PodList.items:
                pod_list.append(pod.metadata.name)
            return pod_list
        
        except ApiException as e:
            logging.error("Exception when calling CoreV1Api->list_namespaced_pod: %s\n" % e)

    def read_configmap(self, namespace, configmap) -> client.V1ConfigMap:
        try:
            res_V1ConfigMap = self.corev1.read_namespaced_config_map(
                namespace=namespace,
                name=configmap, 
                )
            return res_V1ConfigMap

        except ApiException as e:
            logging.error("Exception when calling CoreV1Api->read_namespaced_config_map: %s\n" % e)

import logging

from kubernetes import config, client
from kubernetes.client.rest import ApiException

class K8s:
    def __init__(self) -> None:
        self.K8S_CONTEXT_PATH = "./config/k8scontext"
        config.load_kube_config(self.K8S_CONTEXT_PATH)
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

    def patch_deployment(self, namespace, deployment, body):
        try:
            res_V1Deployment = self.appsv1.patch_namespaced_deployment(
                name=deployment,
                namespace=namespace,
                body=body)

        except ApiException as e:
            logging.error("Exception when calling AppsV1Api->patch_namespaced_deployment: %s\n" % e)

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

    def read_deployment_list(self, namespace) -> list:
        try:
            res_V1DeploymentList = self.appsv1.list_namespaced_deployment( 
                namespace=namespace)
            deployment_list =[]
            for deploy in res_V1DeploymentList.items:
                deployment_list.append(deploy.metadata.name)
            return deployment_list
        
        except ApiException as e:
            logging.error("Exception when calling AppsV1Api->list_namespaced_deployment: %s\n" % e)

    def read_configmap(self, namespace, configmap) -> client.V1ConfigMap:
        try:
            res_V1ConfigMap = self.corev1.read_namespaced_config_map(
                namespace=namespace,
                name=configmap, 
                )
            return res_V1ConfigMap

        except ApiException as e:
            logging.error("Exception when calling CoreV1Api->read_namespaced_config_map: %s\n" % e)

from kubernetes import client, config

config.load_kube_config()

api_client = client.ApiClient()

deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="cloud-native-monitor"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(
            match_labels={"app": "cloud-native-monitor"}
        ),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(
                labels={"app": "cloud-native-monitor"}
            ),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="cloud-native-monitor-container",
                        image="280922563526.dkr.ecr.ap-south-1.amazonaws.com/cloud-native-monitor:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(
    namespace="default",
    body=deployment
)

service = client.V1Service(
    metadata=client.V1ObjectMeta(name="cloud-native-monitor-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "cloud-native-monitor-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(
    namespace="default",
    body=service
)
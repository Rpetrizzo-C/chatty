from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets,
    aws_elasticloadbalancingv2 as elbv2,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_certificatemanager as acm,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct


class ChatAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        vpc = ec2.Vpc(self, "ChatAppVPC", max_azs=2, nat_gateways=1)

        # ECS Cluster
        cluster = ecs.Cluster(self, "ChatAppCluster", vpc=vpc)

        # Backend Service
        backend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "BackendService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../backend"),
                container_port=8000,
                environment={
                    "CORS_ORIGINS": "https://your-domain.com",
                },
            ),
            public_load_balancer=True,
            listener_port=443,
            protocol=elbv2.ApplicationProtocol.HTTPS,
        )

        # Frontend Service
        frontend_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "FrontendService",
            cluster=cluster,
            cpu=256,
            memory_limit_mib=512,
            desired_count=1,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../frontend"),
                container_port=3000,
                environment={
                    "VITE_API_URL": f"https://api.your-domain.com",
                    "VITE_WS_URL": f"wss://api.your-domain.com",
                },
            ),
            public_load_balancer=True,
            listener_port=443,
            protocol=elbv2.ApplicationProtocol.HTTPS,
        )

        # Add health checks
        backend_service.target_group.configure_health_check(
            path="/docs", healthy_http_codes="200"
        )

        frontend_service.target_group.configure_health_check(
            path="/", healthy_http_codes="200"
        )

        # Optional: Add custom domain and SSL certificate
        zone = route53.HostedZone.from_lookup(
            self, "Zone", domain_name="your-domain.com"
        )

        certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name="your-domain.com",
            validation=acm.CertificateValidation.from_dns(zone),
        )

        # DNS records
        route53.ARecord(
            self,
            "FrontendDNS",
            zone=zone,
            target=route53.RecordTarget.from_alias(
                targets.LoadBalancerTarget(frontend_service.load_balancer)
            ),
            record_name="chat",
        )

        route53.ARecord(
            self,
            "BackendDNS",
            zone=zone,
            target=route53.RecordTarget.from_alias(
                targets.LoadBalancerTarget(backend_service.load_balancer)
            ),
            record_name="api",
        )

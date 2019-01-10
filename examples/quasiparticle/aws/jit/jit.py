import logging

from pcf.core import State
from pcf.core.quasiparticle import Quasiparticle

# from pcf.particle.aws.vpc.vpc import VPC

logging.basicConfig(level=logging.DEBUG)

for handler in logging.root.handlers:
    handler.addFilter(logging.Filter('pcf'))

# Edit example json to work in your account

# example quasiparticle that contains all required infrastructure

vpc_definition = {
    "flavor": "vpc",
    "aws_resource": {
        "custom_config": {
            "vpc_name": "jit-vpc",
        },
        "CidrBlock":"10.0.0.0/16"
    }
}

subnet_definition = {
    "flavor": "subnet",
    "parents":["vpc:pcf-jit-example"],
    "aws_resource": {
        "custom_config": {
            "subnet_name": "jit-subnet",
        },
        "CidrBlock":"10.0.0.0/24"
    }
}

security_group_definition = {
    "flavor": "security_group",
    "parents":["vpc:pcf-jit-example"],
    "aws_resource": {
        "custom_config":{
            "IpPermissions":[
                {
                    "FromPort": 80,
                    "IpProtocol": "tcp",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                    "ToPort": 80,
                }
            ]
        },
        "GroupName":"jit-sg",
    }
}

ec2_definition = {
    "flavor": "ec2_instance",  # Required
    "parents":["security_group:pcf-jit-example","subnet:pcf-jit-example"],
    "aws_resource": {
        "custom_config": {
            "instance_name": "jit-ec2",  # Required
        },
        # Refer to https://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.ServiceResource.create_instances for a full list of parameters
        "ImageId": "ami-11111111",  # Required
        "InstanceType": "t2.nano",  # Required
        "MaxCount": 1,
        "MinCount": 1,
        "SecurityGroupIds": [
            "$inherit$security_group:pcf-jit-example$GroupId"
        ],
        "SubnetId":"$inherit$subnet:pcf-jit-example$SubnetId",  # Required
        "UserData": "echo abc123",
    }
}

jit_example_definition = {
    "pcf_name": "pcf-jit-example",  # Required
    "flavor": "quasiparticle",  # Required
    "particles": [
        vpc_definition,
        security_group_definition,
        subnet_definition,
        ec2_definition
    ]
}

# create ec2_route53 quasiparticle
jit_quasiparticle = Quasiparticle(jit_example_definition)

# example start
jit_quasiparticle.set_desired_state(State.running)
jit_quasiparticle.apply(sync=True)
print(jit_quasiparticle.get_state())


# example terminate
jit_quasiparticle.set_desired_state(State.terminated)
jit_quasiparticle.apply(sync=True)
print(jit_quasiparticle.get_state())

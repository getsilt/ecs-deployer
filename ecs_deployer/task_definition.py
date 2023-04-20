def create_task_definition(execution_role, memory, cpu, deployment_type, task_role='', ):
    task_definition = {
        "networkMode": "awsvpc" if deployment_type != 'EXTERNAL' else 'bridge',
        "taskRoleArn": task_role,
        "containerDefinitions": [],
        "executionRoleArn": execution_role,
        "requiresCompatibilities": [
            deployment_type
        ],
        "memory": str(memory),
        "cpu": str(cpu)
    }

    return task_definition


def create_container_definition(env_vars, environment, container_name, ecr_path, command=None, cpu=256,
                                memory=512, ports=None, logs_group=None):
    port_mappings = []
    if ports:
        for p in ports:
            host_port = int(p.split(':')[0])
            container_port = int(p.split(':')[1])

            port_mappings.append({
                "hostPort": host_port,
                "protocol": "tcp",
                "containerPort": container_port
            })

    container_definition = {
        "environment": env_vars,
        "name": container_name,
        "mountPoints": [],
        "image": ecr_path,
        "cpu": cpu,
        "memory": memory,
        "portMappings": port_mappings,
        "essential": True,
        "volumesFrom": []
    }
    if command:
        container_definition["command"] = parse_command(command)

    if logs_group:
        container_definition["logConfiguration"] = {
            "logDriver": "awslogs",
            "options": {
                "awslogs-stream-prefix": "ecs",
                "awslogs-group": f"/ecs/{environment}-{logs_group}",
                "awslogs-region": "eu-west-1"
            }
        }

    return container_definition


def parse_command(cmd):
    return cmd.split(' ')

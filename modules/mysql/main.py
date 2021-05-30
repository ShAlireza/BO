from bo_shared.modules.app import create_module_app

import config

app = create_module_app()

print(config.KAFKA_HOST, config.KAFKA_PORT, config.KAFKA_TOPIC)

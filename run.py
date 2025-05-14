from app.config import DeploymentConfig, TestingConfig

from app import create_app

app = create_app(DeploymentConfig)

if __name__ == '__main__':
    app.run()
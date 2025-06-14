pipeline {
    agent any
    environment {
        DOCKER_IMAGE = "dadanyanya/flask_api-backend"
        DOCKER_REGISTRY = "docker.io"
        API_URL = "http://37.9.53.210:5000/ping"
        DEPLOY_USER="ubuntu"
        DEPLOY_HOST = "37.9.53.210"
        DEPLOY_PATH = "/home/${DEPLOY_USER}/app"
    }
    stages {
        stage('Checkout') {
            steps {
                git url: "https://github.com/daniilvs/flask_api.git", branch: "main"
            }
        }
        stage('Build') {
            steps {
                echo "Building image"
                script {
                    docker.build("${DOCKER_IMAGE}:latest")
                }
            }
        }

        stage('Test/Lint') {
            steps {
                echo "Running linter"
                script {
                    docker.image("${DOCKER_IMAGE}:latest").inside('-u root') {
                        sh 'python -m pip install flake8'
                        sh 'flake8  /app '
                        echo "Linting passed!"
                    }
                }
            }
        }

        stage('Push') {
            steps {
                echo "Pushing image"
                script {
                    docker.withRegistry('https://registry.hub.docker.com', '21') {
                        docker.image("${DOCKER_IMAGE}:latest").push()
                    }
                }
                echo "Docker image pushed to Docker Hub."
            }
        }
    
        stage('Deploy to Target Machine') {
            steps {
                echo "Deploing"
                sshagent (credentials: ['my-deploy-ssh-key']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                            set -euxo pipefail
                            echo "--- Connected to ${DEPLOY_HOST} ---"

                            if [ ! -d "${DEPLOY_PATH}" ]; then
                                mkdir -p "${DEPLOY_PATH}"
                                cd "${DEPLOY_PATH}"
                                git clone https://github.com/daniilvs/flask_api.git .
                            else
                                cd "${DEPLOY_PATH}"
                                git fetch --all
                                git reset --hard origin/main
                            fi

                            docker pull ${DOCKER_IMAGE}:latest
                            docker-compose up -d --remove-orphans
                            echo "--- Application deployed successfully ---"
                        '
                    """
                }
            }
        }
    }
}

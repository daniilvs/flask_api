pipeline {
    agent any
    environment {
        DOCKER_REGISTRY_URL = 'docker.io'
        IMAGE_NAME          = 'flask-api-backend'
        REGISTRY_CREDENTIALS_ID = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Source code checked out successfully."
            }
        }

        stage('Test/Lint') {
            steps {
                sh 'flake8 .'
                echo "Code quality check passed."
            }
        }

        stage('Build') {
            steps {
                script {
                    def fullImageName = "${env.DOCKER_REGISTRY_URL}/${IMAGE_NAME}:${env.BUILD_NUMBER}"
                    echo "Building Docker image"
                    appImage = docker.build(flask-api-backend)
                }
            }
        }

        stage('Push') {
            steps {
                script {

                    docker.withRegistry("https://index.docker.io/v1/", env.REGISTRY_CREDENTIALS_ID) {
                        
                        echo "Pushing image with tag: ${env.BUILD_NUMBER}"
                        appImage.push() 

                        echo "Tagging image as 'latest'"
                        appImage.push('latest') 
                    }
                    echo "Image pushed successfully."
                }
            }
        }
    }
}
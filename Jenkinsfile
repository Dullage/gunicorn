pipeline {
    agent none
    environment {
        DOCKER_REPO_SLUG = 'dullage/gunicorn-python'
    }
    stages {
        stage('Build') {
            parallel {
                stage('Build (amd64)') {
                    agent { label 'docker && amd64' }
                    steps {
                        sh 'docker build -t $DOCKER_REPO_SLUG:3.8-amd64 $WORKSPACE/3.8'
                        sh 'docker build -t $DOCKER_REPO_SLUG:3.8-alpine-amd64 $WORKSPACE/3.8-alpine'
                    }
                }
                stage('Build (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps {
                        sh 'docker build -t $DOCKER_REPO_SLUG:3.8-arm32v7 $WORKSPACE/3.8'
                        sh 'docker build -t $DOCKER_REPO_SLUG:3.8-alpine-arm32v7 $WORKSPACE/3.8-alpine'
                    }
                }
            }
        }
        stage('Deploy Builds') {
            when { branch 'master' }
            environment { DOCKER_CREDENTIALS = credentials('docker') }
            parallel {
                stage('Deploy (amd64)') {
                    agent { label 'docker && amd64' }
                    steps {
                        sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                        sh 'docker push $DOCKER_REPO_SLUG:3.8-amd64'
                        sh 'docker push $DOCKER_REPO_SLUG:3.8-alpine-amd64'
                    }
                }
                stage('Deploy (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps {
                        sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                        sh 'docker push $DOCKER_REPO_SLUG:3.8-arm32v7'
                        sh 'docker push $DOCKER_REPO_SLUG:3.8-alpine-arm32v7'
                    }
                }
            }
        }
        stage('Create & Deploy Manifests') {
            when { branch 'master' }
            agent { label 'docker' }
            environment {
                DOCKER_CREDENTIALS = credentials('docker')
                DOCKER_CLI_EXPERIMENTAL = 'enabled'
            }
            steps {
                sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                // 3.8
                sh 'docker manifest create $DOCKER_REPO_SLUG:3.8 $DOCKER_REPO_SLUG:3.8-amd64 $DOCKER_REPO_SLUG:3.8-arm32v7'
                sh 'docker manifest push $DOCKER_REPO_SLUG:3.8'
                // 3.8-alpine
                sh 'docker manifest create $DOCKER_REPO_SLUG:3.8-alpine $DOCKER_REPO_SLUG:3.8-alpine-amd64 $DOCKER_REPO_SLUG:3.8-alpine-arm32v7'
                sh 'docker manifest push $DOCKER_REPO_SLUG:3.8-alpine'
                // latest
                sh 'docker manifest create $DOCKER_REPO_SLUG:latest $DOCKER_REPO_SLUG:3.8-alpine-amd64 $DOCKER_REPO_SLUG:3.8-alpine-arm32v7'
                sh 'docker manifest push $DOCKER_REPO_SLUG:latest'
            }
        }
    }
}

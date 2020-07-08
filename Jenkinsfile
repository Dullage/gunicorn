pipeline {
    agent none
    environment {
        DOCKER_REPO_SLUG = 'dullage/gunicorn'
        GUNICORN_VERSION = '20.0'
        PYTHON_VERSION = '3.8'
        ALPINE_VERSION = '3.12'
        AMD_TAG = 'amd64'
        ARM_TAG = 'arm32v7'
    }
    stages {
        stage('Build') {
            parallel {
                stage('Build (amd64)') {
                    agent { label 'docker && amd64' }
                    steps {
                        sh 'docker build --build-arg BASE_IMAGE_TAG=${PYTHON_VERSION} --build-arg GUNICORN_VERSION=${GUNICORN_VERSION} -t $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-${AMD_TAG} $WORKSPACE'
                        sh 'docker build --build-arg BASE_IMAGE_TAG=${PYTHON_VERSION}-alpine${ALPINE_VERSION} --build-arg GUNICORN_VERSION=${GUNICORN_VERSION} -t $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${AMD_TAG} $WORKSPACE'
                    }
                }
                stage('Build (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps {
                        sh 'docker build --build-arg BASE_IMAGE_TAG=${PYTHON_VERSION} --build-arg GUNICORN_VERSION=${GUNICORN_VERSION} -t $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-${ARM_TAG} $WORKSPACE'
                        sh 'docker build --build-arg BASE_IMAGE_TAG=${PYTHON_VERSION}-alpine${ALPINE_VERSION} --build-arg GUNICORN_VERSION=${GUNICORN_VERSION} -t $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${ARM_TAG} $WORKSPACE'
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
                        sh 'docker push $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-${AMD_TAG}'
                        sh 'docker push $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${AMD_TAG}'
                    }
                }
                stage('Deploy (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps {
                        sh 'echo $DOCKER_CREDENTIALS_PSW | docker login -u $DOCKER_CREDENTIALS_USR --password-stdin'
                        sh 'docker push $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-${ARM_TAG}'
                        sh 'docker push $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${ARM_TAG}'
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
                // Debian
                sh 'docker manifest create $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION} $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-${AMD_TAG} $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-${ARM_TAG}'
                sh 'docker manifest push --purge $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}'
                // Alpine
                sh 'docker manifest create $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION} $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${AMD_TAG} $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${ARM_TAG}'
                sh 'docker manifest push --purge $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}'
                // Latest
                sh 'docker manifest create $DOCKER_REPO_SLUG:latest $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${AMD_TAG} $DOCKER_REPO_SLUG:${GUNICORN_VERSION}-python${PYTHON_VERSION}-alpine${ALPINE_VERSION}-${ARM_TAG}'
                sh 'docker manifest push --purge $DOCKER_REPO_SLUG:latest'
            }
        }
    }
}

pipeline {
    agent none
    stages {
        stage('Build') {
            parallel {
                stage('Build (amd64)') {
                    agent { label 'docker && amd64' }
                    steps { sh 'python3 ./.jenkins/jenkins.py build amd64' }
                }
                stage('Build (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps { sh 'python3 ./.jenkins/jenkins.py build arm32v7' }
                }
                stage('Build (arm64v8)') {
                    agent { label 'docker && arm64v8' }
                    steps { sh 'python3 ./.jenkins/jenkins.py build arm64v8' }
                }
            }
        }
        stage('Deploy Builds') {
            when { branch 'master' }
            environment { DOCKER_CREDENTIALS = credentials('docker') }
            parallel {
                stage('Build (amd64)') {
                    agent { label 'docker && amd64' }
                    steps { sh 'python3 ./.jenkins/jenkins.py deploy amd64' }
                }
                stage('Build (arm32v7)') {
                    agent { label 'docker && arm32v7' }
                    steps { sh 'python3 ./.jenkins/jenkins.py deploy arm32v7' }
                }
                stage('Build (arm64v8)') {
                    agent { label 'docker && arm64v8' }
                    steps { sh 'python3 ./.jenkins/jenkins.py deploy arm64v8' }
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
            steps { sh 'python3 ./.jenkins/jenkins.py manifest amd64 arm32v7 arm64v8' }
        }
    }
}
